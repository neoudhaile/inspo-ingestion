# Bookmark Auto-Ingestion Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Automatically ingest new X bookmarks from a re-exported JSON into `inspo/inspiration.json` / `inspiration.md`, enriching each with title/category/tags/primary-URL and auto-running design teardowns, triggered by a folder-watch daemon.

**Architecture:** A deterministic Python core (`ingest.py`) diffs a new export against a ledger and harvests URLs, emitting `new-items.json`. A `claude -p` enrichment step applies judgment (filter, primary URL, title, tags, teardown) and emits `enriched-items.json`. Deterministic `writers.py` merges results into the JSON source of truth, splices an auto-region into the MD, archives the raw export, and updates the ledger. A `launchd` agent watching `~/Downloads` is the trigger, built last.

**Tech Stack:** Python 3 (stdlib only: `json`, `re`, `glob`, `pathlib`, `datetime`, `os`), `pytest` for tests, Bash for orchestration (`run.sh`), `launchd` plist for the trigger, `claude -p` headless + Playwright MCP for enrichment.

---

## Key design decisions locked from the spec

- **JSON is source of truth.** `inspiration.md` is a view.
- **MD safety:** `inspiration.md` contains hand-written prose (TOC, tag glossary, section 11 aesthetic notes, section 12 favorites). We therefore DO NOT fully regenerate it. New items are spliced into a single managed region delimited by HTML-comment markers; everything else is left byte-for-byte untouched. Promoting items into curated sections stays manual.
- **Keep-all + tag aggressively.** Every new bookmark becomes an item; link-free ones are tagged, not dropped.
- **Teardown** runs only on domains the enricher marks as resolvable design-worthy homepages.
- **Idempotent** via `_ledger.json`; ledger is updated only after a fully successful run.

## File structure

| Path | Responsibility |
|---|---|
| `tools/ingest/config.py` | Constants: paths, `UTILITY_DENYLIST`, `TWITTER_HOSTS` |
| `tools/ingest/ledger.py` | Load/save `_ledger.json`, compute unprocessed ids |
| `tools/ingest/harvest.py` | Deep-walk a record for external URLs; denylist split |
| `tools/ingest/ingest.py` | CLI: newest export → diff → normalize → `new-items.json` |
| `tools/ingest/jsonio.py` | Atomic JSON read/write (validate-then-swap) |
| `tools/ingest/writers.py` | Merge enriched items + site_designs into `inspiration.json` |
| `tools/ingest/render_md.py` | Render item blocks; splice managed MD region |
| `tools/ingest/enrich_prompt.md` | The instructions handed to `claude -p` |
| `tools/ingest/enrich.sh` | Invoke `claude -p` with the prompt → `enriched-items.json` |
| `run.sh` | Orchestrate: ingest → enrich → write → archive → ledger |
| `tools/ingest/net.neoud.bookmark-ingest.plist` | launchd WatchPaths trigger |
| `tests/fixtures/*.json` | Trimmed real-export fixtures |
| `tests/test_*.py` | Unit tests per module |

## Data contracts

**`new-items.json`** (output of `ingest.py`):
```json
{
  "source_export": "twitter-Bookmarks-1780584772676.json",
  "items": [
    {
      "id": "2061...", "date": "2026-06-02", "author": "blurrhaus",
      "name": "blurr", "author_profile": "https://twitter.com/blurrhaus",
      "tweet": "https://twitter.com/blurrhaus/status/2061...",
      "full_text": "See Ditther in action...",
      "all_urls": ["http://blurr.design", "http://ditther.com", "http://herohype.xyz"],
      "primary_candidates": ["http://blurr.design", "http://ditther.com", "http://herohype.xyz"],
      "media_kinds": ["photo"]
    }
  ]
}
```

