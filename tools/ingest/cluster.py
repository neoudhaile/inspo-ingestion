#!/usr/bin/env python3
"""Cluster sites from their embeddings — clusters discovered, not declared.

The vault's four hand-maintained facets could not answer the searches that matter,
and `pattern_keywords`, the one extensible field, collapsed into 930 terms of which
746 were used exactly once. Both failures come from asking people (or a model) to
name categories up front. This module asks the geometry instead.

Why agglomerative clustering rather than the usual UMAP + HDBSCAN stack: at 201
sites, dimensionality reduction buys nothing and costs determinism — UMAP and
HDBSCAN are stochastic, and this pipeline rebuilds every artifact from scratch on
every daemon run. Average-linkage agglomerative clustering over cosine distance is
exactly deterministic, needs no seed, and produces a dendrogram, which *is*
"clusters within clusters": any coarse cut is refined by every finer cut, so the
nesting is guaranteed rather than hoped for.

Two outputs, both consumed later by the vault renderer:

  levels    each site's cluster path, e.g. 3 / 3.2 / 3.2.1  (the nesting)
  neighbors each site's k nearest sites, with scores        (the graph edges)

Cluster names are generated from the text the cluster actually contains (a
class-based TF-IDF: terms frequent inside the cluster and rare outside it), so the
vocabulary grows by itself and nobody maintains a taxonomy.
"""
import argparse
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from scipy.cluster.hierarchy import fcluster, linkage

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tools.ingest.config import INSPIRATION_JSON, INSPO
from tools.ingest.embed import DEFAULT_MODELS, SPACES, corpus, embed_texts
from tools.ingest.jsonio import read_json, write_json_atomic

OUT_DIR = INSPO / "_clusters"

# Cuts of the same dendrogram, coarse to fine. Finer cuts strictly refine coarser
# ones, which is what makes "clusters within clusters" true rather than aspirational.
DEFAULT_LEVELS = (6, 18, 40)
DEFAULT_K = 6

STOP = set("""
a an the and or but of to in on for with from by at as is are was were be been being
it its this that these those they them their there here what which who whom how why
when where all any both each few more most other some such no nor not only own same
so than too very can will just should now s t don you your yours he she his her i me
my we us our site website page pages web one two three new use used using make makes
made get gets built build builds also into about across over under between

# Corpus-wide noise: every teardown mentions the tweet it came from, and nearly
# every site has a hero and a meta description. These are true of the corpus, not
# distinctive of any cluster, so they drown out real signal in the names.
tweet tweets hero meta description h1 h2 title dom own reads pitch link links
whose simply its the page's own

# DOM-probe vocabulary: measurements and element names describe how we looked at the
# site, not what the site is.
scrollheight innerheight documentelement viewport px rgb hsl hex css html svg iframe
canvas div span font fonts font-family weight weights height width color colors
mobile desktop scroll scrolls scrolling single-screen rum analytics probe fetch
""".split())

# No dots: hostnames like static.cloudflareinsights.com are infrastructure, not
# subject matter, and they were showing up as cluster names.
TOKEN = re.compile(r"[a-z][a-z0-9\-]{2,}")


# --- geometry -------------------------------------------------------------------

def normalize(vecs):
    a = np.asarray(vecs, dtype=np.float64)
    n = np.linalg.norm(a, axis=1, keepdims=True)
    n[n == 0] = 1.0
    return a / n


def cosine_sim(vecs):
    """Full pairwise cosine similarity. 201x201 — no need to be clever."""
    a = normalize(vecs)
    return np.clip(a @ a.T, -1.0, 1.0)


def dendrogram(vecs, method="ward"):
    """Hierarchical linkage over L2-normalized vectors. Deterministic; no seed.

    Ward by default, after average linkage was tried and produced one cluster holding
    183 of 201 sites plus a scatter of crumbs — the usual chaining failure. Ward
    minimises within-cluster variance, so it yields comparably-sized groups, which is
    what a browsable graph needs.

    Ward requires Euclidean distance, which is fine here precisely because the vectors
    are normalized first: on the unit sphere Euclidean distance is a monotonic
    function of cosine distance, so ranking by one ranks by the other.
    """
    a = normalize(vecs)
    if method == "ward":
        return linkage(a, method="ward", metric="euclidean")
    return linkage(a, method=method, metric="cosine")


