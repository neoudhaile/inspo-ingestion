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
- Cluster membership rides in frontmatter as NAMED tags — the family's and the
  cluster's, e.g. `#designer-and-studio-portfolios` and `#design-studios-and-agencies`
  — which the graph config uses for colour only, with tag display switched off. Tags
  that are never displayed cannot become nodes. The name has to be in the tag because
  Obsidian's colour groups have no label field: the query IS the label.
- One colour group per named cluster, hue by family and shade by sibling, so the
  graph reads as colour regions; "Mixed:" clusters are washed out.

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

# Screenshots are linked INTO each vault under this name. Obsidian cannot resolve a
# path outside the vault: the old `../../../screenshots/x.png` embeds never rendered,
# and each became an unresolved node in the graph. A symlinked folder makes them real
# attachments, which render in the note and stay out of the graph (attachments are
# hidden there by default).
SHOTS = "_screenshots"

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


def graph_config(groups, existing=None):
    """An .obsidian/graph.json with one colour group per (tag, rgb) in `groups`.

    When the vault already has a graph.json (the owner has opened it and tuned forces
    or zoom), everything in it is kept and only the colour groups are replaced.
    showTags is false on purpose for a fresh vault: a displayed tag becomes a node.
    Plain strings are accepted for `groups` and get evenly spaced colours.
    """
    g = dict(existing) if existing else dict(DEFAULT_GRAPH)
    pairs = [x if isinstance(x, tuple) else (x, cluster_color(i, len(groups)))
             for i, x in enumerate(groups)]
    g["colorGroups"] = [{"query": t if t.startswith(('"', "tag:")) else f"tag:#{t}",
                         "color": {"a": 1, "rgb": rgb}} for t, rgb in pairs]
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
        body.append(f"![{dom}]({SHOTS}/{Path(scr).name})\n")

    for key, label in lead:
        v = entry.get(key)
        if v:
            body += [f"**{label}.** {v}", ""]

    # Wikilinks ARE graph edges, so only the structured edges are links. The overall
    # nearest neighbours in other clusters are kept as plain text: still readable, no
    # pull on the layout.
    edges = info.get("graph_edges")
    if edges is None:
        edges = info.get("neighbors") or []
    bridges = info.get("bridges") or []
    linked = {n["domain"] for n in edges} | {n["domain"] for n in bridges}
    body += ["## Nearest in this space", ""]
    body += [f"- [[{n['domain']}]] — {n['score']:.3f}" for n in edges] or ["—"]
    body.append("")
    if bridges:
        body += ["## Bridges to other families", ""]
        body += [f"- [[{n['domain']}]] — {n['score']:.3f}" for n in bridges]
        body.append("")
    elsewhere = [n for n in (info.get("neighbors") or []) if n["domain"] not in linked
                 and n["domain"] in (info.get("_other_cluster") or ())]
    if elsewhere:
        body += ["## Also close, in other clusters", ""]
        body += [f"- {n['domain']} — {n['score']:.3f}" for n in elsewhere]
        body.append("")

    extra = [(k, l) for k, l in REST_FIELDS if k not in lead_keys and entry.get(k)]
    if extra:
        body += ["## Everything else", ""]
        for key, label in extra:
            body += [f"**{label}.** {entry[key]}", ""]

    if entry.get("tech_stack"):
        body += [f"**Tech.** {', '.join(entry['tech_stack'])}", ""]

    return "\n".join(fm + body)


