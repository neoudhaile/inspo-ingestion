"""Render inspiration.json into an Obsidian vault: one note per website.

Each site is a single self-contained note holding ALL its extracted teardown data,
plus categorizing **tags** (nested, e.g. #aesthetic/dark #pattern/portfolio #tech/nextjs).
Obsidian connects notes that share tags (enable "Tags" in graph view), and each note
also links its most-similar sites directly. There are no separate hub files — the tags
ARE the connective tissue. Deterministic full rebuild, mirroring render_md.py.

Layout (flat, under inspo/vault/):
  INDEX.md          tag map / entry point
  <domain>.md       one node per teardown
"""
import argparse
import json
import re
import shutil
from collections import Counter, defaultdict
from pathlib import Path

from .config import INSPIRATION_JSON, INSPO
from .jsonio import read_json

VAULT = INSPO / "vault"
# facet-type -> tag namespace
TAG_NS = {"aesthetics": "aesthetic", "patterns": "pattern", "tech": "tech",
          "colors": "color", "fonts": "font", "categories": "category"}

AESTHETIC_TRIGGERS = {
    "dark": "dark", "light": "light",
    "minimal": "minimal", "monochrome": "minimal", "text-first": "minimal",
    "text-only": "minimal", "whitespace": "minimal", "swiss": "minimal",
    "editorial": "editorial", "magazine": "editorial", "serif-display": "editorial",
    "institutional": "editorial", "archive": "editorial", "research": "editorial",
    "playful": "playful", "tactile": "playful", "gamified": "playful",
    "pixel": "playful", "bento": "playful", "frosted": "playful", "glow": "playful",
    "brutalist": "brutalist",
    "retro": "retro", "vaporwave": "retro", "nostalgia": "retro",
    "desktop-metaphor": "retro", "skeuomorphic": "retro", "finder": "retro",
    "luxury": "luxury", "full-bleed": "luxury", "cinematic": "luxury",
    "photography": "luxury", "photo": "luxury",
    "webgl": "experimental", "canvas": "experimental", "3d": "experimental",
    "creative-developer": "experimental", "experimental": "experimental",
    "developer-tool": "developer-product", "monospace": "developer-product",
    "tool-app": "developer-product", "saas": "developer-product",
    "product-landing": "developer-product", "dashboard": "developer-product",
    "portfolio": "portfolio", "personal-homepage": "portfolio", "case-studies": "portfolio",
}
WARM = ("cream", "warm", "peach", "amber", "beige", "tan", "gold", "orange", "sand")
COOL = ("blue", "indigo", "teal", "mint", "cyan", "navy", "violet", "purple", "green")


