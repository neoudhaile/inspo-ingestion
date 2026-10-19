#!/usr/bin/env python3
"""A website's essence: what it is, for whom, in what domain — and on which host.

Why this exists. The teardown prose was written about the PAGE. Clustering it grouped
sites by how they were built rather than what they are: fabra.com, "a browser-based
3D apparel design platform", never surfaced as fashion; appdrop.com and comnyang.com
clustered together on shared Next.js-and-analytics vocabulary. The scrape prompt
asked for exhaustive capture (DOM probe, computed colours, fonts) and never asked for
meaning, so agents were precise about pixels and improvised about purpose.

The essence is six fields, kept separate on purpose:

    subject   the thing actually shared — product, project, article, app, person
    host      the site it lives on, when that differs (appdrop.com/marcgmbh/link-bouquet
              is the Link Bouquet toy, hosted on the AppDrop app platform)
    does      one sentence: what a user can concretely DO with the subject
    for_whom  who it is for
    domain    the subject matter or industry it serves — split from `kind` because
              they are independent axes, and collapsing them is what lost fabra's
              "fashion" under its "generative tool"
    kind      what it IS — never "landing page" or "marketing site"

Where it comes from, best first:

  1. The enrichment step (enrich_prompt.md, step 7e) — the agent with the live site.
  2. `--live-problem`: a fresh, isolated, headless Sonnet session with Playwright, for
     sites whose stored teardown is known to be about the wrong thing (a sub-page
     URL, or prose that opens by describing the page).
  3. `--backfill`: Sonnet reading the stored prose, no browser. Cheaper, and good
     when the stored prose is about the right subject; flagged by confidence when not.

Validation is shared by all three and by apply_enriched, so a malformed or page-shaped
essence is caught the same way wherever it was produced. A bad essence never fails a
daemon run — it is dropped and the site marked, so the backfill picks it up later.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tools.ingest.config import INSPIRATION_JSON, INSPO, REPO
from tools.ingest.embed import _usable
from tools.ingest.jsonio import read_json, write_json_atomic

ESSENCE_KEYS = ("subject", "host", "does", "for_whom", "domain", "kind")
REQUIRED_TEXT = ("subject", "does", "for_whom", "domain", "kind")
PURPOSE_PROSE = ("what_it_is", "what_it_shows", "how_it_works")

# What the live re-scrape found at the URL. Only "live" may replace stored prose: the
# library records what the owner SAW. When a site has since died (404, 5xx, parked) or
# been shut down (acquired, sunset, expired event), the original capture is worth more
# than today's error page — the first live run replaced a researcher's homepage with
# "nothing published at this address" and Fey's research terminal with its sunset notice.
SITE_STATES = ("live", "gone", "sunset")

# "kind" names what a thing IS. These name the page it was seen on.
FORBIDDEN_KINDS = {"landing page", "home page", "homepage", "marketing site",
                   "marketing page", "website", "web site", "web page", "webpage",
                   "site", "page", "product page", "product landing page"}

MODEL = os.environ.get("NEOUD_ENRICH_MODEL", "claude-sonnet-5-5")
CLAUDE = os.environ.get("CLAUDE_BIN", str(Path.home() / ".local/bin/claude"))
NODE_BIN = os.environ.get("NEOUD_NODE_BIN",
                          str(Path.home() / ".nvm/versions/node/v20.20.2/bin"))
MCP_CONFIG = REPO / "tools/ingest/mcp.playwright.json"
LOCKDIR = Path("/tmp/neoud-ingest.lock.d")
RUN_CACHE = INSPO / "_essence"

PAGE_FIRST = re.compile(
    r"^\s*(the |a )?(product |marketing |)(landing|home)\s*page\b", re.I)


# --- validation -----------------------------------------------------------------

def validate_essence(e):
    """List of problems with an essence dict; empty means valid. Pure."""
    if not isinstance(e, dict):
        return ["essence is not an object"]
    errs = [f"missing {k}" for k in ESSENCE_KEYS if k not in e]
    for k in REQUIRED_TEXT:
        if k in e and (not isinstance(e[k], str) or not e[k].strip()):
            errs.append(f"{k} is empty")
    if "host" in e and e["host"] is not None and not isinstance(e["host"], str):
        errs.append("host must be a string or null")
    kind = (e.get("kind") or "").strip().lower().rstrip(".") if isinstance(e.get("kind"), str) else ""
    if kind in FORBIDDEN_KINDS:
        errs.append(f"kind '{kind}' names the page, not the thing")
    return errs


def normalize_essence(e):
    """Trim strings; turn empty-ish hosts into None. Assumes validate passed."""
    out = {k: (e.get(k).strip() if isinstance(e.get(k), str) else e.get(k))
           for k in ESSENCE_KEYS}
    if not out["host"] or str(out["host"]).strip().lower() in ("null", "none", "n/a"):
        out["host"] = None
    return out


def confidence_level(c):
    """'high — reason' -> 'high'. Unknown -> 'unknown'."""
    m = re.match(r"\s*(high|medium|low)\b", str(c or ""), re.I)
    return m.group(1).lower() if m else "unknown"


def check_site_design(payload):
    """Validate an enrichment payload's essence in place. Never raises.

    Called by apply_enriched before merging. A missing or invalid essence is not a
    reason to fail an unattended run: the essence is dropped, the reason recorded in
    `essence_status`, and `--backfill` repairs it later. Returns the status string.
    """
    e = payload.get("essence")
    if e is None:
        payload["essence_status"] = "missing"
        return "missing"
    errs = validate_essence(e)
    if errs:
        payload.pop("essence", None)
        payload["essence_status"] = "invalid: " + "; ".join(errs)
        return payload["essence_status"]
    payload["essence"] = normalize_essence(e)
    payload["essence_status"] = "ok"
    return "ok"


# --- robust JSON ----------------------------------------------------------------

def loads_loose(text):
    """Parse a model's JSON answer, repairing the slips models actually make.

    Seen in practice: a stray quote before a closing brace — `"desktop pet app","}`
    — which broke one of three test runs while the content itself was right. Also
    handled: code fences, prose around the object, trailing commas.
    """
    t = (text or "").strip()
    t = re.sub(r"^```(?:json)?\s*|\s*```$", "", t, flags=re.S)
    a, b = t.find("{"), t.rfind("}")
    if a < 0 or b <= a:
        raise ValueError("no JSON object in output")
    t = t[a:b + 1]
    try:
        return json.loads(t)
    except json.JSONDecodeError:
        pass
    repaired = re.sub(r'",\s*"(\s*[}\]])', r'"\1', t)      # "x","}  ->  "x"}
    repaired = re.sub(r",(\s*[}\]])", r"\1", repaired)      # trailing commas
    return json.loads(repaired)


# --- which sites need which treatment -------------------------------------------

def is_deep_url(url):
    return bool((urlparse(url or "").path or "/").strip("/"))


def _sites(doc):
    return {k: v for k, v in (doc.get("site_designs") or {}).items() if k != "_schema"}


def problem_sites(doc):
    """{domain: reason} for sites whose stored teardown describes the wrong thing.

    Skips sites already settled by a live run — a live essence, or a recorded
    site_state — so re-running is idempotent from the source itself, not from a
    gitignored cache that a cleanup could delete (which would mean paying to re-scrape
    the 24 deep-url sites, whose URLs never stop being deep).
    """
    out = {}
    for dom, e in _sites(doc).items():
        if e.get("site_state") or (e.get("essence_meta") or {}).get("source") == "live":
            continue
        reasons = []
        if is_deep_url(e.get("url")):
            reasons.append("deep-url")
        if PAGE_FIRST.match(e.get("what_it_is") or ""):
            reasons.append("page-first")
        if reasons:
            out[dom] = "+".join(reasons)
    return out


# --- prompts --------------------------------------------------------------------

RULES = """Rules:
- Describe the product, publication, project or person. NEVER the web page.
- "kind" must never be "landing page", "home page", "marketing site" or "website".
- "domain" is the subject matter or industry served (e.g. "fashion and apparel",
  "music production", "indie games"). Use "general" only if it truly serves no
  particular subject.