def render_index(result, labels, tagmap, colours=None):
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
            # A swatch in the cluster's graph colour: the group panel truncates its
            # queries, so this is the one place colour and full name sit side by side.
            dot = (f'<span style="color:#{colours[prefix]:06x}">●</span> '
                   if colours and prefix in colours else "")
            out.append(f"{'  ' * depth}- {dot}**{labels.get(prefix, prefix)}** ({size}) "
                       f"`#{tagmap[prefix]}`")
            if depth == len(result["levels"]) - 1:
                # Plain names, NOT [[links]]: a link from INDEX to all 201 sites made
                # INDEX the biggest hub in the graph, pulling every site towards the
                # centre and breaking "every node is a website".
                for m in sorted(by_path.get(prefix, [])):
                    out.append(f"{'  ' * depth}    - {m}")
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

    shots = outdir / SHOTS
    if not shots.exists() and not shots.is_symlink() and (REPO / "screenshots").is_dir():
        os.symlink(os.path.relpath(REPO / "screenshots", outdir), shots)

    paths = {d: i["path"] for d, i in result["sites"].items()}
    for dom, info in result["sites"].items():
        info["_other_cluster"] = {o for o, p in paths.items() if p != info["path"]}
        entry = sd.get(dom) or {}
        (outdir / f"{dom}.md").write_text(
            render_note(dom, entry, info, labels, tagmap, result["space"], screenshot_rel))

    from tools.ingest.cluster_titles import family_palette
    colours = family_palette(all_paths(result), result.get("cluster_titles"))
    (outdir / "INDEX.md").write_text(render_index(result, labels, tagmap, colours))
    # Titled clusters are matched by their exact name as a quoted phrase, not by tag.
    # Tag queries matched nothing in practice: Obsidian's tag index lags behind a
    # rewrite of an open vault, while a phrase search reads the file itself. The
    # name is also what the panel then shows. Every note carries its cluster's name
    # in its header line and frontmatter; a test asserts no other note does.
    titled = bool(result.get("cluster_titles"))
    def query(p):
        return '"' + str(labels[p]).replace('"', "'") + '"' if titled else tagmap[p]
    groups = [(query(p), colours[p]) for p in sorted(colours, key=_key)]
    obs = outdir / ".obsidian"
    obs.mkdir(exist_ok=True)
    gpath = obs / "graph.json"
    existing = None
    if gpath.exists():
        try:
            existing = json.loads(gpath.read_text())
        except ValueError:
            existing = None
    gpath.write_text(json.dumps(graph_config(groups, existing), indent=2))
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
NEIGHBOR_TEXT = re.compile(r"^- ([^\[\s][^ ]*) — ([0-9.]+)$", re.M)


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
        nb = [(d, float(s)) for d, s in NEIGHBOR.findall(nb_block)]
        if "## Bridges to other families" in t:
            br = t.split("## Bridges to other families", 1)[1].split("\n## ", 1)[0]
            nb += [(d, float(s)) for d, s in NEIGHBOR.findall(br)]
        if "## Also close, in other clusters" in t:
            far = t.split("## Also close, in other clusters", 1)[1].split("\n## ", 1)[0]
            nb += [(d, float(s)) for d, s in NEIGHBOR_TEXT.findall(far)]
        seen, merged = set(), []
        for d, sc in sorted(nb, key=lambda x: -x[1]):
            if d not in seen:
                seen.add(d)
                merged.append({"domain": d, "score": sc})
        sites[f.stem] = {"path": path, "neighbors": merged}
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


def add_structured_edges(results, doc, log=print):
    """Attach in-cluster graph edges, computed from each space's embeddings.

    The edges only shape the layout; membership is whatever the version already has.
    Uses the current text recipe's vectors (cached, so mostly free). If embedding is
    unavailable, falls back to plain neighbours rather than failing the render.
    """
    from tools.ingest.cluster import bridge_edges, structured_edges
    from tools.ingest.embed import embed_space
    for res in results:
        try:
            doms, vecs = embed_space(res["space"], doc=doc, log=lambda m: None)
        except Exception as exc:              # noqa: BLE001 - degrade, don't fail
            log(f"  {res['space']}: no vectors ({exc}); keeping plain neighbours")
            continue
        paths = {d: i["path"] for d, i in res["sites"].items()}
        keep = [i for i, d in enumerate(doms) if d in paths]
        kd, kv = [doms[i] for i in keep], [vecs[i] for i in keep]
        edges = structured_edges(kd, kv, paths)
        inner = sorted(sc for d, l in edges.items() for o, sc in l if paths[o] == paths[d])
        threshold = inner[len(inner) // 2] if inner else 1.0
        bridges = bridge_edges(kd, kv, paths, threshold)
        brid = {}
        for a, b, sc in bridges:
            brid.setdefault(a, []).append((b, sc))
            brid.setdefault(b, []).append((a, sc))
        for d, info in res["sites"].items():
            info["graph_edges"] = [{"domain": o, "score": round(sc, 4)}
                                   for o, sc in edges.get(d, [])]
            info["bridges"] = [{"domain": o, "score": round(sc, 4)}
                               for o, sc in sorted(brid.get(d, []), key=lambda x: -x[1])]
        same = sum(len(v) for v in edges.values())
        log(f"  {res['space']}: {same // 2} in-cluster/sibling edges, "
            f"{len(bridges)} bridges across families (similarity >= {threshold:.3f})")
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
    ap.add_argument("--knn-edges", action="store_true",
                    help="link plain nearest neighbours instead of in-cluster edges")
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
    if not args.knn_edges:
        add_structured_edges(results, doc)
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
