#!/usr/bin/env python3
"""Render a clustering run as browsable Obsidian vaults, one numbered folder per try.

This is the feedback loop for the clustering spike. Each run writes

    inspo/cluster-<n>/
        purpose/     <- open this as an Obsidian vault
        design/      <- and this one
        README.md    <- the settings that produced them, and the cluster sizes

so a reclustering never overwrites the last one and two attempts can be compared
side by side. Numbering is automatic: the next unused n.

The graph model, which is the whole point:

- Every node is a website. Nothing else gets a note, so nothing else can become a
  node — no `dark`, no `minimal`, no theme hubs. That was the explicit ask.
- Edges are each site's nearest neighbours in embedding space, symmetrized. Sites sit
  near the sites they actually resemble, not near the sites that happen to share a
  tag.
- Cluster membership rides in frontmatter as `cluster/<path>` tags, which the shipped
  graph config uses for colour only, with tag display switched off. Tags that are
  never displayed cannot become nodes, so the colouring is free.
"""
import argparse
import colorsys
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tools.ingest.config import INSPIRATION_JSON, INSPO, REPO
from tools.ingest.jsonio import read_json

CLUSTER_JSON = INSPO / "_clusters"

# Which teardown fields each vault leads with. The rest still appear, lower down —
# clicking a node should always show the whole site, whichever graph you came from.
LEAD_FIELDS = {
    "purpose": [("what_it_is", "What it is"), ("what_it_shows", "What it shows"),
                ("how_it_works", "How it works")],
    "design": [("how_its_designed", "How it's designed"), ("palette", "Palette"),
               ("fonts", "Fonts")],
}
REST_FIELDS = [("what_it_is", "What it is"), ("what_it_shows", "What it shows"),
               ("how_it_works", "How it works"),
               ("how_its_designed", "How it's designed"),
               ("palette", "Palette"), ("fonts", "Fonts")]


def next_version(base=INSPO):
    n = 1
    while (base / f"cluster-{n}").exists():
        n += 1
    return n


def cluster_color(i, total):
    """Evenly spaced hues as the integer Obsidian's graph config wants."""
    r, g, b = colorsys.hsv_to_rgb((i / max(total, 1)) % 1.0, 0.62, 0.95)
    return (int(r * 255) << 16) + (int(g * 255) << 8) + int(b * 255)


def graph_config(top_level):
    """An .obsidian/graph.json so the vault opens looking deliberate, not default.

    showTags is false on purpose: the cluster tags exist to drive these colour
    groups, and a displayed tag would appear as a node, which is exactly what this
    whole redesign is getting rid of.
    """
    return {
        "collapse-filter": True, "search": "", "showTags": False,
        "showAttachments": False, "hideUnresolved": True, "showOrphans": True,
        "collapse-color-groups": False,
        "colorGroups": [
            {"query": f"tag:#cluster/{c}", "color": {"a": 1, "rgb": cluster_color(i, len(top_level))}}
            for i, c in enumerate(sorted(top_level, key=int))
        ],
        "collapse-display": False, "showArrow": False, "textFadeMultiplier": -0.7,
        "nodeSizeMultiplier": 1.4, "lineSizeMultiplier": 0.7,
        "collapse-forces": False, "centerStrength": 0.42, "repelStrength": 12,
        "linkStrength": 0.75, "linkDistance": 180, "scale": 0.55,
        "close": False,
    }


def tags_for(path):
    """A tag per level: 3, 3.2, 3.2.1 -> cluster/3, cluster/3-2, cluster/3-2-1."""
    parts = path.split(".")
    return [f"cluster/{'-'.join(parts[:i + 1])}" for i in range(len(parts))]


def yaml_str(s):
    return '"' + str(s).replace('"', "'") + '"'


def render_note(dom, entry, info, names, space, screenshot_rel):
    path = info["path"]
    lead = LEAD_FIELDS[space]
    lead_keys = {k for k, _ in lead}

    fm = ["---",
          f"domain: {dom}",
          f"url: {entry.get('url', '')}",
          f"title: {yaml_str(entry.get('title') or dom)}",
          f"cluster: {yaml_str(path)}",
          f"cluster_name: {yaml_str(names.get(path, ''))}"]
    for depth in range(len(path.split("."))):
        prefix = ".".join(path.split(".")[:depth + 1])
        fm.append(f"cluster_l{depth + 1}: {yaml_str(names.get(prefix, prefix))}")
    fm += ["tags:"] + [f"  - {t}" for t in tags_for(path)] + ["---", ""]

    body = [f"# {entry.get('title') or dom}",
            f"> [{dom}]({entry.get('url', '')}) · cluster **{path}** — "
            f"*{names.get(path, '')}*", ""]

    scr = entry.get("screenshot")
    if scr:
        body.append(f"![{dom}]({screenshot_rel}/{Path(scr).name})\n")

    for key, label in lead:
        v = entry.get(key)
        if v:
            body += [f"**{label}.** {v}", ""]

    rel = info.get("neighbors") or []
    body += ["## Nearest in this space", ""]
    body += [f"- [[{n['domain']}]] — {n['score']:.3f}" for n in rel] or ["—"]
    body.append("")

    extra = [(k, l) for k, l in REST_FIELDS if k not in lead_keys and entry.get(k)]
    if extra:
        body += ["## Everything else", ""]
        for key, label in extra:
            body += [f"**{label}.** {entry[key]}", ""]

    if entry.get("tech_stack"):
        body += [f"**Tech.** {', '.join(entry['tech_stack'])}", ""]

    return "\n".join(fm + body)