- Frameworks, analytics, hosting and other tech never appear in any prose field.
- Only state what the evidence supports. Do not infer a company's or platform's
  identity from a fragment of a page title."""

LIVE_PROMPT = """You are tearing down ONE website for a design-inspiration library. You have a Playwright browser.

URL: {url}

Steps:
1. Open the URL. Look around properly: scroll, and open one or two internal links
   (pricing, about, product, a sample item) if that helps you understand what this is.
2. If the URL is a sub-page (it has a path beyond the bare domain), ALSO open the
   domain root, so you know both the thing that was shared and the site it lives on.
3. Return ONLY a JSON object, no markdown fence and no commentary, with exactly:

{{
  "essence": {{
    "subject":  "the thing actually shared: the product, project, article, app or person",
    "host":     "the site it lives on, if different from the subject; otherwise null",
    "does":     "one sentence: what a user can concretely DO with the subject",
    "for_whom": "who it is for, a few words",
    "domain":   "the subject matter or industry it serves, a few words",
    "kind":     "what kind of thing it IS, a few words"
  }},
  "prose": {{
    "what_it_is":    "2-3 sentences. The essence in prose: the product, publication, person or project. Not the page.",
    "what_it_shows": "2-4 sentences. The content and offering actually presented. No layout chrome, no tech.",
    "how_it_works":  "2-4 sentences. The visitor's experience: what they do and what happens. No tech."
  }},
  "evidence":   ["the specific things on the live site your essence rests on: headlines, nav items, product names"],
  "confidence": "high | medium | low, and a one-line reason",
  "site_state": "live | gone | sunset"
}}

