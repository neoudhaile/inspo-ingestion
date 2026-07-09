import json
from pathlib import Path

def load_ledger(path):
    p = Path(path)
    if not p.exists():
        return {"processed_ids": [], "by_id": {}}
    return json.loads(p.read_text())

def unprocessed_ids(ledger, ids):
    known = set(ledger.get("processed_ids", []))
    return [i for i in ids if i not in known]

def record_ingested(ledger, ids, source_export, ingested_at):
    for i in ids:
        if i not in ledger["processed_ids"]:
            ledger["processed_ids"].append(i)
        ledger["by_id"][i] = {"source_export": source_export, "ingested_at": ingested_at}
    return ledger