def render_index(result, names):
    sites = result["sites"]
    by_path = {}
    for d, info in sites.items():
        by_path.setdefault(info["path"], []).append(d)

    def key(p):
        return tuple(int(x) for x in p.split("."))

    out = [f"# {result['space'].capitalize()} clusters", "",
           f"_{len(sites)} sites · {result['provider']}:{result['model']} · "
           f"cuts {result['levels']} · k={result['k']}._", "",
           "Open this folder as an Obsidian vault, then Graph view. Leave **Tags** "
           "off — every node is a website, and the cluster tags are here only to "
           "colour them.", ""]
    seen = set()
    for leaf in sorted(by_path, key=key):
        parts = leaf.split(".")
        for depth in range(len(parts)):
            prefix = ".".join(parts[:depth + 1])
            if prefix in seen:
                continue
            seen.add(prefix)
            size = sum(len(v) for p, v in by_path.items()
                       if p == prefix or p.startswith(prefix + "."))
            out.append(f"{'  ' * depth}- **{prefix}** ({size}) {names.get(prefix, '')}")
            if depth == len(result["levels"]) - 1:
                for m in sorted(by_path.get(prefix, [])):
                    out.append(f"{'  ' * depth}    - [[{m}]]")
    return "\n".join(out) + "\n"


def render_space(result, doc, outdir):
    names = result["cluster_names"]
    sd = doc["site_designs"]
    outdir.mkdir(parents=True, exist_ok=True)
    # Path back to screenshots/ from inside this folder. relpath rather than
    # relative_to: the output directory is not always under the repo (tests render
    # to a tmpdir), and relative_to raises rather than coping.
    screenshot_rel = os.path.relpath(REPO / "screenshots", outdir).replace(os.sep, "/")

    for dom, info in result["sites"].items():
        entry = sd.get(dom) or {}
        (outdir / f"{dom}.md").write_text(
            render_note(dom, entry, info, names, result["space"], screenshot_rel))

    (outdir / "INDEX.md").write_text(render_index(result, names))

    tops = sorted({i["path"].split(".")[0] for i in result["sites"].values()}, key=int)
    obs = outdir / ".obsidian"
    obs.mkdir(exist_ok=True)
    (obs / "graph.json").write_text(json.dumps(graph_config(tops), indent=2))
    return len(result["sites"])


def render_version(results, doc, version_dir):
    version_dir.mkdir(parents=True, exist_ok=True)
    lines = [f"# {version_dir.name}", "",
             "Two Obsidian vaults from one clustering run. Open "
             f"`{version_dir.name}/purpose` or `{version_dir.name}/design` as a vault "
             "(File → Open folder as vault), then Graph view with **Tags off**.", ""]
    for res in results:
        n = render_space(res, doc, version_dir / res["space"])
        sizes = Counter(i["path"].split(".")[0] for i in res["sites"].values())
        ordered = [sizes[k] for k in sorted(sizes, key=int)]
        lines += [f"## {res['space']} ({n} sites)", "",
                  f"- model: `{res['provider']}:{res['model']}`",
                  f"- cuts: `{res['levels']}` · k: `{res['k']}`",
                  f"- top-level sizes: `{ordered}` "
                  f"(largest {max(ordered) / n:.0%})", ""]
        for top in sorted(sizes, key=int):
            lines.append(f"  - **{top}** ({sizes[top]}) {res['cluster_names'].get(top, '')}")
        lines.append("")
    (version_dir / "README.md").write_text("\n".join(lines))
    return version_dir


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--spaces", default="purpose,design")
    ap.add_argument("--version", type=int, default=None,
                    help="cluster-N to write (default: next unused)")
    ap.add_argument("--from-json", default=str(CLUSTER_JSON),
                    help="directory holding <space>.json from tools.ingest.cluster")
    args = ap.parse_args()

    src = Path(args.from_json)
    results = []
    for space in [s.strip() for s in args.spaces.split(",") if s.strip()]:
        f = src / f"{space}.json"
        if not f.exists():
            print(f"missing {f} — run tools.ingest.cluster --space {space} --save",
                  file=sys.stderr)
            return 1
        results.append(read_json(f))

    n = args.version or next_version()
    out = render_version(results, read_json(INSPIRATION_JSON), INSPO / f"cluster-{n}")
    print(f"CLUSTER_VERSION {out}")
    for res in results:
        print(f"  {res['space']}: {len(res['sites'])} notes -> {out / res['space']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