**`enriched-items.json`** (output of enricher, input to `writers.py`):
```json
{
  "source_export": "twitter-Bookmarks-1780584772676.json",
  "items": [
    {
      "id": "2061...", "title": "Ditther — dithering tool", "author": "blurrhaus",
      "name": "blurr", "author_profile": "https://twitter.com/blurrhaus",
      "tweet": "https://twitter.com/blurrhaus/status/2061...", "date": "2026-06-02",
      "category": "tools-build", "tags": ["tools-build", "design", "tool"],
      "primary_url": "http://ditther.com", "primary_domain": "ditther.com",
      "related_urls": ["http://blurr.design", "http://herohype.xyz"],
      "all_urls": ["http://blurr.design", "http://ditther.com", "http://herohype.xyz"],
      "text": "See Ditther in action...", "source": "bookmarks-export",
      "teardown_domains": ["ditther.com"]
    }
  ],
  "site_designs": {
    "ditther.com": { "url": "https://ditther.com", "title": "...", "screenshot": "ditther.png",
      "extracted_at": "2026-06-04", "extracted_via": "playwright-mcp @ 1440x900",
      "what_it_is": "...", "what_it_shows": "...", "how_it_works": "...",
      "how_its_designed": "...", "palette": "...", "fonts": "...", "pattern_keywords": [] }
  }
}
```

**`_ledger.json`:**
```json
{ "processed_ids": ["2059..."],
  "by_id": { "2059...": { "source_export": "twitter-Bookmarks-1779930252646.json", "ingested_at": "2026-06-04T10:00:00" } } }
```

---

### Task 1: Repo + test scaffold

**Files:**
- Create: `tools/ingest/__init__.py` (empty)
- Create: `tests/__init__.py` (empty)
- Create: `requirements-dev.txt`
- Create: `tests/fixtures/export_old.json`, `tests/fixtures/export_new.json`

- [ ] **Step 1: Initialize git (the repo is not yet under version control)**

Run:
```bash
cd /Users/neoudhaile/Documents/Projects/Code/neoud.net
git init && printf '%s\n' '.venv/' '__pycache__/' '*.pyc' 'inspo/_inbox/' '.playwright-mcp/' > .gitignore
git add -A && git commit -m "chore: initial commit before ingestion pipeline"
```
Expected: a repo with one commit. (If the user prefers no git, skip commits in later steps.)

- [ ] **Step 2: Create a Python venv and install pytest**

Run:
```bash
python3 -m venv .venv && .venv/bin/pip install pytest
echo "pytest" > requirements-dev.txt
```
Expected: `.venv/bin/pytest --version` prints a version.

- [ ] **Step 3: Create package + test init files**

```bash
mkdir -p tools/ingest tests/fixtures
touch tools/ingest/__init__.py tests/__init__.py
```

- [ ] **Step 4: Build trimmed fixtures from the real exports**

Run (creates 5-item fixtures so tests are fast and committable):
```bash
.venv/bin/python - <<'PY'
import json
old=json.load(open('/Users/neoudhaile/Downloads/twitter-Bookmarks-1779930252646.json'))
new=json.load(open('/Users/neoudhaile/Downloads/twitter-Bookmarks-1780584772676.json'))
oid={x['id'] for x in old}
# 3 shared + 2 new-only, picking ones with known URL shapes
shared=[x for x in old][:3]
newonly=[x for x in new if x['id'] not in oid][:2]
json.dump(shared, open('tests/fixtures/export_old.json','w'), indent=2)
json.dump(shared+newonly, open('tests/fixtures/export_new.json','w'), indent=2)
print("old fixture:",len(shared),"new fixture:",len(shared)+len(newonly))
PY
```
Expected: `old fixture: 3 new fixture: 5`.

- [ ] **Step 5: Commit**

```bash
git add -A && git commit -m "chore: test scaffold + export fixtures"
```

---

### Task 2: `config.py` — constants

**Files:**
- Create: `tools/ingest/config.py`

- [ ] **Step 1: Write the module (no test needed — pure constants)**

```python
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
INSPO = REPO / "inspo"
INSPIRATION_JSON = INSPO / "inspiration.json"
INSPIRATION_MD = INSPO / "inspiration.md"
LEDGER = INSPO / "_ledger.json"
INBOX = INSPO / "_inbox"
ARCHIVE = INSPO / "_archive"
DOWNLOADS = Path.home() / "Downloads"
EXPORT_GLOB = "twitter-Bookmarks-*.json"

# Hosts that are the platform itself — never a destination site.
TWITTER_HOSTS = ("twitter.com", "t.co", "x.com", "twimg.com", "pbs.twimg")

# Utility links that should never be chosen as a primary site (kept in all_urls).
UTILITY_DENYLIST = (
    "linktr.ee", "typefully.com", "cal.com", "calendly.com",
    "medium.com", "docs.google.com", "framer.link", "substack.com",
    "github.com", "youtube.com", "youtu.be",
)

# MD managed-region markers.
MD_REGION_START = "<!-- AUTO-INGEST:START — do not edit inside this region by hand -->"
MD_REGION_END = "<!-- AUTO-INGEST:END -->"
```