def cut_levels(Z, n, levels=DEFAULT_LEVELS):
    """[labels per level], coarse to fine. Each finer cut refines the coarser one."""
    out = []
    for want in levels:
        k = max(1, min(int(want), n))
        out.append(fcluster(Z, t=k, criterion="maxclust"))
    return out


def paths(level_labels):
    """Per-item nested path like '3.2.1', built from the cut labels.

    Renumbers each level within its parent so the path reads as a tree rather than
    as unrelated global ids.
    """
    n = len(level_labels[0])
    out = [[] for _ in range(n)]
    parent_key = [()] * n
    for labels in level_labels:
        groups = {}
        for i in range(n):
            groups.setdefault((parent_key[i], labels[i]), []).append(i)
        # stable: order children by size then by first member, so ids don't jitter
        ordered = sorted(groups.items(), key=lambda kv: (kv[0][0], -len(kv[1]), kv[1][0]))
        counter = Counter()
        for (pkey, _), members in ordered:
            counter[pkey] += 1
            cid = counter[pkey]
            for i in members:
                out[i].append(cid)
                parent_key[i] = tuple(out[i])
    return [".".join(str(c) for c in p) for p in out]


def knn(sims, doms, k=DEFAULT_K):
    """Each site's k nearest others, symmetrized.

    Symmetrizing matters: a raw kNN graph is directed, and an unreciprocated edge
    still pulls two nodes together in a force layout, so leaving it asymmetric makes
    the picture depend on arbitrary tie-breaks.
    """
    n = len(doms)
    chosen = set()
    scores = {}
    for i in range(n):
        order = np.argsort(-sims[i])
        picked = 0
        for j in order:
            if j == i:
                continue
            chosen.add((min(i, j), max(i, j)))
            scores[(min(i, j), max(i, j))] = float(sims[i][j])
            picked += 1
            if picked >= k:
                break
    out = {d: [] for d in doms}
    for (i, j) in chosen:
        s = scores[(i, j)]
        out[doms[i]].append((doms[j], s))
        out[doms[j]].append((doms[i], s))
    for d in out:
        out[d].sort(key=lambda x: -x[1])
    return out


# --- naming ---------------------------------------------------------------------

def tokenize(text):
    return [t for t in TOKEN.findall(text.lower()) if t not in STOP and not t.isdigit()]


def name_clusters(texts, labels, top=4):
    """Class-based TF-IDF: terms frequent in a cluster and rare everywhere else.

    This is how the vocabulary grows without anyone curating it — a new kind of site
    produces a new cluster, and the cluster names itself from its own words.
    """
    groups = {}
    for t, lab in zip(texts, labels):
        groups.setdefault(lab, []).append(t)
    df = Counter()
    per = {}
    for lab, docs in groups.items():
        c = Counter()
        for d in docs:
            c.update(set(tokenize(d)))
        per[lab] = c
        for term in c:
            df[term] += 1
    ngroups = len(groups)
    names = {}
    for lab, c in per.items():
        size = len(groups[lab])
        scored = []
        for term, cnt in c.items():
            if cnt < max(2, size * 0.25):
                continue
            tf = cnt / size
            idf = math.log(1 + ngroups / df[term])
            scored.append((tf * idf, term))
        scored.sort(reverse=True)
        # Drop near-duplicates: "browser-default-blue browser-default" reads as a
        # stutter and spends two of four slots saying one thing.
        picked = []
        for _, term in scored:
            if any(term in p or p in term for p in picked):
                continue
            picked.append(term)
            if len(picked) >= top:
                break
        names[lab] = " ".join(picked) or "misc"
    return names


