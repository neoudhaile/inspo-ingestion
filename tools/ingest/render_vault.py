"""Render inspiration.json into an Obsidian vault: one note per website,
connected by a small controlled set of relatedness facets.

Graph model (the whole point):
- Each website is ONE note holding its full teardown.
- The ONLY graph-forming tags are the four taxonomy facets:
    #vertical/<what it IS>   #vibe/<how it FEELS>   #topic/<what it's ABOUT>   #mode/<dark|light>
  (taxonomy.json is the controlled vocabulary; the enricher classifies new sites
  against it, so clusters stay coherent as the vault grows.)
- Verticals cluster sites of the same kind (startup sites, personal blogs...).
- Topics bridge clusters (a personal blog ABOUT startups reaches the startup cluster).
- Each note also links its most-related sites directly, with the WHY printed
  (shared facets), computed from a weighted facet overlap.
- Everything granular (pattern keywords, tech, fonts, tokens) stays inside the note
  as searchable text — never as graph tags.

Deterministic full rebuild: INDEX.md + <domain>.md, flat.
"""
import argparse
import json
import re
import shutil
from collections import Counter
from pathlib import Path

from .config import INSPIRATION_JSON, INSPO
from .jsonio import read_json

VAULT = INSPO / "vault"
FACET_NS = {"vertical": "vertical", "vibe": "vibe", "topics": "topic", "mode": "mode"}
# weighted facet overlap for direct site<->site edges
W_VERTICAL, W_VIBE, W_TOPIC, W_MODE = 3, 2, 2, 1
EDGE_MIN, EDGE_TOP = 5, 6


