import json, os
from pathlib import Path

def read_json(path):
    return json.loads(Path(path).read_text())

def write_json_atomic(path, data):
    """Serialize, validate it parses, then atomically replace the target."""
    path = Path(path)
    text = json.dumps(data, indent=2, ensure_ascii=False)
    json.loads(text)  # guard: never write unparseable JSON
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text)
    os.replace(tmp, path)