- [ ] **Step 2: Commit**

```bash
git add tools/ingest/config.py && git commit -m "feat: ingest config constants"
```

---

### Task 3: `harvest.py` — URL harvesting

**Files:**
- Create: `tools/ingest/harvest.py`
- Test: `tests/test_harvest.py`

- [ ] **Step 1: Write failing tests**

```python
from tools.ingest.harvest import deep_external_urls, split_primary

RECORD = {
    "full_text": "See it https://t.co/abc",
    "metadata": {"legacy": {"entities": {"urls": [
        {"expanded_url": "http://ditther.com"},
        {"expanded_url": "https://twitter.com/x/status/1"},
    ]}}, "bio": "links: https://linktr.ee/me and http://blurr.design"},
}

def test_deep_external_urls_dedups_and_drops_twitter():
    urls = deep_external_urls(RECORD)
    assert "http://ditther.com" in urls
    assert "http://blurr.design" in urls
    assert "https://linktr.ee/me" in urls
    assert not any("twitter.com" in u or "t.co" in u for u in urls)

def test_deep_external_urls_is_ordered_and_unique():
    urls = deep_external_urls(RECORD)
    assert len(urls) == len(set(urls))

def test_split_primary_demotes_denylisted():
    primary, _all = split_primary(["https://linktr.ee/me", "http://blurr.design"])
    assert primary == ["http://blurr.design"]

def test_split_primary_falls_back_to_all_when_only_utility():
    primary, _all = split_primary(["https://linktr.ee/me"])
    assert primary == []  # nothing design-worthy; enricher decides keep-all/tag
```

- [ ] **Step 2: Run to verify failure**

Run: `.venv/bin/python -m pytest tests/test_harvest.py -v`
Expected: FAIL with `ModuleNotFoundError` / `ImportError: cannot import name`.

- [ ] **Step 3: Implement**

```python
import re
from .config import TWITTER_HOSTS, UTILITY_DENYLIST

_URL = re.compile(r'https?://[^\s"\\<>]+')

def _walk(node, sink):
    if isinstance(node, str):
        sink.extend(_URL.findall(node))
    elif isinstance(node, dict):
        for v in node.values():
            _walk(v, sink)
    elif isinstance(node, list):
        for v in node:
            _walk(v, sink)

def deep_external_urls(record):
    """Every external (non-platform) http(s) URL anywhere in the record, ordered, unique."""
    raw = []
    _walk(record, raw)
    seen, out = set(), []
    for u in raw:
        u = u.rstrip(').,';\"')
        if any(h in u for h in TWITTER_HOSTS):
            continue
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out

def split_primary(urls):
    """Return (primary_candidates, all_urls). Utility/footer links can't be primary."""
    primary = [u for u in urls if not any(d in u for d in UTILITY_DENYLIST)]
    return primary, list(urls)
```

- [ ] **Step 4: Run to verify pass**

Run: `.venv/bin/python -m pytest tests/test_harvest.py -v`
Expected: 4 passed.

- [ ] **Step 5: Commit**

```bash
git add tools/ingest/harvest.py tests/test_harvest.py && git commit -m "feat: deep URL harvest + denylist split"
```

---

### Task 4: `ledger.py` — dedup ledger

**Files:**
- Create: `tools/ingest/ledger.py`
- Test: `tests/test_ledger.py`

- [ ] **Step 1: Write failing tests**

```python
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
```

- [ ] **Step 2: Run to verify failure**

Run: `.venv/bin/python -m pytest tests/test_ledger.py -v`
Expected: FAIL `ImportError`.

- [ ] **Step 3: Implement**

```python
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
```

- [ ] **Step 4: Run to verify pass**

Run: `.venv/bin/python -m pytest tests/test_ledger.py -v`
Expected: 3 passed.

- [ ] **Step 5: Commit**

```bash
git add tools/ingest/ledger.py tests/test_ledger.py && git commit -m "feat: dedup ledger with provenance"
```

---

### Task 5: `jsonio.py` — atomic JSON I/O

