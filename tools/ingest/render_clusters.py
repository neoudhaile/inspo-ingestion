#!/usr/bin/env python3
"""Render a clustering run as browsable Obsidian vaults, one numbered folder per try.

This is the feedback loop for the clustering spike. Each run writes

    inspo/cluster-<n>/
        purpose/     <- open this as an Obsidian vault
        design/      <- and this one
        README.md    <- the settings that produced them, and the cluster sizes
        titles.json  <- the human title of every cluster (see cluster_titles.py)

so a reclustering never overwrites the last one and two attempts can be compared
side by side. Numbering is automatic: the next unused n.

The graph model, which is the whole point:

- Every node is a website. Nothing else gets a note, so nothing else can become a
  node — no `dark`, no `minimal`, no theme hubs. That was the explicit ask.
- Edges are each site's nearest neighbours in embedding space, symmetrized. Sites sit
  near the sites they actually resemble, not near the sites that happen to share a
  tag.
- Cluster membership rides in frontmatter as a NAMED, nested tag —
  `#portfolios-and-studios/design-studios` — which the graph config uses for colour
  only, with tag display switched off. Tags that are never displayed cannot become
  nodes. The name has to be in the tag because Obsidian's colour groups have no label
  field: the group shows its query, so `tag:#portfolios-and-studios` IS the label.

`--relabel cluster-<n>` names an existing version in place: it rebuilds the result
from that vault's own notes, so the clustering is exactly what was rendered even when
the intermediate JSON has since been overwritten. The owner's graph settings (forces,
zoom) are kept; only the colour groups are replaced.
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
from tools.ingest.jsonio import read_json, write_json_atomic

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


def _key(p):
    return tuple(int(x) for x in p.split("."))


def next_version(base=INSPO):
    n = 1
    while (base / f"cluster-{n}").exists():
        n += 1
    return n


def cluster_color(i, total):
    """Evenly spaced hues as the integer Obsidian's graph config wants."""
    r, g, b = colorsys.hsv_to_rgb((i / max(total, 1)) % 1.0, 0.62, 0.95)
    return (int(r * 255) << 16) + (int(g * 255) << 8) + int(b * 255)


DEFAULT_GRAPH = {
    "collapse-filter": True, "search": "", "showTags": False,
    "showAttachments": False, "hideUnresolved": True, "showOrphans": True,
    "collapse-color-groups": False,
    "collapse-display": False, "showArrow": False, "textFadeMultiplier": -0.7,
    "nodeSizeMultiplier": 1.4, "lineSizeMultiplier": 0.7,
    "collapse-forces": False, "centerStrength": 0.42, "repelStrength": 12,
    "linkStrength": 0.75, "linkDistance": 180, "scale": 0.55,
    "close": False,
}


def graph_config(top_tags, existing=None):
    """An .obsidian/graph.json, one colour group per top-level cluster.

    `top_tags` is ordered, one tag per top-level cluster. When the vault already has
    a graph.json (the owner has opened it and tuned forces or zoom), everything in it
    is kept and only the colour groups are replaced. showTags is false on purpose for
    a fresh vault: a displayed tag would appear as a node.
    """
    g = dict(existing) if existing else dict(DEFAULT_GRAPH)
    g["colorGroups"] = [
        {"query": f"tag:#{t}", "color": {"a": 1, "rgb": cluster_color(i, len(top_tags))}}
        for i, t in enumerate(top_tags)
    ]
    return g


def numeric_tags(paths):
    """Fallback when there are no titles: 3.2 -> cluster/3, cluster/3-2."""
    return {p: "cluster/" + p.replace(".", "-") for p in paths}


def tags_for(path, tagmap):
    """One tag per level of `path`, so a note carries its parent's tag too."""
    parts = path.split(".")
    return [tagmap[".".join(parts[:i + 1])] for i in range(len(parts))]


def yaml_str(s):
    return '"' + str(s).replace('"', "'") + '"'


def render_note(dom, entry, info, labels, tagmap, space, screenshot_rel):
    path = info["path"]
    lead = LEAD_FIELDS[space]
    lead_keys = {k for k, _ in lead}
    parts = path.split(".")
    trail = [labels.get(".".join(parts[:i + 1]), "") for i in range(len(parts))]

    fm = ["---",
          f"domain: {dom}",
          f"url: {entry.get('url', '')}",
          f"title: {yaml_str(entry.get('title') or dom)}",
          f"cluster: {yaml_str(path)}",
          f"cluster_name: {yaml_str(labels.get(path, ''))}"]
    for depth, name in enumerate(trail):
        fm.append(f"cluster_l{depth + 1}: {yaml_str(name)}")
    fm += ["tags:"] + [f"  - {t}" for t in tags_for(path, tagmap)] + ["---", ""]

    body = [f"# {entry.get('title') or dom}",
            f"> [{dom}]({entry.get('url', '')}) · **{' › '.join(n for n in trail if n)}**",
            ""]

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


