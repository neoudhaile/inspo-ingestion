import argparse
from pathlib import Path
from datetime import datetime
from .config import INSPIRATION_JSON, INSPIRATION_MD, LEDGER, INBOX
from .jsonio import read_json, write_json_atomic
from .ledger import load_ledger, record_ingested
from .writers import merge_items, merge_site_designs
from .render_md import render_region_body, splice_region

def apply(enriched, inspiration_path, md_path, ledger_path, ingested_at):
    doc = read_json(inspiration_path)
    src = enriched.get("source_export", "unknown")
    new_items = enriched.get("items", [])
    merge_items(doc, new_items, src, ingested_at)
    merge_site_designs(doc, enriched.get("site_designs"))
    write_json_atomic(inspiration_path, doc)

    md_text = Path(md_path).read_text()
    region = render_region_body(doc["items"])
    Path(md_path).write_text(splice_region(md_text, region))

    ledger = load_ledger(ledger_path)
    record_ingested(ledger, [i["id"] for i in new_items], src, ingested_at)
    write_json_atomic(ledger_path, ledger)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--enriched", default=str(INBOX / "enriched-items.json"))
    args = ap.parse_args()
    enriched = read_json(args.enriched)
    apply(enriched, INSPIRATION_JSON, INSPIRATION_MD, LEDGER, datetime.now().isoformat(timespec="seconds"))
    print(f"APPLIED {len(enriched.get('items', []))}")

if __name__ == "__main__":
    raise SystemExit(main())