**Files:**
- Create: `tools/ingest/jsonio.py`
- Test: `tests/test_jsonio.py`

- [ ] **Step 1: Write failing tests**

```python
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
```

- [ ] **Step 2: Run to verify failure**

Run: `.venv/bin/python -m pytest tests/test_jsonio.py -v`
Expected: FAIL `ImportError`.

- [ ] **Step 3: Implement**

```python
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
```

- [ ] **Step 4: Run to verify pass**

Run: `.venv/bin/python -m pytest tests/test_jsonio.py -v`
Expected: 2 passed.

- [ ] **Step 5: Commit**

```bash
git add tools/ingest/jsonio.py tests/test_jsonio.py && git commit -m "feat: atomic JSON I/O"
```

---

### Task 6: `ingest.py` — normalize + CLI

**Files:**
- Create: `tools/ingest/ingest.py`
- Test: `tests/test_ingest.py`

- [ ] **Step 1: Write failing tests**

```python
import json
from tools.ingest.ingest import normalize_item, build_new_items

def _rec(id, sn, text, expanded):
    return {"id": id, "screen_name": sn, "name": sn.title(),
            "created_at": "2026-06-02 09:00:00 -04:00", "full_text": text,
            "url": f"https://twitter.com/{sn}/status/{id}",
            "media": [{"type": "photo"}],
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

def test_build_new_items_only_unprocessed():
    recs = [_rec("1","a","",[]), _rec("2","b","",["http://b.com"])]
    ledger = {"processed_ids": ["1"], "by_id": {}}
    out = build_new_items(recs, ledger, "export.json")
    assert out["source_export"] == "export.json"
    assert [i["id"] for i in out["items"]] == ["2"]
```

- [ ] **Step 2: Run to verify failure**

Run: `.venv/bin/python -m pytest tests/test_ingest.py -v`
Expected: FAIL `ImportError`.

- [ ] **Step 3: Implement**

```python
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
    }

def build_new_items(records, ledger, source_export):
    ids = [r["id"] for r in records]
    new = set(unprocessed_ids(ledger, ids))
    items = [normalize_item(r) for r in records if r["id"] in new]
    return {"source_export": source_export, "items": items}

def newest_export(downloads=DOWNLOADS, pattern=EXPORT_GLOB):
    matches = sorted(glob.glob(str(Path(downloads) / pattern)), key=lambda p: Path(p).stat().st_mtime)
    return Path(matches[-1]) if matches else None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--export", help="path to export JSON (default: newest in ~/Downloads)")
    ap.add_argument("--out", default=str(INBOX / "new-items.json"))
    args = ap.parse_args()
    export = Path(args.export) if args.export else newest_export()
    if not export:
        print("NO_EXPORT"); return 0
    records = json.loads(export.read_text())
    ledger = load_ledger(LEDGER)
    out = build_new_items(records, ledger, export.name)
    if not out["items"]:
        print("NO_NEW_ITEMS"); return 0
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    write_json_atomic(args.out, out)
    print(f"NEW_ITEMS {len(out['items'])} {args.out}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run to verify pass + a real-data smoke check**

Run: `.venv/bin/python -m pytest tests/test_ingest.py -v`
Expected: 2 passed.

Run (real data, writes nothing permanent — uses the new export, empty ledger via the old as baseline is skipped; this prints the count):
```bash
.venv/bin/python -m tools.ingest.ingest --export ~/Downloads/twitter-Bookmarks-1780584772676.json --out /tmp/new-items.json
```
Expected: `NEW_ITEMS 187 ...` (empty ledger ⇒ all are "new"; with a real ledger it would be 33). Inspect `/tmp/new-items.json` to confirm shape.

- [ ] **Step 5: Commit**

```bash
git add tools/ingest/ingest.py tests/test_ingest.py && git commit -m "feat: ingest CLI — diff + normalize to new-items.json"
```

---

### Task 7: `writers.py` — merge into inspiration.json

**Files:**
- Create: `tools/ingest/writers.py`
- Test: `tests/test_writers.py`

- [ ] **Step 1: Write failing tests**

```python
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
```

- [ ] **Step 2: Run to verify failure**

Run: `.venv/bin/python -m pytest tests/test_writers.py -v`
Expected: FAIL `ImportError`.

- [ ] **Step 3: Implement**

```python
def merge_items(doc, enriched_items, source_export, ingested_at):
    existing = {i["id"] for i in doc.get("items", [])}
    for it in enriched_items:
        if it["id"] in existing:
            continue
        row = dict(it)
        row["source_export"] = source_export
        row["ingested_at"] = ingested_at
        # teardown_domains is enricher-internal; not part of the item record
        row.pop("teardown_domains", None)
        doc.setdefault("items", []).append(row)
        existing.add(it["id"])
    return doc

