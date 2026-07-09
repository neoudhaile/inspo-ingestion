#!/usr/bin/env python3
"""Resumable teardown backfill for design-worthy items lacking a site_designs entry.

Processes category in {design, favorites, personal} whose primary_domain has no teardown,
in chunks, via the same enrich.sh + apply_enriched path. Recomputes the remaining set each
loop, so it's safe to stop/restart (already-done domains are skipped). Logs to
/tmp/neoud-backfill.log.
"""
import json, os, subprocess, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tools.ingest.config import INSPIRATION_JSON, INBOX, UTILITY_DENYLIST, REPO
from tools.ingest.jsonio import read_json, write_json_atomic

LOCKDIR = Path("/tmp/neoud-ingest.lock.d")  # same lock run.sh uses, so the daemon defers
ATTEMPTED = Path(__file__).resolve().parents[2] / "inspo" / "_backfill_attempted.json"

def load_attempted():
    return set(json.loads(ATTEMPTED.read_text())) if ATTEMPTED.exists() else set()

def mark_attempted(domains):
    s = load_attempted() | set(domains)
    ATTEMPTED.write_text(json.dumps(sorted(s), indent=2))

# Scope: default = design-worthy subset; pass --all to tear down every loadable domain.
CATS = {"design", "favorites", "personal"}
ALL = "--all" in sys.argv
CHUNK = 4
LOG = Path("/tmp/neoud-backfill.log")

def log(m):
    line = f"[{time.strftime('%H:%M:%S')}] {m}"
    with LOG.open("a") as f:
        f.write(line + "\n")
    print(line, flush=True)

def remaining():
    d = read_json(INSPIRATION_JSON)
    sd = {k for k in d["site_designs"] if k != "_schema"}
    done = sd | load_attempted()  # skip torn-down AND already-attempted-this-pass
    seen, out = set(), []
    for it in d["items"]:
        dom, u = it.get("primary_domain"), it.get("primary_url")
        if not u or not dom:
            continue
        if not ALL and it.get("category") not in CATS:
            continue
        if dom in done or dom in seen or any(x in dom for x in UTILITY_DENYLIST):
            continue
        seen.add(dom)
        out.append(it)
    return out

def to_newitem(it):
    cand = [it["primary_url"]] + [u for u in it.get("related_urls", []) if u != it["primary_url"]]
    return {
        "id": it["id"], "date": it.get("date"), "author": it.get("author"),
        "name": it.get("name"), "author_profile": it.get("author_profile"),
        "tweet": it.get("tweet"), "full_text": it.get("text") or "",
        "all_urls": it.get("all_urls") or cand, "primary_candidates": cand,
        "media": [{k: m.get(k) for k in ("type", "original_url", "thumbnail_url")}
                  for m in it.get("media", [])],
    }

def main():
    # Acquire the daemon lock (wait up to ~20m if a daemon run is in progress).
    for _ in range(120):
        try:
            os.mkdir(LOCKDIR); break
        except FileExistsError:
            log("daemon run in progress — waiting for lock…"); time.sleep(10)
    else:
        log("could not acquire lock; aborting"); return 1
    try:
        scope = "ALL" if ALL else "design-worthy"
        log(f"backfill start ({scope}): {len(remaining())} domains to tear down")
        batch = 0
        while True:
            rem = remaining()
            if not rem:
                log("backfill COMPLETE — nothing left")
                return 0
            chunk = rem[:CHUNK]
            batch += 1
            write_json_atomic(INBOX / "new-items.json",
                              {"source_export": "backfill", "items": [to_newitem(i) for i in chunk]})
            log(f"batch {batch}: {[c['primary_domain'] for c in chunk]}  ({len(rem)} remaining)")
            try:
                r = subprocess.run(["bash", "tools/ingest/enrich.sh"], cwd=str(REPO),
                                   capture_output=True, text=True, timeout=2700)
            except subprocess.TimeoutExpired:
                log("  enrich TIMEOUT (>45m) — stopping; rerun to resume")
                return 1
            if r.returncode != 0:
                log(f"  enrich FAILED rc={r.returncode} (rate limit?) — stopping; rerun to resume. {r.stderr[-300:]}")
                return 1
            a = subprocess.run([".venv/bin/python", "-m", "tools.ingest.apply_enriched"],
                              cwd=str(REPO), capture_output=True, text=True)
            # Mark this chunk attempted ONLY after a successful batch, so a domain the
            # enricher declines to tear down isn't retried forever (the churn bug); a
            # rate-limited/failed batch above returns early and is NOT marked, so it resumes.
            mark_attempted([c["primary_domain"] for c in chunk])
            log(f"  applied: {a.stdout.strip()} {a.stderr[-150:].strip()}")
    finally:
        try:
            os.rmdir(LOCKDIR)
        except OSError:
            pass

if __name__ == "__main__":
    raise SystemExit(main())
