#!/usr/bin/env python3
"""Ingest arbitrary URLs into the inspiration pipeline — the universal adapter.

The pipeline's seam is `new-items.json`: anything that can produce a URL list can
feed the same enrichment (teardown + facets) and writers as X bookmarks. This
module is that adapter. Mediums it covers by construction: pasted links, browser
bookmark exports, Raindrop/Pocket CSVs, read-later apps — anything you can reduce
to one URL per line.

Usage:
  .venv/bin/python -m tools.ingest.add_urls https://a.com https://b.com
  .venv/bin/python -m tools.ingest.add_urls --file urls.txt      # one URL per line, # comments ok
  NEOUD_HAVE_LOCK=1 ... (set by run.sh, which already holds the daemon lock)

Dedup: by synthetic item id (sha1 of normalized URL) against the ledger, and by
domain against existing site_designs (already-torn-down sites are skipped).
"""
import argparse
import hashlib
import os
import re
import subprocess
import sys
import time
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tools.ingest.config import INSPIRATION_JSON, INBOX, LEDGER, REPO
from tools.ingest.jsonio import read_json, write_json_atomic
from tools.ingest.ledger import load_ledger

LOCKDIR = Path("/tmp/neoud-ingest.lock.d")
CHUNK = 5


def normalize(url):
    url = url.strip()
    if not url or url.startswith("#"):
        return None
    if not re.match(r"^https?://", url):
        url = "https://" + url
    return url


def domain_of(url):
    h = urlparse(url).netloc.lower()
    return h[4:] if h.startswith("www.") else h


def url_id(url):
    return "url-" + hashlib.sha1(url.encode()).hexdigest()[:12]


def build_url_items(urls, doc, ledger):
    """Normalized items for URLs not already ingested/torn down. Pure; testable."""
    sd = {k for k in doc.get("site_designs", {}) if k != "_schema"}
    known = set(ledger.get("processed_ids", []))
    items, skipped = [], []
    seen = set()
    for raw in urls:
        url = normalize(raw)
        if not url or url in seen:
            continue
        seen.add(url)
        uid, dom = url_id(url), domain_of(url)
        if uid in known:
            skipped.append((url, "already ingested"))
            continue
        if dom in sd:
            skipped.append((url, f"domain {dom} already has a teardown"))
            continue
        items.append({
            "id": uid,
            "date": date.today().isoformat(),
            "author": None, "name": None, "author_profile": None, "tweet": None,
            "full_text": "",
            "all_urls": [url],
            "primary_candidates": [url],
            "media": [],
            "media_kinds": [],
            "source": "manual-url",
        })
    return items, skipped


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("urls", nargs="*")
    ap.add_argument("--file", help="file with one URL per line (# comments allowed)")
    ap.add_argument("--label", default="manual-urls", help="source_export label for provenance")
    ap.add_argument("--no-render", action="store_true", help="skip vault rebuild (caller does it)")
    args = ap.parse_args()

    urls = list(args.urls)
    if args.file:
        urls += Path(args.file).read_text().splitlines()
    items, skipped = build_url_items(urls, read_json(INSPIRATION_JSON), load_ledger(LEDGER))
    for u, why in skipped:
        print(f"SKIP {u} — {why}")
    if not items:
        print("NO_NEW_URLS")
        return 0

    have_lock = os.environ.get("NEOUD_HAVE_LOCK") == "1"
    if not have_lock:
        try:
            os.mkdir(LOCKDIR)
        except FileExistsError:
            print("another run in progress — try again shortly")
            return 1
    try:
        for i in range(0, len(items), CHUNK):
            chunk = items[i:i + CHUNK]
            write_json_atomic(INBOX / "new-items.json",
                              {"source_export": args.label, "items": chunk})
            print(f"URL_ITEMS {len(chunk)} of {len(items)} ({args.label})", flush=True)
            r = subprocess.run(["bash", "tools/ingest/enrich.sh"], cwd=str(REPO), timeout=2700)
            if r.returncode != 0:
                print("enrich failed (rate limit?) — rerun to resume")
                return 1
            subprocess.run([".venv/bin/python", "-m", "tools.ingest.apply_enriched"],
                           cwd=str(REPO), check=True)
        if not args.no_render:
            subprocess.run([".venv/bin/python", "-m", "tools.ingest.render_vault"],
                           cwd=str(REPO), check=True)
        print(f"URL_INGEST_COMPLETE {len(items)}")
        return 0
    finally:
        if not have_lock:
            try:
                os.rmdir(LOCKDIR)
            except OSError:
                pass


if __name__ == "__main__":
    raise SystemExit(main())