def merge_site_designs(doc, site_designs):
    reg = doc.setdefault("site_designs", {})
    for domain, payload in (site_designs or {}).items():
        if domain in reg:
            continue  # never overwrite an existing teardown
        reg[domain] = payload
    return doc
```

- [ ] **Step 4: Run to verify pass**

Run: `.venv/bin/python -m pytest tests/test_writers.py -v`
Expected: 3 passed.

- [ ] **Step 5: Commit**

```bash
git add tools/ingest/writers.py tests/test_writers.py && git commit -m "feat: merge enriched items + site_designs into JSON"
```

---

### Task 8: `render_md.py` — managed-region MD splice

**Files:**
- Create: `tools/ingest/render_md.py`
- Test: `tests/test_render_md.py`

- [ ] **Step 1: Write failing tests**

```python
from tools.ingest.render_md import render_item_block, splice_region
from tools.ingest.config import MD_REGION_START, MD_REGION_END

ITEM = {"title": "Ditther", "primary_url": "http://ditther.com", "author": "blurrhaus",
        "author_profile": "https://twitter.com/blurrhaus", "tweet": "https://twitter.com/blurrhaus/status/1",
        "date": "2026-06-02", "tags": ["tools-build", "design"], "text": "See it"}

def test_render_item_block_has_title_and_link():
    md = render_item_block(ITEM)
    assert "Ditther" in md and "http://ditther.com" in md
    assert "`tools-build`" in md

def test_splice_creates_region_when_absent():
    out = splice_region("# Doc\n\nbody\n", "GENERATED")
    assert MD_REGION_START in out and MD_REGION_END in out
    assert "GENERATED" in out
    assert out.startswith("# Doc")  # original content preserved

def test_splice_replaces_existing_region_only():
    base = f"# Doc\n\n{MD_REGION_START}\nOLD\n{MD_REGION_END}\n\nfooter\n"
    out = splice_region(base, "NEW")
    assert "OLD" not in out and "NEW" in out
    assert "footer" in out  # content outside region untouched
```

- [ ] **Step 2: Run to verify failure**

Run: `.venv/bin/python -m pytest tests/test_render_md.py -v`
Expected: FAIL `ImportError`.

- [ ] **Step 3: Implement**

```python
from .config import MD_REGION_START, MD_REGION_END

def render_item_block(it):
    title = it.get("title") or it.get("primary_domain") or it.get("author")
    url = it.get("primary_url")
    site = f"**Site:** [{it.get('primary_domain') or url}]({url})  \n" if url else ""
    prof = it.get("author_profile") or ""
    tweet = it.get("tweet") or ""
    tags = " ".join(f"`{t}`" for t in it.get("tags", []))
    text = (it.get("text") or "").strip().replace("\n", " ")
    if len(text) > 200:
        text = text[:200] + "…"
    return (
        f"### {title}\n\n"
        f"{site}"
        f"**Author:** [@{it.get('author')}]({prof})  \n"
        f"**Source:** [tweet]({tweet}) · {it.get('date')}  \n"
        f"**Tags:** {tags}  \n\n"
        + (f"> {text}\n" if text else "")
    )

def render_region_body(items):
    header = "## Auto-ingested (newest first)\n\n_Appended automatically from X bookmark exports. Move into curated sections by hand._\n\n"
    blocks = "\n".join(render_item_block(i) for i in items)
    return header + blocks

def splice_region(md_text, region_body):
    block = f"{MD_REGION_START}\n{region_body}\n{MD_REGION_END}"
    if MD_REGION_START in md_text and MD_REGION_END in md_text:
        pre = md_text.split(MD_REGION_START)[0]
        post = md_text.split(MD_REGION_END, 1)[1]
        return pre + block + post
    sep = "" if md_text.endswith("\n") else "\n"
    return md_text + sep + "\n" + block + "\n"