# --- the run --------------------------------------------------------------------

def cluster_space(space, provider="gemini", model=None, levels=DEFAULT_LEVELS,
                  k=DEFAULT_K, doc=None, log=print, method="ward"):
    doc = doc if doc is not None else read_json(INSPIRATION_JSON)
    pairs = corpus(doc, space)
    doms = [d for d, _ in pairs]
    texts = [t for _, t in pairs]
    vecs = embed_texts(texts, provider=provider, model=model, log=log)

    sims = cosine_sim(vecs)
    Z = dendrogram(vecs, method)
    level_labels = cut_levels(Z, len(doms), levels)
    site_paths = paths(level_labels)
    neighbors = knn(sims, doms, k)

    # name every cluster at every level
    cluster_names = {}
    for depth in range(len(levels)):
        prefix_of = [".".join(p.split(".")[:depth + 1]) for p in site_paths]
        cluster_names.update(name_clusters(texts, prefix_of))

    return {
        "space": space,
        "provider": provider,
        "model": model or DEFAULT_MODELS[provider],
        "levels": list(levels),
        "k": k,
        "sites": {
            d: {"path": p, "neighbors": [{"domain": nd, "score": round(s, 4)}
                                         for nd, s in neighbors[d]]}
            for d, p in zip(doms, site_paths)
        },
        "cluster_names": cluster_names,
    }


def report(result, members_per_cluster=0):
    """Human-readable tree. members_per_cluster=0 means show all."""
    sites = result["sites"]
    names = result["cluster_names"]
    by_path = {}
    for d, info in sites.items():
        by_path.setdefault(info["path"], []).append(d)

    def sort_key(p):
        return tuple(int(x) for x in p.split("."))

    lines = [f"{result['space'].upper()} — {len(sites)} sites "
             f"({result['provider']}:{result['model']}, levels {result['levels']}, k={result['k']})",
             ""]
    seen = set()
    for leaf in sorted(by_path, key=sort_key):
        parts = leaf.split(".")
        for depth in range(len(parts)):
            prefix = ".".join(parts[:depth + 1])
            if prefix in seen:
                continue
            seen.add(prefix)
            size = sum(len(v) for p, v in by_path.items()
                       if p == prefix or p.startswith(prefix + "."))
            indent = "  " * depth
            lines.append(f"{indent}[{prefix}] ({size}) {names.get(prefix, '')}")
            if depth == len(result["levels"]) - 1:
                mem = sorted(by_path.get(prefix, []))
                shown = mem if not members_per_cluster else mem[:members_per_cluster]
                for m in shown:
                    lines.append(f"{indent}    · {m}")
                if len(mem) > len(shown):
                    lines.append(f"{indent}    … +{len(mem) - len(shown)} more")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--space", choices=SPACES + ("all",), default="all")
    ap.add_argument("--provider", default="gemini")
    ap.add_argument("--model", default=None)
    ap.add_argument("--levels", default=",".join(str(x) for x in DEFAULT_LEVELS))
    ap.add_argument("--k", type=int, default=DEFAULT_K)
    ap.add_argument("--method", default="ward", choices=("ward", "average", "complete"))
    ap.add_argument("--members", type=int, default=0,
                    help="members to list per leaf cluster (0 = all)")
    ap.add_argument("--save", action="store_true", help="write inspo/_clusters/<space>.json")
    args = ap.parse_args()

    levels = tuple(int(x) for x in args.levels.split(","))
    doc = read_json(INSPIRATION_JSON)
    for space in (SPACES if args.space == "all" else (args.space,)):
        res = cluster_space(space, args.provider, args.model, levels, args.k, doc,
                            log=lambda m: print(m, file=sys.stderr), method=args.method)
        print(report(res, args.members))
        print()
        if args.save:
            OUT_DIR.mkdir(parents=True, exist_ok=True)
            write_json_atomic(OUT_DIR / f"{space}.json", res)
            print(f"saved {OUT_DIR / (space + '.json')}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