site_state:
- "live"   the thing that was shared is up and you could see what it is.
- "gone"   the shared URL is an error or empty: 404, 5xx, DNS failure, a parked
           domain, or a platform's "nothing here" page.
- "sunset" the thing has been shut down, acquired, closed or has ended, and the
           page is now mostly a notice about that.
When the state is not "live", still fill in every field from what you can learn,
and say in "confidence" what you could not see.

""" + RULES


BACKFILL_PROMPT = """You are cataloguing websites for a design-inspiration library. You have NO
browser: work only from the stored notes below, which were written by an earlier
crawler and often describe the web PAGE rather than the thing it is for.

For EACH site, state its essence. Watch for two traps:
1. Notes that open "the landing page for X" or "the marketing site for X" — describe X.
2. Notes about one item hosted on a larger platform (one user's app, one channel, one
   article — usually a URL with a path). Set "subject" to that item and "host" to the
   platform, and lower your confidence if the notes do not say what the platform is.

Return ONLY a JSON object keyed by domain, no markdown fence, with exactly:

{{
  "<domain>": {{
    "essence": {{"subject": "...", "host": null, "does": "...", "for_whom": "...",
                 "domain": "...", "kind": "..."}},
    "confidence": "high | medium | low, and a one-line reason"
  }}
}}

""" + RULES + """

