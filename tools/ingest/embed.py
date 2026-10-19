#!/usr/bin/env python3
"""Embed each torn-down site into a vector, so similarity is measured not declared.

Why this exists: the vault's four facets could not answer "personal websites",
"books as a motif" or "light minimal portfolios" (see
docs/superpowers/specs/2026-10-17-vault-views-design.md). The information was in the
teardown prose all along; it was never structured. Embedding the prose makes
closeness computable without anyone maintaining a vocabulary.

Two spaces, because the owner wants two graphs:

  purpose — what the site IS, shows and does      (what_it_is + what_it_shows + how_it_works)
  design  — how it LOOKS and feels                (how_its_designed + palette + fonts + headings)

Both are built from fields already stored on every site, so embedding costs one API
call per site per space and never re-visits the web.

Vectors are cached on disk keyed by (model, exact text), so re-runs are free and
tuning the text recipe only re-embeds what actually changed.

Providers are swappable on purpose — the clustering is the experiment, not the
embedder. `hash` is a deterministic offline fake for tests; it produces stable
vectors with no network and no key, and is never meaningful for real clustering.
"""
import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tools.ingest.config import INSPIRATION_JSON, INSPO
from tools.ingest.jsonio import read_json, write_json_atomic

CACHE_DIR = INSPO / "_embeddings"

SPACES = ("purpose", "design")

# Gemini batch size and output width. 1536 is plenty for 201 items and halves
# both the cache and the distance maths; the model supports truncation natively.
GEMINI_BATCH = 50
GEMINI_DIM = 1536

# Gemini's free tier limits embeddings per minute, not per day: a full run trips it
# after a couple of requests and then recovers. So pace requests rather than firing
# them back to back, and back off for a whole minute when it still says no. Vectors
# checkpoint to disk after every batch, so even a hard failure only costs the batch
# in flight.
PACE_SECONDS = {"gemini": 20.0, "openai": 0.0, "hash": 0.0}
RATE_LIMIT_WAIT = 60.0

DEFAULT_MODELS = {
    "gemini": "gemini-embedding-001",
    "openai": "text-embedding-3-small",
    "hash": "hash-256",
}


# --- what text represents a site in each space ----------------------------------

# The teardown prose sometimes narrates the pipeline rather than the website: a
# failed capture, a WebFetch fallback, a bot-protection wall. Those sentences are
# true of our bad day, not of the site, and embedding them makes every site that had
# the same bad day look alike — ten of them once formed a cluster literally named
# "extracted captured. screenshot". They are stripped sentence by sentence, because
# they usually sit inside otherwise-good prose rather than replacing it.
NOT_CAPTURED = re.compile(r"^\s*(not[\s-]+captured|unknown)\b", re.I)

PIPELINE_NOISE = re.compile(
    r"webfetch|text-fetch|dom probe|not captured|extracted_via|non-browser fetcher"
    r"|blocks? non-browser|this run\b|no browser needed|bot protection"
    r"|blocked automated access|playwright",
    re.I)

SENTENCE = re.compile(r"(?<=[.!?])\s+")


def _scrub(text):
    """Drop sentences that describe the extraction rather than the site."""
    keep = [s for s in SENTENCE.split(text) if s.strip() and not PIPELINE_NOISE.search(s)]
    return " ".join(keep).strip()


def _clean(x):
    if not x:
        return ""
    if isinstance(x, (list, tuple)):
        return " ".join(str(i) for i in x if i)
    return str(x)


def _usable(x):
    """Text with pipeline narration removed; "" if nothing real is left."""
    t = _clean(x).strip()
    if NOT_CAPTURED.match(t):
        return ""
    return _scrub(t)


def space_text(dom, e, space):
    """The text that stands for this site in `space`. Pure; testable.

    Deliberately prose-led. The structured sidecars (palette, fonts) are appended as
    words rather than numbers because an embedder reads them as text either way, and
    the prose is what carries the meaning.

    Returns "" when the site has no real prose in this space. The title alone is not
    enough: embedding a bare domain name places the site somewhere arbitrary, which
    is worse than leaving it out of the graph and visibly unplaced.
    """
    if space == "purpose":
        prose = [
            _usable(e.get("what_it_is")),
            _usable(e.get("what_it_shows")),
            _usable(e.get("how_it_works")),
        ]
        head = [e.get("title") or dom]
    elif space == "design":
        prose = [
            _usable(e.get("how_its_designed")),
            _usable(e.get("palette")),
            _usable(e.get("fonts")),
            " ".join(_clean(f) for f in (e.get("fonts_loaded") or [])),
            " ".join(_clean(h) for h in (e.get("headings") or [])[:6]),
        ]
        head = []
    else:
        raise ValueError(f"unknown space: {space}")
    if not any(p.strip() for p in prose):
        return ""
    return "\n".join(p for p in head + prose if p).strip()