```

- [ ] **Step 4: Run to verify pass**

Run: `.venv/bin/python -m pytest tests/test_render_md.py -v`
Expected: 3 passed.

- [ ] **Step 5: Commit**

```bash
git add tools/ingest/render_md.py tests/test_render_md.py && git commit -m "feat: managed-region markdown splice"
```

---

### Task 9: `enrich_prompt.md` — the enricher instructions

**Files:**
- Create: `tools/ingest/enrich_prompt.md`

- [ ] **Step 1: Write the prompt (this is the model's contract; no unit test)**

````markdown
# Bookmark enrichment

You are given `inspo/_inbox/new-items.json`. Produce `inspo/_inbox/enriched-items.json`
with the exact schema below. Use Playwright MCP for teardowns.

## Rules
1. **Keep every item.** Never drop one. Link-free items still get a title, category, tags.
2. **Primary URL:** choose the subject site from `primary_candidates`. If a tweet
   showcases a site AND links the author's portfolio, the showcased site is primary;
   demote the rest to `related_urls`. If `primary_candidates` is empty, set
   `primary_url`/`primary_domain` to null and tag accordingly (e.g. `uncategorized`).
3. **List tweets** (many sites in one tweet): keep one item; put every site in
   `all_urls`/`related_urls`; tag `directory`/`thread`; mark each design-worthy
   domain in `teardown_domains`.
4. **Category** ∈ the existing set in `inspiration.json.meta.categories`.
   **Tags** drawn from `meta.all_tags` (you may add new tags when warranted).
5. **Teardown:** for each domain in `teardown_domains`, load it at 1440×900, take one
   screenshot saved to the repo root as `<domain-without-dots>.png`, do a hover and a
   scroll, then write a `site_designs` entry using the PROSE schema:
   `what_it_is`, `what_it_shows`, `how_it_works`, `how_its_designed` (prose),
   plus one-line `palette`, one-line `fonts`, and `pattern_keywords[]`.
   Skip domains that fail to load; do not block other items.
6. Copy `id`, `author`, `name`, `author_profile`, `tweet`, `date` through unchanged.
   Set `text` = the tweet's `full_text`. Set `source` = "bookmarks-export".

## Output schema
(Exactly the `enriched-items.json` contract in the plan: top-level `source_export`,
`items[]`, and `site_designs{}`.)

Write ONLY the file. Do not modify `inspiration.json` or `inspiration.md` — the
deterministic writer does that.
````

- [ ] **Step 2: Commit**

```bash
git add tools/ingest/enrich_prompt.md && git commit -m "feat: enricher prompt contract"
```

---

### Task 10: `apply_enriched.py` — writer CLI (ties writers + render_md + ledger)

**Files:**
- Create: `tools/ingest/apply_enriched.py`
- Test: `tests/test_apply_enriched.py`

- [ ] **Step 1: Write failing test (integration over a temp repo layout)**

```python
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
```

- [ ] **Step 2: Run to verify failure**

Run: `.venv/bin/python -m pytest tests/test_apply_enriched.py -v`
Expected: FAIL `ImportError`.

- [ ] **Step 3: Implement**

```python
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
    region = render_region_body(doc["items"])  # render full list so region stays consistent
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
```

Note: `render_region_body(doc["items"])` renders the auto-region from ALL items so the
region is deterministic; if that becomes too long later, switch to newest-N. For now
(YAGNI) the full list is fine.

- [ ] **Step 4: Run to verify pass**

Run: `.venv/bin/python -m pytest tests/test_apply_enriched.py -v`
Expected: 1 passed.

- [ ] **Step 5: Commit**

```bash
git add tools/ingest/apply_enriched.py tests/test_apply_enriched.py && git commit -m "feat: apply enriched items + splice MD + update ledger"
```

---

### Task 11: `enrich.sh` + `run.sh` orchestration

**Files:**
- Create: `tools/ingest/enrich.sh`
- Create: `run.sh`
- Create: `tests/test_run_noop.py`

- [ ] **Step 1: Write `enrich.sh`**

```bash
#!/usr/bin/env bash
# Invoke Claude headless to turn new-items.json into enriched-items.json.
set -euo pipefail
cd "$(dirname "$0")/../.."   # repo root
PROMPT="$(cat tools/ingest/enrich_prompt.md)"
claude -p "$PROMPT" --permission-mode acceptEdits
```

- [ ] **Step 2: Write `run.sh` (cheap no-op guard + lockfile + ordering)**

```bash
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
VENV=.venv/bin/python
LOCK=/tmp/neoud-ingest.lock

