import json, pytest
from tools.ingest.jsonio import write_json_atomic, read_json

def test_roundtrip(tmp_path):
    p = tmp_path / "x.json"
    write_json_atomic(p, {"a": 1})
    assert read_json(p) == {"a": 1}

def test_atomic_write_does_not_leave_tmp(tmp_path):
    p = tmp_path / "x.json"
    write_json_atomic(p, {"a": 1})
    assert list(tmp_path.glob("*.tmp")) == []