def corpus(doc, space):
    """[(domain, text)] for every site with usable text in this space."""
    sd = {k: v for k, v in (doc.get("site_designs") or {}).items() if k != "_schema"}
    out = []
    for dom, e in sorted(sd.items()):
        t = space_text(dom, e, space)
        if t:
            out.append((dom, t))
    return out


# --- cache ----------------------------------------------------------------------

def cache_path(provider, model):
    safe = f"{provider}-{model}".replace("/", "_")
    return CACHE_DIR / f"{safe}.json"


def text_key(text):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


def load_cache(provider, model):
    p = cache_path(provider, model)
    return read_json(p) if p.exists() else {}


def save_cache(provider, model, cache):
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    write_json_atomic(cache_path(provider, model), cache)


# --- providers ------------------------------------------------------------------

class RateLimited(Exception):
    """429, carrying the server's own Retry-After when it gave one."""

    def __init__(self, retry_after=None):
        super().__init__("rate limited")
        self.retry_after = retry_after


def _post_json(url, payload, headers, timeout=60):
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code == 429:
            ra = e.headers.get("Retry-After")
            raise RateLimited(float(ra) if ra and ra.isdigit() else None) from e
        # surface the body: the provider usually says exactly what was wrong
        body = ""
        try:
            body = e.read().decode("utf-8", "replace")[:500]
        except Exception:
            pass
        raise urllib.error.HTTPError(
            e.url, e.code, f"{e.reason} — {body}", e.headers, None) from None


def embed_hash(texts, model):
    """Deterministic offline fake. Not semantic — for tests and dry runs only."""
    dim = 256
    out = []
    for t in texts:
        h = hashlib.sha256(t.encode("utf-8")).digest()
        # tile the digest out to `dim` floats in [-1, 1]
        vals = [(h[i % len(h)] - 127.5) / 127.5 for i in range(dim)]
        out.append(vals)
    return out


def api_key(*names):
    """A key from the environment, else from the gitignored .env at the repo root.

    The daemon runs under launchd with a minimal environment, and a key pasted into
    a shell only lives in that shell — so a file the repo ignores is the one place
    both an interactive run and an unattended one can read. Format: KEY=value, one
    per line, '#' comments allowed.
    """
    for n in names:
        v = os.environ.get(n)
        if v:
            return v.strip()
    envfile = INSPO.parent / ".env"
    if envfile.exists():
        for line in envfile.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            if k.strip() in names:
                return v.strip().strip('"').strip("'")
    return None


def embed_gemini(texts, model):
    """Batched, via batchEmbedContents.

    One call per text would be 400+ requests for a full two-space run, which is both
    slow and the quickest way to meet a free-tier rate limit. Output is truncated to
    GEMINI_DIM: gemini-embedding-001 is Matryoshka-trained, so a prefix of the vector
    is itself a good embedding, and callers re-normalize before use (see
    cluster.normalize).
    """
    key = api_key("GEMINI_API_KEY", "GOOGLE_API_KEY")
    if not key:
        raise RuntimeError(
            "No Gemini key. Put GEMINI_API_KEY=... in the repo's .env (gitignored) "
            "or export it in the environment.")
    url = (f"https://generativelanguage.googleapis.com/v1beta/models/"
           f"{model}:batchEmbedContents?key={key}")
    out = []
    for i in range(0, len(texts), GEMINI_BATCH):
        batch = texts[i:i + GEMINI_BATCH]
        payload = {"requests": [{
            "model": f"models/{model}",
            "content": {"parts": [{"text": t}]},
            # clustering and nearest-neighbour, not question->document retrieval
            "taskType": "SEMANTIC_SIMILARITY",
            "outputDimensionality": GEMINI_DIM,
        } for t in batch]}
        r = _post_json(url, payload, {"Content-Type": "application/json"}, timeout=120)
        out.extend(e["values"] for e in r["embeddings"])
    return out


