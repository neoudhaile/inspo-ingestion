from tools.ingest.writers import merge_items, merge_site_designs


def test_merge_items_appends_with_provenance():
    doc = {"items": [{"id": "1"}], "site_designs": {}}
    enriched = [{"id": "2", "title": "X", "primary_domain": "x.com"}]
    merge_items(doc, enriched, "export.json", "2026-06-04T10:00:00")
    ids = [i["id"] for i in doc["items"]]
    assert ids == ["1", "2"]
    new = doc["items"][-1]
    assert new["source_export"] == "export.json"
    assert new["ingested_at"] == "2026-06-04T10:00:00"


def test_merge_items_skips_existing_id():
    doc = {"items": [{"id": "1"}], "site_designs": {}}
    merge_items(doc, [{"id": "1", "title": "dup"}], "e.json", "t")
    assert len(doc["items"]) == 1


def test_merge_site_designs_skips_existing_domain():
    doc = {"items": [], "site_designs": {"x.com": {"keep": True}}}
    merge_site_designs(doc, {"x.com": {"keep": False}, "y.com": {"new": True}})
    assert doc["site_designs"]["x.com"] == {"keep": True}
    assert doc["site_designs"]["y.com"] == {"new": True}
