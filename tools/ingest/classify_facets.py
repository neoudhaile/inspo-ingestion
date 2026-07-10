#!/usr/bin/env python3
"""Backfill relatedness facets onto existing site_designs entries.

For every site_designs entry missing `facets`, send its already-extracted prose
(no browser, no images) to `claude -p` (Sonnet) in chunks and ask it to classify
the site against tools/ingest/taxonomy.json:

    facets: { "vertical": <one>, "mode": <one>, "vibe": [1-3], "topics": [0-3] }

Resumable: entries that already have `facets` are skipped, so a rate-limited run
just continues on relaunch. Values are validated against the taxonomy; invalid
values are dropped (and vertical/mode fall back to null for a later pass).

Usage: .venv/bin/python -m tools.ingest.classify_facets
"""
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tools.ingest.config import INSPIRATION_JSON, REPO
from tools.ingest.jsonio import read_json, write_json_atomic

TAXONOMY = Path(__file__).parent / "taxonomy.json"
CHUNK = 20
CLAUDE = os.environ.get("CLAUDE_BIN", str(Path.home() / ".local/bin/claude"))
MODEL = os.environ.get("NEOUD_ENRICH_MODEL", "sonnet")
LOG = Path("/tmp/neoud-classify.log")


def log(m):
    line = f"[{time.strftime('%H:%M:%S')}] {m}"
    with LOG.open("a") as f:
        f.write(line + "\n")
    print(line, flush=True)


def compact_site(dom, e):
    """The evidence the classifier reads — small but sufficient."""
    return {
        "domain": dom,
        "title": e.get("title"),
        "tagline": e.get("tagline"),
        "what_it_is": e.get("what_it_is"),
        "how_its_designed": e.get("how_its_designed"),
        "palette": e.get("palette"),
        "pattern_keywords": e.get("pattern_keywords", []),
    }


def build_prompt(tax, sites):
    return f"""You are classifying websites for a design-inspiration knowledge graph.

TAXONOMY (the ONLY allowed values; keys starting with _ are rules/instructions):
{json.dumps(tax, indent=1)}

For EACH site below, classify it using ONLY taxonomy values:
- "vertical": exactly one key from taxonomy.vertical (what the site IS)
- "mode": exactly one key from taxonomy.mode (dominant color mode; infer from palette/prose)
- "vibe": 1-3 keys from taxonomy.vibe (how it feels; only ones that genuinely dominate)
- "topics": 0-3 keys from taxonomy.topic (what it is ABOUT; omit when unclear — empty list is fine)

SITES:
{json.dumps(sites, indent=1, ensure_ascii=False)}

Reply with ONLY a JSON object mapping each domain to its facets, no prose, no code fences:
{{"<domain>": {{"vertical": "...", "mode": "...", "vibe": ["..."], "topics": ["..."]}}, ...}}"""


def parse_json_reply(text):
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.S)
    start = text.find("{")
    if start < 0:
        raise ValueError("no JSON object in reply")
    return json.loads(text[start:text.rfind("}") + 1])


def validate(f, tax):
    v = f.get("vertical")
    m = f.get("mode")
    return {
        "vertical": v if v in tax["vertical"] else None,
        "mode": m if m in tax["mode"] else None,
        "vibe": [x for x in (f.get("vibe") or []) if x in tax["vibe"]][:3],
        "topics": [x for x in (f.get("topics") or []) if x in tax["topic"]][:3],
    }


def remaining(doc):
    return [(k, v) for k, v in doc["site_designs"].items()
            if k != "_schema" and "facets" not in v]


def main():
    tax = {k: v for k, v in read_json(TAXONOMY).items() if not k.startswith("_")}
    batch = 0
    while True:
        doc = read_json(INSPIRATION_JSON)
        todo = remaining(doc)
        if not todo:
            log("classify COMPLETE — every site has facets")
            return 0
        chunk = todo[:CHUNK]
        batch += 1
        log(f"batch {batch}: {len(chunk)} sites ({len(todo)} remaining)")
        prompt = build_prompt(tax, [compact_site(d, e) for d, e in chunk])
        r = subprocess.run([CLAUDE, "-p", prompt, "--model", MODEL,
                            "--dangerously-skip-permissions", "--strict-mcp-config"],
                           capture_output=True, text=True, timeout=900, cwd=str(REPO))
        if r.returncode != 0:
            log(f"  claude FAILED rc={r.returncode} (rate limit?) — stopping; rerun to resume. {r.stderr[-200:]}")
            return 1
        try:
            result = parse_json_reply(r.stdout)
        except Exception as ex:
            log(f"  parse error: {ex}; head of reply: {r.stdout[:200]!r} — stopping")
            return 1
        doc = read_json(INSPIRATION_JSON)  # re-read in case daemon wrote meanwhile
        wrote = 0
        for dom, _ in chunk:
            if dom in result:
                doc["site_designs"][dom]["facets"] = validate(result[dom], tax)
                wrote += 1
        write_json_atomic(INSPIRATION_JSON, doc)
        log(f"  wrote facets for {wrote}/{len(chunk)}")


if __name__ == "__main__":
    raise SystemExit(main())
