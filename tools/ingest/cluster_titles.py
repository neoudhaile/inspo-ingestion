#!/usr/bin/env python3
"""Give each cluster a human title, written from what its members actually are.

Why. Obsidian's graph colour groups have no label field — the group shows its search
query and nothing else — so a cluster tagged `#cluster/3` is just "3" on screen, and
the auto-generated keyword names ("app single grid plus", "plus fixed jonas google")
were word-frequency noise. A title has to be a real phrase, and it has to live in the
tag itself so the group query reads as the name: `tag:#personal-portfolios`.

How. One Sonnet call per space, handed every sub-cluster's members:

  purpose  each member's essence — kind, domain, subject
  design   each member's design prose — how it looks, its palette and type

The prompt asks for what members genuinely share, and asks for honesty when they
don't: an incoherent cluster is titled "Mixed: a, b, c". That makes the titles a
review tool as well as a label — a "Mixed:" group is one the clustering got wrong.

Titles are judgment, so they live in the rendered vault and its README, never in
inspiration.json.
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tools.ingest.essence import MODEL, loads_loose, run_claude

MAX_WORDS = 6
MAX_SLUG = 48

LENS = {
    "purpose": ("PURPOSE — what each site is and what it is for",
                'e.g. "Personal portfolios", "Open-source animation libraries", '
                '"B2B lead-gen agencies", "Design inspiration galleries"'),
    "design": ("DESIGN — how each site looks and feels",
               'e.g. "Warm paper and serif type", "Stark black-and-white mono", '
               '"Glossy SaaS gradients", "Retro pixel desktop"'),
}

PROMPT = """You are naming clusters in a design-inspiration library. An algorithm grouped
these websites by {lens}. Each member is listed with a short description.

For EVERY cluster id below, write a short title: 2 to 5 words, naming what its members
genuinely share, the way a designer browsing the library would describe the group
({examples}).

- Top-level ids (no dot) are parents; their members are the union of their children.
  Name a parent for what its children have in common.
- Child ids (with a dot) sit inside their parent. Name them MORE specifically than the
  parent, and make sibling titles clearly different from each other.
- Be honest. If a cluster's members do not share a clear {short}, the title must start
  with "Mixed:" followed by the two or three main things in it
  (e.g. "Mixed: hardware, dev tools, aerospace").
- Every title must be unique. No numbers, no quotes, no trailing punctuation.

Return ONLY a JSON object mapping every id to its title, no markdown fence.

CLUSTERS:
{clusters}"""


def member_line(dom, entry, space):
    """One short line describing a site through the lens of `space`."""
    if space == "purpose":
        e = entry.get("essence") or {}
        bits = [e.get("kind"), e.get("domain"), e.get("subject")]
        text = " | ".join(b for b in bits if b) or (entry.get("what_it_is") or "")[:160]
    else:
        text = " ".join(str(entry.get(k) or "") for k in ("how_its_designed", "palette"))
    text = re.sub(r"\s+", " ", text).strip()
    return f"{dom}: {text[:220]}"


def cluster_members(result):
    """{path: [domains]} for every prefix of every site's path (all levels)."""
    out = defaultdict(list)
    for dom, info in result["sites"].items():
        parts = info["path"].split(".")
        for i in range(len(parts)):
            out[".".join(parts[:i + 1])].append(dom)
    return out


def _key(p):
    return tuple(int(x) for x in p.split("."))


def build_prompt(result, doc, space):
    """Children are listed with members; parents by which children they contain, so
    the prompt stays short and each site is described once."""
    members = cluster_members(result)
    sd = doc["site_designs"]
    deepest = max(len(p.split(".")) for p in members)
    blocks = []
    for p in sorted(members, key=_key):
        depth = len(p.split("."))
        if depth < deepest:
            kids = sorted((q for q in members if q.startswith(p + ".")
                           and len(q.split(".")) == depth + 1), key=_key)
            blocks.append(f"[{p}] parent of {', '.join(kids)} ({len(members[p])} sites)")
        else:
            lines = "\n".join("  - " + member_line(d, sd.get(d) or {}, space)
                              for d in sorted(members[p]))
            blocks.append(f"[{p}] ({len(members[p])} sites)\n{lines}")
    lens, examples = LENS[space]
    short = "purpose" if space == "purpose" else "look"
    return PROMPT.format(lens=lens, examples=examples, short=short,
                         clusters="\n\n".join(blocks))


