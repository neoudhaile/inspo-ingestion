from tools.ingest.add_urls import build_url_items, normalize, url_id


DOC = {"site_designs": {"_schema": {}, "torn.com": {"url": "https://torn.com"}}}
LEDGER = {"processed_ids": [url_id("https://seen.com/page")], "by_id": {}}


def test_normalize_adds_scheme_and_skips_comments():
    assert normalize("example.com") == "https://example.com"
    assert normalize("# a comment") is None
    assert normalize("   ") is None


def test_build_url_items_shape_and_dedup():
    items, skipped = build_url_items(
        ["https://vivekhaldar.com/ideaverse/chord.html",   # new
         "https://torn.com/anything",                      # domain already torn down
         "https://seen.com/page",                          # id already in ledger
         "https://vivekhaldar.com/ideaverse/chord.html"],  # duplicate in same batch
        DOC, LEDGER)
    assert len(items) == 1 and len(skipped) == 2
    it = items[0]
    assert it["id"].startswith("url-") and it["source"] == "manual-url"
    assert it["primary_candidates"] == ["https://vivekhaldar.com/ideaverse/chord.html"]
    assert it["tweet"] is None and it["media"] == []
    reasons = {u: why for u, why in skipped}
    assert "already ingested" in reasons["https://seen.com/page"]
    assert "torn.com" in reasons["https://torn.com/anything"]


def test_url_id_is_stable():
    assert url_id("https://a.com") == url_id("https://a.com")
    assert url_id("https://a.com") != url_id("https://b.com")
