import json, shutil
from pathlib import Path
from tools.ingest.apply_enriched import apply

def test_apply_merges_and_updates_ledger(tmp_path):
    inspiration = tmp_path / "inspiration.json"
    md = tmp_path / "inspiration.md"
    ledger = tmp_path / "_ledger.json"
    inspiration.write_text(json.dumps({"items": [{"id": "0"}], "site_designs": {}}))
    md.write_text("# Inspiration\n\nbody\n")
    enriched = {"source_export": "e.json", "items": [
        {"id": "9", "title": "T", "author": "a", "author_profile": "p", "tweet": "tw",
         "date": "2026-06-02", "category": "design", "tags": ["design"],
         "primary_url": "http://x.com", "primary_domain": "x.com",
         "related_urls": [], "all_urls": ["http://x.com"], "text": "hi", "source": "bookmarks-export",
         "teardown_domains": []}],
        "site_designs": {"x.com": {"url": "https://x.com"}}}
    apply(enriched, inspiration, md, ledger, "2026-06-04T10:00:00")
    doc = json.loads(inspiration.read_text())
    assert [i["id"] for i in doc["items"]] == ["0", "9"]
    assert "x.com" in doc["site_designs"]
    assert "9" in json.loads(ledger.read_text())["processed_ids"]
    assert "AUTO-INGEST:START" in md.read_text()
    assert md.read_text().startswith("# Inspiration")
