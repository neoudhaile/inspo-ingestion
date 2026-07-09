import json
from tools.ingest.ingest import normalize_item, build_new_items

def _rec(id, sn, text, expanded):
    return {"id": id, "screen_name": sn, "name": sn.title(),
            "created_at": "2026-06-02 09:00:00 -04:00", "full_text": text,
            "url": f"https://twitter.com/{sn}/status/{id}",
            "media": [{"type": "photo", "original": "https://pbs.twimg.com/media/X?name=orig",
                       "thumbnail": "https://pbs.twimg.com/media/X?name=thumb"}],
            "metadata": {"legacy": {"entities": {"urls": [{"expanded_url": e} for e in expanded]}}}}

def test_normalize_item_shape():
    it = normalize_item(_rec("1", "blurrhaus", "hi https://t.co/x", ["http://blurr.design"]))
    assert it["id"] == "1"
    assert it["author"] == "blurrhaus"
    assert it["date"] == "2026-06-02"
    assert it["author_profile"] == "https://twitter.com/blurrhaus"
    assert it["all_urls"] == ["http://blurr.design"]
    assert it["primary_candidates"] == ["http://blurr.design"]
    assert it["media_kinds"] == ["photo"]
    assert it["media"] == [{"type": "photo",
                            "original_url": "https://pbs.twimg.com/media/X?name=orig",
                            "thumbnail_url": "https://pbs.twimg.com/media/X?name=thumb"}]

def test_normalize_item_no_media():
    it = normalize_item(_rec("1", "a", "", []))
    # _rec always has media; verify a record with no media yields empty list
    rec = {"id": "2", "screen_name": "a", "created_at": "2026-06-02 00:00:00 -04:00",
           "url": "https://twitter.com/a/status/2", "full_text": "", "metadata": {}}
    assert normalize_item(rec)["media"] == []

def test_build_new_items_only_unprocessed():
    recs = [_rec("1","a","",[]), _rec("2","b","",["http://b.com"])]
    ledger = {"processed_ids": ["1"], "by_id": {}}
    out = build_new_items(recs, ledger, "export.json")
    assert out["source_export"] == "export.json"
    assert [i["id"] for i in out["items"]] == ["2"]