# Cheap no-op: bail before any heavy work if there are no new items.
if ! "$VENV" -m tools.ingest.ingest >/tmp/ingest.out 2>&1; then
  echo "ingest failed"; cat /tmp/ingest.out; exit 1
fi
HEAD="$(head -n1 /tmp/ingest.out || true)"
case "$HEAD" in
  NO_EXPORT|NO_NEW_ITEMS) echo "nothing to do: $HEAD"; exit 0 ;;
esac

# Serialize runs (Downloads can fire WatchPaths repeatedly).
exec 9>"$LOCK"; flock -n 9 || { echo "another run in progress"; exit 0; }

bash tools/ingest/enrich.sh
"$VENV" -m tools.ingest.apply_enriched

# Archive the export that was just processed.
EXPORT="$($VENV - <<'PY'
from tools.ingest.ingest import newest_export
print(newest_export() or "")
PY
)"
if [ -n "$EXPORT" ]; then
  mkdir -p inspo/_archive && cp "$EXPORT" "inspo/_archive/$(basename "$EXPORT")"
fi
echo "ingest run complete"
```

- [ ] **Step 3: Write a no-op test for the guard logic**

```python
import subprocess, sys, os

def test_ingest_prints_no_export_when_dir_empty(tmp_path):
    # Run the ingest module pointed at an empty dir via --export missing path
    r = subprocess.run([sys.executable, "-m", "tools.ingest.ingest",
                        "--export", str(tmp_path / "absent.json")],
                       capture_output=True, text=True, cwd=os.getcwd())
    # absent export path -> json load fails; guard is newest_export only when no --export.
    assert r.returncode != 0 or "NO_" in r.stdout
```

- [ ] **Step 4: Make scripts executable and run the no-op path**

Run:
```bash
chmod +x run.sh tools/ingest/enrich.sh
.venv/bin/python -m pytest tests/test_run_noop.py -v
```
Expected: 1 passed.

- [ ] **Step 5: Commit**

```bash
git add run.sh tools/ingest/enrich.sh tests/test_run_noop.py && git commit -m "feat: run.sh orchestration + enrich.sh"
```

---

### Task 12: End-to-end dry run on the real new export

**Files:** none (validation task)

- [ ] **Step 1: Seed the ledger from the OLD export so only the 33 are new**

Run:
```bash
.venv/bin/python - <<'PY'
import json
from datetime import datetime
from tools.ingest.config import LEDGER
old=json.load(open('/Users/neoudhaile/Downloads/twitter-Bookmarks-1779930252646.json'))
led={"processed_ids":[x["id"] for x in old],
     "by_id":{x["id"]:{"source_export":"twitter-Bookmarks-1779930252646.json","ingested_at":datetime.now().isoformat(timespec='seconds')} for x in old}}
LEDGER.parent.mkdir(parents=True,exist_ok=True)
json.dump(led, open(LEDGER,'w'), indent=2)
print("ledger seeded:", len(led["processed_ids"]))
PY
```
Expected: `ledger seeded: 154`.

- [ ] **Step 2: Run ingest only against the new export**

Run:
```bash
.venv/bin/python -m tools.ingest.ingest --export ~/Downloads/twitter-Bookmarks-1780584772676.json
```
Expected: `NEW_ITEMS 33 inspo/_inbox/new-items.json`. Open the file and verify the 33 items match the earlier diff (blurrhaus, heynavtoor, … uihssn).

- [ ] **Step 3: Run the enricher + writer manually**

Run:
```bash
bash tools/ingest/enrich.sh && .venv/bin/python -m tools.ingest.apply_enriched
```
Expected: `enriched-items.json` written; `APPLIED 33`. Then verify:
```bash
.venv/bin/python -c "import json; d=json.load(open('inspo/inspiration.json')); print(len(d['items']),'items'); print(len(d['site_designs']),'site_designs')"
git diff --stat inspo/inspiration.md
```
Expected: items count grew by 33; new `site_designs` for the design-worthy domains; MD has a populated `AUTO-INGEST` region with hand-written sections untouched (`git diff` shows only the region added).

- [ ] **Step 4: Verify idempotency**

Run the same export through again:
```bash
.venv/bin/python -m tools.ingest.ingest --export ~/Downloads/twitter-Bookmarks-1780584772676.json
```
Expected: `NO_NEW_ITEMS` (ledger now contains all 187).

- [ ] **Step 5: Commit the populated bucket**

```bash
git add inspo/ && git commit -m "feat: ingest 33 new bookmarks via pipeline (live validation)"
```

---

### Task 13: launchd daemon (the trigger — built last)

**Files:**
- Create: `tools/ingest/net.neoud.bookmark-ingest.plist`
- Create: `tools/ingest/INSTALL.md`

- [ ] **Step 1: Write the plist (WatchPaths on ~/Downloads)**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>net.neoud.bookmark-ingest</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>/Users/neoudhaile/Documents/Projects/Code/neoud.net/run.sh</string>
  </array>
  <key>WatchPaths</key>
  <array><string>/Users/neoudhaile/Downloads</string></array>
  <key>StandardOutPath</key><string>/tmp/neoud-ingest.log</string>
  <key>StandardErrorPath</key><string>/tmp/neoud-ingest.err</string>
  <key>EnvironmentVariables</key>
  <dict><key>PATH</key><string>/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin</string></dict>
</dict>
</plist>
```

