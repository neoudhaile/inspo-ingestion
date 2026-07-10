import argparse, glob, json
from pathlib import Path
from .config import DOWNLOADS, EXPORT_GLOB, LEDGER, INBOX
from .harvest import deep_external_urls, split_primary
from .ledger import load_ledger, unprocessed_ids
from .jsonio import write_json_atomic

def normalize_item(rec):
    urls = deep_external_urls(rec)
    primary, all_urls = split_primary(urls)
    sn = rec.get("screen_name", "")
    return {
        "id": rec["id"],
        "date": (rec.get("created_at") or "")[:10],
        "author": sn,
        "name": rec.get("name"),
        "author_profile": f"https://twitter.com/{sn}" if sn else None,
        "tweet": rec.get("url"),
        "full_text": rec.get("full_text") or "",
        "all_urls": all_urls,
        "primary_candidates": primary,
        "media_kinds": sorted({m.get("type") for m in (rec.get("media") or []) if m.get("type")}),
        "media": [
            {"type": m.get("type"), "original_url": m.get("original"), "thumbnail_url": m.get("thumbnail")}
            for m in (rec.get("media") or [])
            if m.get("original") or m.get("thumbnail")
        ],
    }

def build_new_items(records, ledger, source_export):
    ids = [r["id"] for r in records]
    new = set(unprocessed_ids(ledger, ids))
    items = [normalize_item(r) for r in records if r["id"] in new]
    return {"source_export": source_export, "items": items}

def newest_export(downloads=DOWNLOADS, pattern=EXPORT_GLOB):
    """Newest VALID export. Skips corrupt/empty files (e.g. a failed 2-byte
    download) so a bad newest file can't shadow a good earlier one."""
    matches = sorted(glob.glob(str(Path(downloads) / pattern)),
                     key=lambda p: Path(p).stat().st_mtime, reverse=True)
    for m in matches:
        p = Path(m)
        try:
            data = json.loads(p.read_text())
            if isinstance(data, list) and data:
                return p
        except (ValueError, OSError):
            pass
        print(f"SKIPPING invalid/empty export: {p.name}")
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--export", help="path to export JSON (default: newest in ~/Downloads)")
    ap.add_argument("--out", default=str(INBOX / "new-items.json"))
    ap.add_argument("--limit", type=int, default=0,
                    help="cap the number of new items written this pass (0 = all); "
                         "lets run.sh enrich in resumable chunks")
    args = ap.parse_args()
    export = Path(args.export) if args.export else newest_export()
    if not export:
        print("NO_EXPORT"); return 0
    records = json.loads(export.read_text())
    ledger = load_ledger(LEDGER)
    out = build_new_items(records, ledger, export.name)
    if not out["items"]:
        print("NO_NEW_ITEMS"); return 0
    total = len(out["items"])
    if args.limit and total > args.limit:
        out["items"] = out["items"][:args.limit]
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    write_json_atomic(args.out, out)
    print(f"NEW_ITEMS {len(out['items'])} of {total} {args.out}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
