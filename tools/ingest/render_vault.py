"""Render inspiration.json into an Obsidian-style knowledge-graph vault.

Notes are graph nodes; `[[wikilinks]]` are edges. An agent (or a human in Obsidian)
navigates INDEX -> a hub -> a few site notes, and hops between related sites — never
loading the whole JSON. Deterministic full rebuild, mirroring render_md.py's
"view from the JSON" pattern.

Layout (under inspo/vault/):
  INDEX.md                     entry point / map of content
  sites/<domain>.md            one node per teardown
  patterns|categories|tech|colors|fonts|aesthetics/<slug>.md   hub notes

A facet only becomes a hub when enough sites share it (see HUB_MIN); rarer facets
stay as searchable `tags` on the site note so nothing is lost, but the graph's
navigation nodes stay meaningful.
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
HUB_TYPES = ["aesthetics", "patterns", "categories", "tech", "colors", "fonts"]
# min sites sharing a facet for it to become a hub note; unlisted types = keep all
HUB_MIN = {"patterns": 3, "tech": 3, "fonts": 2}
INDEX_CAP = 40  # max hubs listed per section in INDEX (all hub files still exist)

# --- taxonomy derivation -------------------------------------------------------

# pattern_keyword substring -> aesthetic hub (a site may match several)
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
    s = re.sub(r"[^a-z0-9]+", "-", s.strip().lower())
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
        fam = re.sub(r"\s+\d+$", "", f).strip()          # "Geist 400" -> "Geist"
        if not fam or "fallback" in fam.lower():
            continue
        out.append(fam)
    if not out and "fonts_loaded" in entry:               # rich entry, empty list
        out = ["system-fonts"]
    return list(dict.fromkeys(out))


def domain_category(doc):
    cats = {}
    for it in doc.get("items", []):
        dm = it.get("primary_domain")
        if dm and dm not in cats and it.get("category"):
            cats[dm] = it["category"]
    return cats


# --- graph assembly ------------------------------------------------------------

def build_graph(doc):
    """Return sd, per-site facets, hub membership (thresholded), related-site edges."""
    sd = {k: v for k, v in doc.get("site_designs", {}).items() if k != "_schema"}
    cats = domain_category(doc)
    facets = {}                                  # domain -> {type: [names]}
    for dom, e in sd.items():
        patterns = e.get("pattern_keywords", []) or []
        facets[dom] = {
            "patterns": patterns,
            "categories": [cats.get(dom, "uncategorized")],
            "tech": e.get("tech_stack", []) or [],
            "colors": color_families(e),
            "fonts": font_families(e),
            "aesthetics": aesthetics_for(patterns),
        }
    all_hubs = {t: defaultdict(set) for t in HUB_TYPES}
    for dom, f in facets.items():
        for t in HUB_TYPES:
            for name in f[t]:
                all_hubs[t][name].add(dom)
    # keep only facets shared by >= threshold sites (bounded types keep all)
    hubs = {t: {n: m for n, m in all_hubs[t].items() if len(m) >= HUB_MIN.get(t, 1)}
            for t in HUB_TYPES}
    # related sites by pattern-overlap (top 5)
    related = {}
    for a in sd:
        pa = set(facets[a]["patterns"])
        scored = [(len(pa & set(facets[b]["patterns"])), b) for b in sd if b != a]
        scored = [(n, b) for n, b in scored if n]
        scored.sort(key=lambda x: (-x[0], x[1]))
        related[a] = [b for _, b in scored[:5]]
    return sd, facets, hubs, related


def related_hubs(hubs, t, name, facets):
    """Same-type hubs that co-occur most with `name` across its member sites."""
    co = Counter()
    for dom in hubs[t][name]:
        for other in facets[dom][t]:
            if other != name and other in hubs[t]:
                co[other] += 1
    return [n for n, _ in co.most_common(5)]


# --- rendering -----------------------------------------------------------------

def _facet_line(t, names, hub_names):
    """Link facet names that are hubs; show the rest as inline `tags`."""
    if not names:
        return "—"
    return " ".join(f"[[{t}/{slug(n)}|{n}]]" if n in hub_names else f"`{n}`" for n in names)


def render_site_note(dom, e, facet, related, hubs):
    scr = e.get("screenshot")
    img = f"![{dom}](../../../{scr})\n\n" if scr else ""
    fm = [
        "---",
        f"url: {e.get('url','')}",
        f"title: \"{(e.get('title') or dom).replace(chr(34), '')}\"",
        f"category: {facet['categories'][0]}",
        f"aesthetics: [{', '.join(facet['aesthetics'])}]",
        f"tags: [{', '.join(slug(p) for p in facet['patterns'])}]",
        f"extracted_at: {e.get('extracted_at','')}",
        "---",
        "",
    ]
    body = [
        f"# {e.get('title') or dom}",
        f"> {e.get('tagline','')}  ·  [{dom}]({e.get('url','')})",
        "",
        img.rstrip() + "\n" if img else "",
        f"**What it is** — {e.get('what_it_is','')}",
        "",
        f"**What it shows** — {e.get('what_it_shows','')}",
        "",
        f"**How it works** — {e.get('how_it_works','')}",
        "",
        f"**How it's designed** — {e.get('how_its_designed','')}",
        "",
        f"**Palette** — {e.get('palette','')}",
        f"**Fonts** — {e.get('fonts','')}",
        "",
        "## Connections",
        f"**Aesthetics:** {_facet_line('aesthetics', facet['aesthetics'], hubs['aesthetics'])}",
        f"**Patterns:** {_facet_line('patterns', facet['patterns'], hubs['patterns'])}",
        f"**Category:** {_facet_line('categories', facet['categories'], hubs['categories'])}",
        f"**Tech:** {_facet_line('tech', facet['tech'], hubs['tech'])}",
        f"**Colors:** {_facet_line('colors', facet['colors'], hubs['colors'])}",
        f"**Fonts:** {_facet_line('fonts', facet['fonts'], hubs['fonts'])}",
        "",
        "## Related sites",
        " ".join(f"[[sites/{r}|{r}]]" for r in related) or "—",
        "",
    ]
    return "\n".join(fm) + "\n".join(body)


def render_hub_note(t, name, members, sd, rel):
    lines = [f"# {name}", f"_{len(members)} sites · hub type: {t}_", ""]
    for dom in sorted(members):
        tag = (sd[dom].get("tagline") or sd[dom].get("title") or "").strip()
        lines.append(f"- [[sites/{dom}|{dom}]] — {tag}" if tag else f"- [[sites/{dom}|{dom}]]")
    if rel:
        lines += ["", f"**Related {t}:** {_facet_line(t, rel, set(rel))}"]
    return "\n".join(lines) + "\n"


def render_index(hubs):
    out = ["# Inspiration Vault — Index", "",
           "_Entry point. Pick a hub below, open the site notes it links, then hop via each "
           "site's **Related sites**. You never need to open inspiration.json._", ""]
    titles = {"aesthetics": "By aesthetic", "patterns": "By pattern", "categories": "By category",
              "tech": "By tech", "colors": "By color", "fonts": "By font"}
    for t in HUB_TYPES:
        ranked = sorted(hubs[t].items(), key=lambda kv: (-len(kv[1]), kv[0]))
        shown, extra = ranked[:INDEX_CAP], max(0, len(ranked) - INDEX_CAP)
        line = " · ".join(f"[[{t}/{slug(n)}|{n}]] ({len(m)})" for n, m in shown) or "—"
        if extra:
            line += f"  _+{extra} more hubs in `{t}/`_"
        out += [f"## {titles[t]}", line, ""]
    return "\n".join(out)


def build_vault(doc, out_dir=VAULT):
    sd, facets, hubs, related = build_graph(doc)
    out_dir = Path(out_dir)
    for sub in ["sites", *HUB_TYPES]:            # wipe generated content; keep .obsidian/
        shutil.rmtree(out_dir / sub, ignore_errors=True)
        (out_dir / sub).mkdir(parents=True, exist_ok=True)

    for dom, e in sd.items():
        (out_dir / "sites" / f"{dom}.md").write_text(
            render_site_note(dom, e, facets[dom], related[dom], hubs))

    counts = {"sites": len(sd)}
    for t in HUB_TYPES:
        counts[t] = len(hubs[t])
        for name, members in hubs[t].items():
            rel = related_hubs(hubs, t, name, facets)
            (out_dir / t / f"{slug(name)}.md").write_text(
                render_hub_note(t, name, members, sd, rel))

    (out_dir / "INDEX.md").write_text(render_index(hubs))
    return counts


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