def render_index(result, labels, tagmap):
    sites = result["sites"]
    by_path = {}
    for d, info in sites.items():
        by_path.setdefault(info["path"], []).append(d)

    out = [f"# {result['space'].capitalize()} clusters", "",
           f"_{len(sites)} sites · {result['provider']}:{result['model']} · "
           f"cuts {result['levels']} · k={result['k']}._", "",
           "Open this folder as an Obsidian vault, then Graph view. Leave **Tags** "
           "off — every node is a website, and the cluster tags are here only to "
           "colour them.", ""]
    seen = set()
    for leaf in sorted(by_path, key=_key):
        parts = leaf.split(".")
        for depth in range(len(parts)):
            prefix = ".".join(parts[:depth + 1])
            if prefix in seen:
                continue
            seen.add(prefix)
            size = sum(len(v) for p, v in by_path.items()
                       if p == prefix or p.startswith(prefix + "."))
            out.append(f"{'  ' * depth}- **{labels.get(prefix, prefix)}** ({size}) "
                       f"`#{tagmap[prefix]}`")
            if depth == len(result["levels"]) - 1:
                for m in sorted(by_path.get(prefix, [])):
                    out.append(f"{'  ' * depth}    - [[{m}]]")
    return "\n".join(out) + "\n"


def all_paths(result):
    out = set()
    for info in result["sites"].values():
        parts = info["path"].split(".")
        out.update(".".join(parts[:i + 1]) for i in range(len(parts)))
    return out


def labels_and_tags(result):
    """(labels, tagmap) for a result: human titles when present, else keyword names."""
    from tools.ingest.cluster_titles import named_tags
    titles = result.get("cluster_titles") or {}
    paths = all_paths(result)
    if titles and paths <= set(titles):
        return titles, named_tags({p: titles[p] for p in paths})
    names = result.get("cluster_names") or {}
    return {p: names.get(p, "") for p in paths}, numeric_tags(paths)


def render_space(result, doc, outdir):
    labels, tagmap = labels_and_tags(result)
    sd = doc["site_designs"]
    outdir.mkdir(parents=True, exist_ok=True)
    # Path back to screenshots/ from inside this folder. relpath rather than
    # relative_to: the output directory is not always under the repo (tests render
    # to a tmpdir), and relative_to raises rather than coping.
    screenshot_rel = os.path.relpath(REPO / "screenshots", outdir).replace(os.sep, "/")

    for dom, info in result["sites"].items():
        entry = sd.get(dom) or {}
        (outdir / f"{dom}.md").write_text(
            render_note(dom, entry, info, labels, tagmap, result["space"], screenshot_rel))

    (outdir / "INDEX.md").write_text(render_index(result, labels, tagmap))

    tops = sorted({i["path"].split(".")[0] for i in result["sites"].values()}, key=int)
    obs = outdir / ".obsidian"
    obs.mkdir(exist_ok=True)
    gpath = obs / "graph.json"
    existing = None
    if gpath.exists():
        try:
            existing = json.loads(gpath.read_text())
        except ValueError:
            existing = None
    gpath.write_text(json.dumps(graph_config([tagmap[t] for t in tops], existing), indent=2))
    return len(result["sites"])


def render_version(results, doc, version_dir):
    version_dir.mkdir(parents=True, exist_ok=True)
    lines = [f"# {version_dir.name}", "",
             "Two Obsidian vaults from one clustering run. Open "
             f"`{version_dir.name}/purpose` or `{version_dir.name}/design` as a vault "
             "(File → Open folder as vault), then Graph view with **Tags off**.", ""]
    titles_out = {}
    for res in results:
        n = render_space(res, doc, version_dir / res["space"])
        labels, tagmap = labels_and_tags(res)
        if res.get("cluster_titles"):
            titles_out[res["space"]] = res["cluster_titles"]
        sizes = Counter(i["path"].split(".")[0] for i in res["sites"].values())
        ordered = [sizes[k] for k in sorted(sizes, key=int)]
        mixed = sum(1 for p in labels if str(labels[p]).lower().startswith("mixed"))
        lines += [f"## {res['space']} ({n} sites)", "",
                  f"- model: `{res['provider']}:{res['model']}`",
                  f"- cuts: `{res['levels']}` · k: `{res['k']}`",
                  f"- top-level sizes: `{ordered}` "
                  f"(largest {max(ordered) / n:.0%})"]
        if titles_out.get(res["space"]):
            lines.append(f"- clusters titled \"Mixed:\" (members share no clear theme): "
                         f"`{mixed}` of `{len(labels)}`")
        lines.append("")
        for top in sorted(sizes, key=int):
            lines.append(f"  - **{labels.get(top, top)}** ({sizes[top]}) `#{tagmap[top]}`")
            for sub in sorted((p for p in labels if p.startswith(top + ".")
                               and p.count(".") == 1), key=_key):
                cnt = sum(1 for i in res["sites"].values()
                          if i["path"] == sub or i["path"].startswith(sub + "."))
                lines.append(f"    - {labels.get(sub, sub)} ({cnt})")
        lines.append("")
    (version_dir / "README.md").write_text("\n".join(lines))
    if titles_out:
        write_json_atomic(version_dir / "titles.json", titles_out)
    return version_dir


