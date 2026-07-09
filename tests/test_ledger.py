import json
from tools.ingest.ledger import load_ledger, unprocessed_ids, record_ingested

def test_load_missing_ledger_returns_empty(tmp_path):
    led = load_ledger(tmp_path / "nope.json")
    assert led == {"processed_ids": [], "by_id": {}}

def test_unprocessed_ids_filters_known(tmp_path):
    led = {"processed_ids": ["a"], "by_id": {}}
    assert unprocessed_ids(led, ["a", "b", "c"]) == ["b", "c"]

def test_record_ingested_adds_provenance():
    led = {"processed_ids": [], "by_id": {}}
    record_ingested(led, ["b"], "export.json", "2026-06-04T10:00:00")
    assert "b" in led["processed_ids"]
    assert led["by_id"]["b"] == {"source_export": "export.json", "ingested_at": "2026-06-04T10:00:00"}