def slug(s: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", str(s).strip().lower())
    return s.strip("-") or "misc"


def facets_of(e):
    f = e.get("facets") or {}
    return {
        "vertical": f.get("vertical"),
        "mode": f.get("mode"),
        "vibe": f.get("vibe") or [],
        "topics": f.get("topics") or [],
    }


def tags_for(f):
    tags = []
    if f["vertical"]:
        tags.append(f"vertical/{slug(f['vertical'])}")
    for v in f["vibe"]:
        tags.append(f"vibe/{slug(v)}")
    for t in f["topics"]:
        tags.append(f"topic/{slug(t)}")
    if f["mode"]:
        tags.append(f"mode/{slug(f['mode'])}")
    return tags


def edge_score(fa, fb):
    """Weighted overlap + the shared facets (the printable WHY)."""
    score, shared = 0, []
    if fa["vertical"] and fa["vertical"] == fb["vertical"]:
        score += W_VERTICAL
        shared.append(fa["vertical"])
    for v in fa["vibe"]:
        if v in fb["vibe"]:
            score += W_VIBE
            shared.append(v)
    for t in fa["topics"]:
        if t in fb["topics"]:
            score += W_TOPIC
            shared.append(t)
    if fa["mode"] and fa["mode"] == fb["mode"]:
        score += W_MODE
        shared.append(fa["mode"])
    return score, shared


def related_sites(facets):
    rel = {}
    doms = list(facets)
    for a in doms:
        scored = []
        for b in doms:
            if b == a:
                continue
            s, shared = edge_score(facets[a], facets[b])
            if s >= EDGE_MIN:
                scored.append((s, b, shared))
        scored.sort(key=lambda x: (-x[0], x[1]))
        rel[a] = [(b, shared) for _, b, shared in scored[:EDGE_TOP]]
    return rel


# --- note rendering -------------------------------------------------------------

def _tokens(e):
    out = []
    if e.get("palette"):
        out.append(f"- **Palette:** {e['palette']}")
    if e.get("palette_tokens"):
        toks = ", ".join(f"{t.get('name')}: {t.get('value')} ({t.get('kind')})"
                         for t in e["palette_tokens"])
        out.append(f"- **Palette tokens:** {toks}")
    if e.get("fonts"):
        out.append(f"- **Fonts:** {e['fonts']}")
    if e.get("fonts_loaded") is not None:
        out.append(f"- **Fonts loaded:** {', '.join(e['fonts_loaded']) or 'system only (no webfont)'}")
    if e.get("tech_stack"):
        out.append(f"- **Tech stack:** {', '.join(e['tech_stack'])}")
    if e.get("pattern_keywords"):
        out.append(f"- **Keywords:** {', '.join(e['pattern_keywords'])}")
    if e.get("media_mix"):
        m = e["media_mix"]
        out.append("- **Media mix:** " + " · ".join(f"{k} {v}" for k, v in m.items() if v))
    if e.get("page_height_px") is not None:
        out.append(f"- **Page height:** {e['page_height_px']}px "
                   f"(single-screen: {e.get('is_single_screen')})")
    if e.get("responsive_note"):
        out.append(f"- **Responsive:** {e['responsive_note']}")
    if e.get("headings"):
        out.append(f"- **Headings:** {' / '.join(e['headings'])}")
    if e.get("links_out"):
        out.append("- **Links out:** " + " · ".join(
            f"[{l.get('label','link')}]({l.get('href','')})" for l in e["links_out"]))
    if e.get("weight"):
        w = e["weight"]
        out.append(f"- **Weight:** {w.get('requests')} requests; hosts: {', '.join(w.get('hosts', []))}")
    if e.get("extracted_at") or e.get("extracted_via"):
        out.append(f"- **Extracted:** {e.get('extracted_at','')} · {e.get('extracted_via','')}")
    return "\n".join(out)


def render_site_note(dom, e, f, related):
    tags = tags_for(f)
    scr = e.get("screenshot")
    img = f"![{dom}](../../{scr})\n" if scr else ""
    fm = [
        "---",
        f"url: {e.get('url','')}",
        f"domain: {dom}",
        f"title: \"{(e.get('title') or dom).replace(chr(34), '')}\"",
        f"vertical: {f['vertical'] or 'unclassified'}",
        f"mode: {f['mode'] or ''}",
        f"vibe: [{', '.join(f['vibe'])}]",
        f"topics: [{', '.join(f['topics'])}]",
        f"extracted_at: {e.get('extracted_at','')}",
        "tags:",
        *[f"  - {t}" for t in tags],
        "---",
        "",
    ]
    rel_lines = [f"- [[{b}]] — shared: {', '.join(shared)}" for b, shared in related] or ["—"]
    body = [
        f"# {e.get('title') or dom}",
        f"> {e.get('tagline','')}  ·  [{dom}]({e.get('url','')})",
        "",
        img,
        f"**Vertical:** #{ 'vertical/'+slug(f['vertical']) if f['vertical'] else 'unclassified' }"
        f"  ·  **Vibe:** {' '.join('#vibe/'+slug(v) for v in f['vibe']) or '—'}"
        f"  ·  **Topics:** {' '.join('#topic/'+slug(t) for t in f['topics']) or '—'}"
        f"  ·  **Mode:** {'#mode/'+slug(f['mode']) if f['mode'] else '—'}",
        "",
        f"## What it is\n{e.get('what_it_is','')}",
        "",
        f"## What it shows\n{e.get('what_it_shows','')}",
        "",
        f"## How it works\n{e.get('how_it_works','')}",
        "",
        f"## How it's designed\n{e.get('how_its_designed','')}",
        "",
        "## Design data",
        _tokens(e),
        "",
        "## Related sites",
        *rel_lines,
        "",
    ]
    return "\n".join(fm) + "\n".join(body)


def render_index(facets, tag_counts):
    total = len(facets)
    unclassified = sum(1 for f in facets.values() if not f["vertical"])
    out = ["# Inspiration Vault", "",
           f"_{total} websites, one note each. Sites connect through four controlled facets "
           "(see `tools/ingest/taxonomy.json`): **vertical** (what it is), **vibe** (how it "
           "feels), **topic** (what it's about — bridges clusters), **mode** (dark/light). "
           "In Obsidian: Graph view with **Tags** on. As an agent: "
           "`rg -l '#vertical/portfolio' inspo/vault` then read those notes; each note's "
           "Related sites lists its nearest neighbors with the shared facets._", ""]
    if unclassified:
        out += [f"> {unclassified} sites not yet classified (run "
                "`python -m tools.ingest.classify_facets`).", ""]
    order = ["vertical", "vibe", "topic", "mode"]
    for ns in order:
        rows = sorted(((t, c) for t, c in tag_counts.items() if t.startswith(ns + "/")),
                      key=lambda x: (-x[1], x[0]))
        if rows:
            out += [f"## {ns}",
                    " · ".join(f"`#{t}` ({c})" for t, c in rows), ""]
    return "\n".join(out)


def build_vault(doc, out_dir=VAULT):
    sd = {k: v for k, v in doc.get("site_designs", {}).items() if k != "_schema"}
    facets = {dom: facets_of(e) for dom, e in sd.items()}
    related = related_sites(facets)

    out_dir = Path(out_dir)
    # hand-written notes the rebuild must never delete
    PRESERVE = {".obsidian", "ITERATIONS.md"}
    if out_dir.exists():
        for p in out_dir.iterdir():
            if p.name in PRESERVE:
                continue
            shutil.rmtree(p, ignore_errors=True) if p.is_dir() else p.unlink()
    out_dir.mkdir(parents=True, exist_ok=True)

    tag_counts = Counter()
    edge_count = 0
    for dom, e in sd.items():
        (out_dir / f"{dom}.md").write_text(
            render_site_note(dom, e, facets[dom], related[dom]))
        tag_counts.update(tags_for(facets[dom]))
        edge_count += len(related[dom])

    (out_dir / "INDEX.md").write_text(render_index(facets, tag_counts))
    return {"sites": len(sd), "tag_nodes": len(tag_counts),
            "singleton_tags": sum(1 for c in tag_counts.values() if c == 1),
            "site_edges": edge_count}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default=str(INSPIRATION_JSON))
    ap.add_argument("--out", default=str(VAULT))
    args = ap.parse_args()
    summary = build_vault(read_json(args.json), args.out)
    print("VAULT_BUILT " + args.out + " " + json.dumps(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