# --- rebuilding a result from a rendered vault -----------------------------------

FM_PATH = re.compile(r'^cluster: "([^"]+)"', re.M)
FM_LEVEL = re.compile(r'^cluster_l(\d+): "([^"]*)"', re.M)
NEIGHBOR = re.compile(r"^- \[\[([^\]]+)\]\] — ([0-9.]+)$", re.M)


def result_from_vault(space_dir):
    """Reconstruct a cluster result from the notes of one rendered space.

    The vault is the record of what the owner is looking at; the intermediate JSON
    in inspo/_clusters/ is overwritten by every run. Relabelling from the notes is
    the only way to name a version without silently reclustering it.
    """
    space_dir = Path(space_dir)
    sites, names = {}, {}
    for f in sorted(space_dir.glob("*.md")):
        if f.stem == "INDEX":
            continue
        t = f.read_text()
        m = FM_PATH.search(t)
        if not m:
            continue
        path = m.group(1)
        parts = path.split(".")
        for lvl, name in FM_LEVEL.findall(t):
            names.setdefault(".".join(parts[:int(lvl)]), name)
        nb_block = t.split("## Nearest in this space", 1)[-1].split("\n## ", 1)[0]
        sites[f.stem] = {"path": path, "neighbors": [
            {"domain": d, "score": float(s)} for d, s in NEIGHBOR.findall(nb_block)]}
    readme = (space_dir.parent / "README.md")
    meta = {"provider": "?", "model": "?", "levels": [], "k": 0}
    if readme.exists():
        r = readme.read_text()
        sec = r.split(f"## {space_dir.name}", 1)[-1]
        mm = re.search(r"model: `([^:`]+):([^`]+)`", sec)
        if mm:
            meta["provider"], meta["model"] = mm.group(1), mm.group(2)
        mc = re.search(r"cuts: `\[([0-9, ]+)\]` · k: `(\d+)`", sec)
        if mc:
            meta["levels"] = [int(x) for x in mc.group(1).split(",")]
            meta["k"] = int(mc.group(2))
    return {"space": space_dir.name, **meta, "sites": sites, "cluster_names": names}


# --- CLI ------------------------------------------------------------------------

def add_titles(results, doc, version_dir, retitle=False, log=print):
    """Attach human titles, reusing titles.json when it already covers a space."""
    from tools.ingest.cluster_titles import title_clusters
    cached = {}
    tfile = version_dir / "titles.json"
    if tfile.exists() and not retitle:
        cached = read_json(tfile)
    for res in results:
        prev = cached.get(res["space"]) or {}
        if prev and all_paths(res) <= set(prev):
            res["cluster_titles"] = prev
            log(f"  {res['space']}: titles reused from {tfile.name}")
            continue
        log(f"  {res['space']}: titling {len(all_paths(res))} clusters with Sonnet…")
        res["cluster_titles"] = title_clusters(res, doc)
    return results


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--spaces", default="purpose,design")
    ap.add_argument("--version", type=int, default=None,
                    help="cluster-N to write (default: next unused)")
    ap.add_argument("--from-json", default=str(CLUSTER_JSON),
                    help="directory holding <space>.json from tools.ingest.cluster")
    ap.add_argument("--relabel", default=None, metavar="cluster-N",
                    help="name an existing version in place, without reclustering")
    ap.add_argument("--no-titles", action="store_true",
                    help="skip Sonnet titles; fall back to keyword names")
    ap.add_argument("--retitle", action="store_true",
                    help="ignore titles.json and ask for new titles")
    args = ap.parse_args()

    doc = read_json(INSPIRATION_JSON)
    spaces = [s.strip() for s in args.spaces.split(",") if s.strip()]

    if args.relabel:
        out = INSPO / args.relabel
        if not out.is_dir():
            print(f"no such version: {out}", file=sys.stderr)
            return 1
        results = [result_from_vault(out / s) for s in spaces if (out / s).is_dir()]
    else:
        src = Path(args.from_json)
        results = []
        for space in spaces:
            f = src / f"{space}.json"
            if not f.exists():
                print(f"missing {f} — run tools.ingest.cluster --space {space} --save",
                      file=sys.stderr)
                return 1
            results.append(read_json(f))
        out = INSPO / f"cluster-{args.version or next_version()}"

    if not args.no_titles:
        add_titles(results, doc, out, retitle=args.retitle)
    render_version(results, doc, out)
    print(f"CLUSTER_VERSION {out}")
    for res in results:
        labels, tagmap = labels_and_tags(res)
        print(f"\n  {res['space']}: {len(res['sites'])} notes -> {out / res['space']}")
        tops = sorted({i['path'].split('.')[0] for i in res['sites'].values()}, key=int)
        for t in tops:
            print(f"    tag:#{tagmap[t]:44}  {labels.get(t, '')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