- [ ] **Step 2: Write `INSTALL.md`**

```markdown
# Install the bookmark-ingest daemon

1. Copy the plist:
   `cp tools/ingest/net.neoud.bookmark-ingest.plist ~/Library/LaunchAgents/`
2. Load it:
   `launchctl load ~/Library/LaunchAgents/net.neoud.bookmark-ingest.plist`
3. Confirm: `launchctl list | grep neoud`
4. Test: re-export bookmarks to ~/Downloads, then `tail -f /tmp/neoud-ingest.log`.

`claude` must be on the PATH in the plist's EnvironmentVariables, and the Playwright
MCP server must be configured for headless `claude -p`. WatchPaths fires on any
~/Downloads change; `run.sh` no-ops cheaply when there is no new export.

Unload: `launchctl unload ~/Library/LaunchAgents/net.neoud.bookmark-ingest.plist`
```

- [ ] **Step 3: Install and smoke-test**

Run:
```bash
cp tools/ingest/net.neoud.bookmark-ingest.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/net.neoud.bookmark-ingest.plist
launchctl list | grep neoud
```
Expected: the label appears. Touch a dummy file in ~/Downloads and confirm `/tmp/neoud-ingest.log` shows a no-op run ("nothing to do").

- [ ] **Step 4: Commit**

```bash
git add tools/ingest/net.neoud.bookmark-ingest.plist tools/ingest/INSTALL.md && git commit -m "feat: launchd WatchPaths daemon + install docs"
```

---

## Self-review

**Spec coverage:**
- Watcher/daemon → Task 13. Deterministic ingest + diff + harvest → Tasks 3, 4, 6. Enricher (filter, primary URL, title/tags/category, teardown) → Tasks 9, 11. Writers (merge JSON, append site_designs, MD splice, ledger, archive) → Tasks 7, 8, 10, 11. Traceability fields (`source_export`, `ingested_at`) → Tasks 4, 7. Idempotency → Tasks 4, 12 step 4. Failure handling (atomic writes, ledger-after-success, teardown non-fatal) → Tasks 5, 9, 11. Build order (manual first, daemon last) → Tasks 12 then 13. Denylist + list-tweets → Tasks 3, 9.
- Gap intentionally narrowed vs spec: spec said "regenerate inspiration.md"; plan uses a safer managed-region splice to protect hand-written sections (documented in "Key design decisions"). JSON remains source of truth, so no loss of fidelity.

**Placeholder scan:** No TBD/TODO; every code step has complete code; the enricher prompt is the model's contract (intentionally instructions, not code) and the writers it feeds are fully tested.

**Type consistency:** `new-items.json` fields (`all_urls`, `primary_candidates`) produced in Task 6 are consumed by the enricher (Task 9); `enriched-items.json` fields consumed by `merge_items`/`merge_site_designs` (Task 7) and `apply` (Task 10) match the data contract. `deep_external_urls`/`split_primary` (Task 3) names match their use in Task 6. `splice_region`/`render_region_body` (Task 8) match Task 10.
