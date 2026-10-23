#!/usr/bin/env python3
"""Export the whole library as one graph.json for the web UI and for agents.

`inspo/graph.json` is a generated view of inspiration.json, like the vault. It is
written into inspo/ deliberately: the daemon owns inspo/ and screenshots/ and treats
anything else as a hand edit, so a data file anywhere else would stall every sync.

Shape:

    {
      "generated_at": "...",
      "sites": { "<domain>": { title, url, what_it_is, essence{...}, how_its_designed,
                               palette, fonts, tech_stack, screenshot } },
      "views": {
        "purpose": { "families": [...], "groups": [...], "nodes": [...], "edges": [...] },
        "design":  { ... }
      }
    }

Site details live once under "sites"; each view only says where a site sits and what
links it. Edges carry a `kind`: "cluster" (same group), "sibling" (same family) or
"bridge" (across families, only when as strong as a typical in-group link).

Group titles cost a Sonnet call, so they are cached by membership: a group whose
members haven't changed keeps its title across runs, and nothing is re-titled unless
the clustering actually moved.
"""
import argparse
import hashlib
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tools.ingest.cluster import (bridge_edges, cluster_space, structured_edges)
from tools.ingest.cluster_titles import family_palette, title_clusters
from tools.ingest.config import INSPIRATION_JSON, INSPO
from tools.ingest.embed import embed_space
from tools.ingest.jsonio import read_json, write_json_atomic

GRAPH_JSON = INSPO / "graph.json"
TITLE_CACHE = INSPO / "_clusters" / "titles_cache.json"
LEVELS = (8, 22)

SITE_FIELDS = ("title", "url", "what_it_is", "how_its_designed", "palette", "fonts",
               "tech_stack", "screenshot")


def _key(p):
    return tuple(int(x) for x in p.split("."))


def members_by_path(result):
    out = {}
    for dom, info in result["sites"].items():
        parts = info["path"].split(".")
        for i in range(len(parts)):
            out.setdefault(".".join(parts[:i + 1]), []).append(dom)
    return out


def membership_key(space, members):
    return hashlib.sha1((space + "|" + ",".join(sorted(members))).encode()).hexdigest()


def cached_titles(result, doc, cache, titler, log=print):
    """Titles for every cluster, reusing any whose membership is unchanged."""
    space = result["space"]
    mem = members_by_path(result)
    keys = {p: membership_key(space, m) for p, m in mem.items()}
    if all(k in cache for k in keys.values()):
        log(f"  {space}: all {len(keys)} titles reused (membership unchanged)")
        return {p: cache[k] for p, k in keys.items()}, False
    log(f"  {space}: titling {len(keys)} clusters…")
    try:
        titles = titler(result, doc)
    except Exception as exc:                  # noqa: BLE001 - degrade, never fail a run
        # Titling needs a working `claude` login. If it is down (an expired OAuth
        # session stalled the daemon for days once), keep what's cached and fall back
        # to keyword names for the rest. Fallbacks are NOT cached, so real titles
        # replace them on the first run after the login is fixed.
        log(f"  {space}: titling unavailable ({str(exc)[:80]}); using keyword names")
        names = result.get("cluster_names") or {}
        return {p: cache.get(k) or names.get(p) or p for p, k in keys.items()}, False
    for p, k in keys.items():
        cache[k] = titles[p]
    return titles, True


def build_view(result, titles, vecs_by_dom):
    """One view's families, groups, nodes and typed edges."""
    paths = {d: i["path"] for d, i in result["sites"].items()}
    all_paths = set(members_by_path(result))
    colours = family_palette(all_paths, titles)
    mem = members_by_path(result)

    families = [{"id": p, "name": titles.get(p, p), "size": len(mem[p])}
                for p in sorted((p for p in all_paths if "." not in p), key=_key)]
    groups = [{"id": p, "name": titles.get(p, p), "family": p.split(".")[0],
               "color": f"#{colours[p]:06x}", "size": len(mem[p]),
               "mixed": str(titles.get(p, "")).lower().startswith("mixed")}
              for p in sorted(colours, key=_key)]
    leaf_of = {}
    for d, p in paths.items():
        # a site's colour group is its path cut to the colour level
        depth = len(groups[0]["id"].split(".")) if groups else 1
        leaf_of[d] = ".".join(p.split(".")[:depth])

    nodes = [{"id": d, "group": leaf_of[d], "family": paths[d].split(".")[0],
              "path": paths[d]} for d in sorted(paths)]

    doms = [d for d in sorted(paths) if d in vecs_by_dom]
    vecs = [vecs_by_dom[d] for d in doms]
    edges, seen = [], set()
    if doms:
        se = structured_edges(doms, vecs, paths)
        inner = sorted(sc for d, l in se.items() for o, sc in l if paths[o] == paths[d])
        threshold = inner[len(inner) // 2] if inner else 1.0
        for d, lst in se.items():
            for o, sc in lst:
                k = tuple(sorted((d, o)))
                if k in seen:
                    continue
                seen.add(k)
                kind = "cluster" if paths[d] == paths[o] else "sibling"
                edges.append({"source": k[0], "target": k[1], "kind": kind,
                              "w": round(sc, 4)})
        for a, b, sc in bridge_edges(doms, vecs, paths, threshold):
            k = tuple(sorted((a, b)))
            if k in seen:
                continue
            seen.add(k)
            edges.append({"source": k[0], "target": k[1], "kind": "bridge",
                          "w": round(sc, 4)})
    return {"families": families, "groups": groups, "nodes": nodes, "edges": edges}


def site_details(doc, domains):
    sd = doc["site_designs"]
    out = {}
    for d in sorted(domains):
        e = sd.get(d) or {}
        row = {k: e.get(k) for k in SITE_FIELDS if e.get(k)}
        if e.get("essence"):
            row["essence"] = e["essence"]
        if e.get("site_state"):
            row["site_state"] = e["site_state"].get("state")
        out[d] = row
    return out


def build_graph(doc, provider="gemini", titler=None, cache=None, log=print):
    titler = titler or (lambda result, doc: title_clusters(result, doc))
    cache = {} if cache is None else cache
    views, all_doms, changed = {}, set(), False
    for space in ("purpose", "design"):
        result = cluster_space(space, provider=provider, levels=LEVELS, doc=doc,
                               log=lambda m: None)
        titles, did = cached_titles(result, doc, cache, titler, log)
        changed |= did
        doms, vecs = embed_space(space, provider=provider, doc=doc, log=lambda m: None)
        views[space] = build_view(result, titles, dict(zip(doms, vecs)))
        all_doms |= set(result["sites"])
        v = views[space]
        log(f"  {space}: {len(v['nodes'])} sites, {len(v['groups'])} groups, "
            f"{len(v['edges'])} edges "
            f"({sum(e['kind'] == 'bridge' for e in v['edges'])} bridges)")
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "sites": site_details(doc, all_doms),
        "views": views,
    }, changed


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--provider", default="gemini")
    ap.add_argument("--out", default=str(GRAPH_JSON))
    args = ap.parse_args()
    doc = read_json(INSPIRATION_JSON)
    cache = read_json(TITLE_CACHE) if TITLE_CACHE.exists() else {}
    graph, changed = build_graph(doc, provider=args.provider, cache=cache)
    if changed:
        TITLE_CACHE.parent.mkdir(parents=True, exist_ok=True)
        write_json_atomic(TITLE_CACHE, cache)
    write_json_atomic(Path(args.out), graph)
    print(f"GRAPH_EXPORTED {args.out} ({len(graph['sites'])} sites)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