def clean_title(t):
    t = re.sub(r"\s+", " ", str(t or "")).strip().strip('"\'.;,')
    words = t.split()
    return " ".join(words[:MAX_WORDS + 3]) if len(words) > MAX_WORDS + 3 else t


def title_clusters(result, doc, model=MODEL, run=None):
    """{path: title} for every cluster in `result`. Missing ids fall back to the
    automatic keyword name, so a partial answer never breaks a render."""
    run = run or run_claude
    space = result["space"]
    text, _meta = run(build_prompt(result, doc, space), browser=False, model=model,
                      timeout=300)
    got = loads_loose(text)
    fallback = result.get("cluster_names") or {}
    out = {}
    for p in cluster_members(result):
        t = clean_title(got.get(p))
        out[p] = t if t else (fallback.get(p) or f"cluster {p}")
    return out


def slug_tag(title):
    """A title as an Obsidian tag segment: lowercase, letters/digits/hyphens.

    Obsidian tags cannot hold spaces or most punctuation, and a tag that is all
    digits is not a tag at all, so a numeric-only slug gets a prefix.
    """
    s = re.sub(r"[^a-z0-9]+", "-", str(title).lower()).strip("-")
    s = re.sub(r"-{2,}", "-", s)[:MAX_SLUG].strip("-") or "cluster"
    return s if re.search(r"[a-z]", s) else f"c-{s}"


def named_tags(titles):
    """{path: tag}, one FLAT tag per cluster, unique across the whole space.

    Flat rather than nested (`family/child`) because the graph panel truncates a
    group's query after ~20 characters: nested, both children of
    "designer-and-studio-portfolios" render as the same `tag:#designer-and-studio-…`,
    and the name is the only label a group has. Each note carries its family's tag and
    its cluster's tag, so families stay searchable without the nesting.
    """
    out, taken = {}, set()
    for p in sorted(titles, key=_key):
        base = slug_tag(titles[p])
        slug, n = base, 2
        while slug in taken:
            slug, n = f"{base}-{n}", n + 1
        taken.add(slug)
        out[p] = slug
    return out


def colour_depth(paths):
    """Which level gets a colour group: the second when there is one.

    The owner wants every named cluster coloured, not just the eight families, and
    the second level is where names are specific ("Personal designer and developer
    portfolios" rather than "Designer and studio portfolios").
    """
    deepest = max(p.count(".") + 1 for p in paths)
    return min(2, deepest)


def family_palette(paths, titles=None):
    """{path: rgb_int} for every cluster at colour_depth, coordinated by family.

    Hue encodes the family, so the graph reads as eight colour regions; lightness
    separates siblings inside a family. A cluster titled "Mixed:" keeps its family's
    hue at low saturation: still placed, visibly weaker, so the clusters the titler
    could not name stand out as greyed patches.
    """
    import colorsys
    titles = titles or {}
    depth = colour_depth(paths)
    level = sorted((p for p in paths if p.count(".") + 1 == depth), key=_key)
    tops = sorted({p.split(".")[0] for p in level}, key=int)
    out = {}
    for i, top in enumerate(tops):
        hue = (0.0 + i / len(tops)) % 1.0
        kids = [p for p in level if p.split(".")[0] == top]
        n = len(kids)
        for j, k in enumerate(kids):
            t = 0.5 if n == 1 else j / (n - 1)
            light = 0.72 - 0.28 * t
            # Fan the hue a little inside the family too. Lightness alone did not
            # separate siblings: six shades of yellow read as one colour. ±0.04 keeps
            # every family clear of its neighbours (families sit 1/8 = 0.125 apart).
            h = (hue - 0.04 + 0.08 * t) % 1.0
            mixed = str(titles.get(k, "")).lower().startswith("mixed")
            sat = 0.16 if mixed else 0.74
            r, g, b = colorsys.hls_to_rgb(h, light, sat)
            out[k] = (int(r * 255) << 16) + (int(g * 255) << 8) + int(b * 255)
    return out