def slug(s: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", str(s).strip().lower())
    return s.strip("-") or "misc"


def aesthetics_for(patterns):
    out = []
    for kw in patterns:
        for trig, aes in AESTHETIC_TRIGGERS.items():
            if trig in kw and aes not in out:
                out.append(aes)
    return out


def color_families(entry):
    fams = []
    joined = " ".join(entry.get("pattern_keywords", [])).lower()
    palette = (entry.get("palette") or "").lower()
    if "dark" in joined:
        fams.append("dark")
    if "light" in joined:
        fams.append("light")
    if "monochrome" in joined or "monochrome" in palette:
        fams.append("monochrome")
    if any(w in palette for w in WARM):
        fams.append("warm")
    if any(c in palette for c in COOL):
        fams.append("cool")
    return list(dict.fromkeys(fams)) or ["neutral"]


def font_families(entry):
    out = []
    for f in entry.get("fonts_loaded", []) or []:
        fam = re.sub(r"\s+\d+$", "", f).strip()
        if not fam or "fallback" in fam.lower():
            continue
        out.append(fam)
    if not out and "fonts_loaded" in entry:
        out = ["system-fonts"]
    return list(dict.fromkeys(out))


def domain_category(doc):
    cats = {}
    for it in doc.get("items", []):
        dm = it.get("primary_domain")
        if dm and dm not in cats and it.get("category"):
            cats[dm] = it["category"]
    return cats


def facets_for(dom, e, cats):
    patterns = e.get("pattern_keywords", []) or []
    return {
        "aesthetics": aesthetics_for(patterns),
        "patterns": patterns,
        "tech": e.get("tech_stack", []) or [],
        "colors": color_families(e),
        "fonts": font_families(e),
        "categories": [cats.get(dom, "uncategorized")],
    }


def tags_for(facet):
    """Flat, deduped nested tags across all facet types, in a stable order."""
    tags = []
    for ftype in ("categories", "aesthetics", "patterns", "tech", "colors", "fonts"):
        for name in facet[ftype]:
            t = f"{TAG_NS[ftype]}/{slug(name)}"
            if t not in tags:
                tags.append(t)
    return tags


def related_sites(sd, facets):
    rel = {}
    for a in sd:
        pa = set(facets[a]["patterns"])
        scored = [(len(pa & set(facets[b]["patterns"])), b) for b in sd if b != a]
        scored = [(n, b) for n, b in scored if n]
        scored.sort(key=lambda x: (-x[0], x[1]))
        rel[a] = [b for _, b in scored[:6]]
    return rel


# --- rendering -----------------------------------------------------------------

def _tokens(e):
    """Full structured extraction as a bullet list (skip absent fields)."""
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


def render_site_note(dom, e, facet, related):
    tags = tags_for(facet)
    scr = e.get("screenshot")
    img = f"![{dom}](../../{scr})\n\n" if scr else ""
    fm = [
        "---",
        f"url: {e.get('url','')}",
        f"domain: {dom}",
        f"title: \"{(e.get('title') or dom).replace(chr(34), '')}\"",
        f"category: {facet['categories'][0]}",
        f"extracted_at: {e.get('extracted_at','')}",
        "tags:",
        *[f"  - {t}" for t in tags],
        "---",
        "",
    ]
    body = [
        f"# {e.get('title') or dom}",
        f"> {e.get('tagline','')}  ·  [{dom}]({e.get('url','')})",
        "",
        img.rstrip("\n") + ("\n" if img else ""),
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
        " ".join(f"[[{r}]]" for r in related) or "—",
        "",
        "## Tags",
        " ".join(f"#{t}" for t in tags),
        "",
    ]
    return "\n".join(fm) + "\n".join(body)


def render_index(tag_counts):
    out = ["# Inspiration Vault", "",
           "_Each note is one website with its full teardown. Tags (nested, e.g. "
           "`#aesthetic/dark`) categorize and connect the notes — in Obsidian, enable "
           "**Tags** in Graph view; as an agent, `rg -l '#pattern/portfolio' inspo/vault` "
           "to find matching sites, then read those notes. Tags shared by ≥2 sites:_", ""]
    by_ns = defaultdict(list)
    for tag, n in tag_counts.items():
        ns, name = tag.split("/", 1)
        if n >= 2:
            by_ns[ns].append((name, n))
    order = ["aesthetic", "pattern", "category", "tech", "color", "font"]
    cap = 40
    for ns in order:
        rows = sorted(by_ns.get(ns, []), key=lambda x: (-x[1], x[0]))
        if rows:
            shown, extra = rows[:cap], max(0, len(rows) - cap)
            line = " · ".join(f"`#{ns}/{slug(n)}` ({c})" for n, c in shown)
            if extra:
                line += f"  _+{extra} more (grep the vault, or use Obsidian's Tag pane)_"
            out += [f"## {ns}", line, ""]
    return "\n".join(out)


def build_vault(doc, out_dir=VAULT):
    sd = {k: v for k, v in doc.get("site_designs", {}).items() if k != "_schema"}
    cats = domain_category(doc)
    facets = {dom: facets_for(dom, e, cats) for dom, e in sd.items()}
    related = related_sites(sd, facets)

    out_dir = Path(out_dir)
    # wipe generated content (everything except a top-level .obsidian config)
    if out_dir.exists():
        for p in out_dir.iterdir():
            if p.name == ".obsidian":
                continue
            shutil.rmtree(p, ignore_errors=True) if p.is_dir() else p.unlink()
    out_dir.mkdir(parents=True, exist_ok=True)

    tag_counts = Counter()
    for dom, e in sd.items():
        (out_dir / f"{dom}.md").write_text(render_site_note(dom, e, facets[dom], related[dom]))
        tag_counts.update(tags_for(facets[dom]))

    (out_dir / "INDEX.md").write_text(render_index(tag_counts))
    return {"sites": len(sd), "distinct_tags": len(tag_counts),
            "connective_tags": sum(1 for c in tag_counts.values() if c >= 2)}


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