SITES:
{sites}"""


def material(dom, e):
    """Stored knowledge about a site, scrubbed of pipeline narration."""
    bits = [f"domain: {dom}", f"url: {e.get('url', '')}", f"title: {e.get('title', '')}"]
    for k in PURPOSE_PROSE:
        v = _usable(e.get(k))
        if v:
            bits.append(f"{k}: {v}")
    hs = e.get("headings") or []
    if hs:
        bits.append("headings: " + " | ".join(str(h) for h in hs[:8]))
    return "\n".join(bits)


# --- running headless claude ----------------------------------------------------

def run_claude(prompt, *, browser, model=MODEL, timeout=420):
    """One headless Sonnet session in its own EMPTY directory.

    Isolation is not hygiene for its own sake: Claude Code lets a session read its
    working directory without asking, and in testing one session read the list of
    the other sites it was not asked about and reported on them. An empty temp dir
    per run removes that whole class of leak.
    """
    work = tempfile.mkdtemp(prefix="essence-")
    env = dict(os.environ)
    if Path(NODE_BIN).is_dir():
        env["PATH"] = f"{NODE_BIN}:{env.get('PATH', '')}"
    cmd = [CLAUDE, "-p", prompt, "--model", model, "--output-format", "json",
           "--strict-mcp-config"]
    if browser:
        cmd += ["--mcp-config", str(MCP_CONFIG), "--allowedTools", "mcp__playwright"]
    try:
        r = subprocess.run(cmd, cwd=work, env=env, capture_output=True, text=True,
                           timeout=timeout)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    if r.returncode != 0:
        raise RuntimeError(f"claude exited {r.returncode}: {r.stderr[-300:]}")
    meta = json.loads(r.stdout)
    if meta.get("is_error"):
        raise RuntimeError(f"claude reported an error: {str(meta.get('result'))[:300]}")
    return meta.get("result", ""), meta


def scrape_live(dom, url, model=MODEL, attempts=2):
    """Fresh live essence + purpose prose for one site. Retries once if invalid."""
    last = None
    for attempt in range(attempts):
        try:
            text, meta = run_claude(LIVE_PROMPT.format(url=url), browser=True, model=model)
            d = loads_loose(text)
            errs = validate_essence(d.get("essence"))
            prose = d.get("prose") or {}
            errs += [f"prose.{k} empty" for k in PURPOSE_PROSE
                     if not str(prose.get(k, "")).strip()]
            state = str(d.get("site_state", "")).strip().lower()
            if state not in SITE_STATES:
                errs.append(f"site_state {state!r} not in {SITE_STATES}")
            if errs:
                raise ValueError("; ".join(errs))
            return {
                "essence": normalize_essence(d["essence"]),
                "prose": {k: prose[k].strip() for k in PURPOSE_PROSE},
                "evidence": [str(x) for x in (d.get("evidence") or [])][:20],
                "confidence": str(d.get("confidence", "")),
                "site_state": state,
                "cost_usd": meta.get("total_cost_usd", 0.0),
                "turns": meta.get("num_turns"),
                "attempts": attempt + 1,
            }
        except Exception as exc:                       # noqa: BLE001 - retried, then reported
            last = exc
    raise RuntimeError(f"{dom}: {last}")


def backfill_batch(batch, model=MODEL, attempts=2):
    """({domain: result}, {domain: why_invalid}) for a batch, from stored prose."""
    sites = "\n\n---\n\n".join(material(d, e) for d, e in batch)
    want = [d for d, _ in batch]
    last = None
    for attempt in range(attempts):
        try:
            text, meta = run_claude(BACKFILL_PROMPT.format(sites=sites), browser=False,
                                    model=model, timeout=300)
            d = loads_loose(text)
            out, bad = {}, {}
            for dom in want:
                r = d.get(dom) or {}
                errs = validate_essence(r.get("essence"))
                if errs:
                    bad[dom] = "; ".join(errs)
                    continue
                out[dom] = {"essence": normalize_essence(r["essence"]),
                            "confidence": str(r.get("confidence", "")),
                            "attempts": attempt + 1}
            share = meta.get("total_cost_usd", 0.0) / max(len(batch), 1)
            for r in out.values():
                r["cost_usd"] = share
            if not bad or attempt == attempts - 1:
                return out, bad
            last = ValueError(f"invalid for {list(bad)}")
        except Exception as exc:                       # noqa: BLE001
            last = exc
    raise RuntimeError(f"batch failed: {last}")


# --- writing results back -------------------------------------------------------

def acquire_lock(wait=900, poll=5):
    """Take the daemon's lock; inspiration.json must never be written by two
    processes at once. Waits out a running daemon fire rather than racing it."""
    deadline = time.time() + wait
    while True:
        try:
            os.mkdir(LOCKDIR)
            return True
        except FileExistsError:
            if time.time() > deadline:
                return False
            time.sleep(poll)


def release_lock():
    try:
        os.rmdir(LOCKDIR)
    except OSError:
        pass


def apply_results(doc, results, source, model, when=None):
    """Write essences (and, for live results, purpose prose) into `doc`. Pure on doc.

    This deliberately overrides merge_site_designs' never-overwrite rule, for the
    live mode only and only for the three purpose prose fields: those sites were
    selected precisely because their stored prose describes the wrong thing. The
    design prose and the DOM sidecar are never touched — they were DOM-grounded, and
    the live essence run does not repeat the probe. Git keeps the replaced text.

    A live result whose site_state is not "live" writes NOTHING but the state: the
    stored capture is a record of what the owner saw, and a dead or sunset site's
    current page is not a better description of it. Its essence is then left for the
    prose backfill, which derives it from that original capture.
    """
    when = when or datetime.now().isoformat(timespec="seconds")
    sd = doc["site_designs"]
    n = 0
    for dom, r in results.items():
        if dom not in sd:
            continue
        entry = sd[dom]
        state = r.get("site_state", "live") if source == "live" else None
        if state and state != "live":
            entry["site_state"] = {"state": state, "at": when,
                                   "note": r.get("confidence", "")}
            continue
        if state == "live":
            entry.pop("site_state", None)
        entry["essence"] = r["essence"]
        entry["essence_status"] = "ok"
        entry["essence_meta"] = {
            "source": source, "model": model, "at": when,
            "confidence": confidence_level(r.get("confidence")),
            "confidence_note": r.get("confidence", ""),
        }
        if r.get("evidence"):
            entry["essence_meta"]["evidence"] = r["evidence"]
        if source == "live":
            for k in PURPOSE_PROSE:
                entry[k] = r["prose"][k]
        n += 1
    return n


def _save_run(results, name):
    RUN_CACHE.mkdir(parents=True, exist_ok=True)
    write_json_atomic(RUN_CACHE / f"{name}.json", results)


def _load_run(name):
    p = RUN_CACHE / f"{name}.json"
    return read_json(p) if p.exists() else {}


def commit_to_source(results, source, model):
    """Apply under the daemon lock, re-reading the source inside it."""
    if not results:
        return 0
    if not acquire_lock():
        raise RuntimeError("daemon lock held too long; results are kept in the run "
                           "cache, rerun to apply them")
    try:
        doc = read_json(INSPIRATION_JSON)
        n = apply_results(doc, results, source, model)
        write_json_atomic(INSPIRATION_JSON, doc)
        return n
    finally:
        release_lock()


# --- CLI ------------------------------------------------------------------------

def run_live(doms, model, parallel, log=print):
    sd = _sites(read_json(INSPIRATION_JSON))
    cache = _load_run("live")
    todo = [d for d in doms if d not in cache]
    log(f"LIVE {len(todo)} to scrape ({len(doms) - len(todo)} cached from an earlier run)")
    failed = {}
    with ThreadPoolExecutor(max_workers=parallel) as ex:
        futs = {ex.submit(scrape_live, d, sd[d].get("url") or f"https://{d}/", model): d
                for d in todo}
        for f in as_completed(futs):
            d = futs[f]
            try:
                cache[d] = f.result()
                _save_run(cache, "live")       # paid work survives a crash
                r = cache[d]
                log(f"  ok   {d:30} {r['essence']['kind'][:38]:38} | "
                    f"{r['essence']['domain'][:32]:32} ${r['cost_usd']:.3f}", flush=True)
            except Exception as exc:          # noqa: BLE001
                failed[d] = str(exc)
                log(f"  FAIL {d}: {str(exc)[:160]}", flush=True)
    return {d: cache[d] for d in doms if d in cache}, failed


def run_backfill(doms, model, batch_size, parallel, log=print):
    sd = _sites(read_json(INSPIRATION_JSON))
    cache = _load_run("backfill")
    todo = [d for d in doms if d not in cache]
    batches = [todo[i:i + batch_size] for i in range(0, len(todo), batch_size)]
    log(f"BACKFILL {len(todo)} sites in {len(batches)} batches "
        f"({len(doms) - len(todo)} cached)", flush=True)
    failed = {}
    with ThreadPoolExecutor(max_workers=parallel) as ex:
        futs = {ex.submit(backfill_batch, [(d, sd[d]) for d in b], model): b for b in batches}
        for f in as_completed(futs):
            b = futs[f]
            try:
                out, bad = f.result()
                cache.update(out)
                failed.update(bad)
                _save_run(cache, "backfill")
                log(f"  batch ok {len(out)}/{len(b)}"
                    + (f"  invalid: {list(bad)}" if bad else ""), flush=True)
            except Exception as exc:          # noqa: BLE001
                for d in b:
                    failed[d] = str(exc)
                log(f"  batch FAIL ({len(b)} sites): {str(exc)[:160]}", flush=True)
    return {d: cache[d] for d in doms if d in cache}, failed


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--live-problem", action="store_true",
                      help="live re-scrape every deep-url / page-first site")
    mode.add_argument("--backfill", action="store_true",
                      help="essence from stored prose for every site still missing one")
    mode.add_argument("--list", action="store_true", help="show what each mode would do")
    ap.add_argument("--only", nargs="*", help="restrict to these domains")
    ap.add_argument("--model", default=MODEL)
    ap.add_argument("--parallel", type=int, default=4)
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--no-apply", action="store_true",
                    help="run and cache, but do not write inspiration.json")
    args = ap.parse_args()

    doc = read_json(INSPIRATION_JSON)
    sd = _sites(doc)
    problems = problem_sites(doc)
    missing = sorted(d for d, e in sd.items() if not e.get("essence"))
    only = set(args.only or [])

    if args.list:
        print(f"{len(problems)} live re-scrape candidates (deep url or page-first):")
        for d, why in sorted(problems.items()):
            print(f"  {d:34} {why}")
        print(f"\n{len(missing)} sites currently without an essence")
        return 0

    if args.live_problem:
        doms = sorted(d for d in problems if not only or d in only)
        results, failed = run_live(doms, args.model, args.parallel)
        source = "live"
    else:
        doms = [d for d in missing if not only or d in only]
        results, failed = run_backfill(doms, args.model, args.batch, args.parallel)
        source = "prose"

    not_live = sorted(d for d, r in results.items()
                      if r.get("site_state", "live") != "live")
    cost = sum(r.get("cost_usd", 0.0) for r in results.values())
    low = sorted(d for d, r in results.items()
                 if confidence_level(r.get("confidence")) == "low")
    print(f"\n{source.upper()}: {len(results)} ok, {len(failed)} failed, ${cost:.2f}")
    if low:
        print(f"low confidence ({len(low)}): {', '.join(low)}")
    if not_live:
        print(f"site changed since capture, original prose kept ({len(not_live)}): "
              + ", ".join(f"{d} [{results[d]['site_state']}]" for d in not_live))
    if failed:
        print("failed:")
        for d, why in sorted(failed.items()):
            print(f"  {d}: {why[:200]}")
    if not args.no_apply:
        n = commit_to_source(results, source, args.model)
        print(f"APPLIED {n} essences to inspiration.json ({source})"
              + (f"; {len(not_live)} recorded as changed, left for backfill"
                 if not_live else ""))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
