import argparse
from pathlib import Path
from datetime import datetime
from .config import INSPIRATION_JSON, INSPIRATION_MD, LEDGER, INBOX
from .jsonio import read_json, write_json_atomic
from .ledger import load_ledger, record_ingested
from .writers import merge_items, merge_site_designs
from .essence import check_site_design
from .render_md import render_region_body, splice_region

def apply(enriched, inspiration_path, md_path, ledger_path, ingested_at):
    doc = read_json(inspiration_path)
    src = enriched.get("source_export", "unknown")
    new_items = enriched.get("items", [])
    merge_items(doc, new_items, src, ingested_at)
    # Validate each new teardown's essence before it lands. Never fails the run: an
    # invalid essence is dropped and marked, and `essence --backfill` repairs it.
    statuses = {dom: check_site_design(payload)
                for dom, payload in (enriched.get("site_designs") or {}).items()}
    merge_site_designs(doc, enriched.get("site_designs"))
    write_json_atomic(inspiration_path, doc)

    md_text = Path(md_path).read_text()
    region = render_region_body(doc["items"])
    Path(md_path).write_text(splice_region(md_text, region))

    ledger = load_ledger(ledger_path)
    record_ingested(ledger, [i["id"] for i in new_items], src, ingested_at)
    write_json_atomic(ledger_path, ledger)
    return statuses

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--enriched", default=str(INBOX / "enriched-items.json"))
    args = ap.parse_args()
    enriched = read_json(args.enriched)
    statuses = apply(enriched, INSPIRATION_JSON, INSPIRATION_MD, LEDGER,
                     datetime.now().isoformat(timespec="seconds"))
    print(f"APPLIED {len(enriched.get('items', []))}")
    bad = {d: s for d, s in statuses.items() if s != "ok"}
    if bad:
        print(f"ESSENCE_NEEDS_BACKFILL {len(bad)}: "
              + ", ".join(f"{d} ({s})" for d, s in sorted(bad.items())))

if __name__ == "__main__":
    raise SystemExit(main())