def embed_openai(texts, model):
    key = api_key("OPENAI_API_KEY")
    if not key:
        raise RuntimeError(
            "No OpenAI key. Put OPENAI_API_KEY=... in the repo's .env (gitignored) "
            "or export it in the environment.")
    out = []
    # the API takes batches; keep them modest so one failure costs little
    for i in range(0, len(texts), 64):
        batch = texts[i:i + 64]
        r = _post_json(
            "https://api.openai.com/v1/embeddings",
            {"model": model, "input": batch},
            {"Content-Type": "application/json", "Authorization": f"Bearer {key}"},
        )
        out.extend(d["embedding"] for d in sorted(r["data"], key=lambda d: d["index"]))
    return out


PROVIDERS = {"gemini": embed_gemini, "openai": embed_openai, "hash": embed_hash}


# --- the one entry point --------------------------------------------------------

def embed_texts(texts, provider="gemini", model=None, use_cache=True, log=print,
                retries=5):
    """Vectors for `texts`, in order. Cached by (model, exact text).

    Only uncached texts hit the network, so re-running after a prose tweak re-embeds
    just the sites whose text actually changed.
    """
    model = model or DEFAULT_MODELS[provider]
    fn = PROVIDERS[provider]
    cache = load_cache(provider, model) if use_cache else {}

    todo = [t for t in dict.fromkeys(texts) if text_key(t) not in cache]
    if todo:
        log(f"EMBED {len(todo)} new / {len(texts)} total via {provider}:{model}")
        # Match the provider's own batch size: double-batching just makes more
        # requests, which is the thing the rate limit counts.
        step = GEMINI_BATCH if provider == "gemini" else 64
        pace = PACE_SECONDS.get(provider, 0.0)
        done = 0
        for i in range(0, len(todo), step):
            batch = todo[i:i + step]
            if i and pace:
                time.sleep(pace)
            for attempt in range(retries):
                try:
                    vecs = fn(batch, model)
                    break
                except RateLimited as exc:
                    if attempt == retries - 1:
                        raise
                    wait = exc.retry_after or RATE_LIMIT_WAIT
                    log(f"  rate limited — waiting {wait:.0f}s "
                        f"(attempt {attempt + 1}/{retries}, {done}/{len(todo)} cached so far)")
                    time.sleep(wait)
                except (urllib.error.URLError, urllib.error.HTTPError, KeyError) as exc:
                    if attempt == retries - 1:
                        raise
                    wait = 2 ** attempt
                    log(f"  retry {attempt + 1}/{retries} after {exc} — sleeping {wait}s")
                    time.sleep(wait)
            for t, v in zip(batch, vecs):
                cache[text_key(t)] = v
            done += len(batch)
            log(f"  {done}/{len(todo)}")
            if use_cache:
                save_cache(provider, model, cache)   # checkpoint; a crash loses nothing
    else:
        log(f"EMBED 0 new / {len(texts)} total (all cached)")

    return [cache[text_key(t)] for t in texts]


def embed_space(space, provider="gemini", model=None, doc=None, log=print):
    """(domains, vectors) for one space."""
    doc = doc if doc is not None else read_json(INSPIRATION_JSON)
    pairs = corpus(doc, space)
    doms = [d for d, _ in pairs]
    vecs = embed_texts([t for _, t in pairs], provider=provider, model=model, log=log)
    return doms, vecs


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--space", choices=SPACES + ("all",), default="all")
    ap.add_argument("--provider", choices=tuple(PROVIDERS), default="gemini")
    ap.add_argument("--model", default=None)
    ap.add_argument("--dry-run", action="store_true",
                    help="report what would be embedded; no network, no key needed")
    args = ap.parse_args()

    doc = read_json(INSPIRATION_JSON)
    spaces = SPACES if args.space == "all" else (args.space,)
    for space in spaces:
        pairs = corpus(doc, space)
        if args.dry_run:
            lens = [len(t) for _, t in pairs]
            avg = sum(lens) // len(lens) if lens else 0
            print(f"{space}: {len(pairs)} sites, avg {avg} chars, "
                  f"min {min(lens, default=0)}, max {max(lens, default=0)}, "
                  f"~{sum(lens)//4} tokens total")
            continue
        doms, vecs = embed_space(space, args.provider, args.model, doc)
        print(f"{space}: {len(doms)} vectors, dim {len(vecs[0]) if vecs else 0}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
