"""graph.json: every node, edge and group must line up, and titles must be cached
by membership so an unchanged clustering never pays for re-titling."""
import json

import pytest

from tools.ingest import export_graph as eg


def doc_with(n=24):
    sd = {"_schema": {}}
    kinds = ["portfolio", "newsletter", "library"]
    for i in range(n):
        k = kinds[i % 3]
        sd[f"s{i}.com"] = {
            "url": f"https://s{i}.com", "title": f"S{i}",
            "what_it_is": f"A {k} site number {i} about {k} things.",
            "how_its_designed": f"{k} design with type {i % 4} and colour {i % 5}.",
            "palette": "black on white", "fonts": "Inter",
            "essence": {"subject": f"S{i}", "host": None, "does": "x", "for_whom": "y",
                        "domain": k, "kind": k},
        }
    return {"site_designs": sd}


def fake_titler(calls):
    def t(result, doc):
        calls.append(result["space"])
        return {p: f"{result['space']} group {p}" for p in eg.members_by_path(result)}
    return t


@pytest.fixture
def graph():
    calls = []
    g, changed = eg.build_graph(doc_with(), provider="hash", titler=fake_titler(calls),
                                cache={}, log=lambda m: None)
    return g, calls, changed


def test_both_views_cover_their_sites(graph):
    g, _, _ = graph
    assert set(g["views"]) == {"purpose", "design"}
    for v in g["views"].values():
        assert len(v["nodes"]) == 24


def test_every_edge_and_group_reference_resolves(graph):
    g, _, _ = graph
    for v in g["views"].values():
        ids = {n["id"] for n in v["nodes"]}
        gids = {x["id"] for x in v["groups"]}
        fids = {x["id"] for x in v["families"]}
        assert all(n["group"] in gids and n["family"] in fids for n in v["nodes"])
        assert all(e["source"] in ids and e["target"] in ids for e in v["edges"])
        assert all(e["kind"] in ("cluster", "sibling", "bridge") for e in v["edges"])
        assert all(x["color"].startswith("#") and len(x["color"]) == 7 for x in v["groups"])


def test_site_details_are_shared_once_with_essence(graph):
    g, _, _ = graph
    assert len(g["sites"]) == 24
    assert g["sites"]["s0.com"]["essence"]["domain"] == "portfolio"
    assert g["sites"]["s0.com"]["url"] == "https://s0.com"


def test_unchanged_membership_reuses_titles_without_calling_sonnet():
    cache, calls = {}, []
    eg.build_graph(doc_with(), provider="hash", titler=fake_titler(calls), cache=cache,
                   log=lambda m: None)
    first = len(calls)
    _, changed = eg.build_graph(doc_with(), provider="hash", titler=fake_titler(calls),
                                cache=cache, log=lambda m: None)
    assert first == 2 and len(calls) == 2, "second run must not re-title"
    assert changed is False


def test_graph_is_json_serialisable(graph):
    g, _, _ = graph
    assert json.loads(json.dumps(g))


def test_a_titling_failure_falls_back_instead_of_crashing():
    """An expired claude login once stalled the daemon; the export must survive it."""
    def broken(result, doc):
        raise RuntimeError("Failed to authenticate: OAuth session expired")
    cache = {}
    g, changed = eg.build_graph(doc_with(), provider="hash", titler=broken, cache=cache,
                                log=lambda m: None)
    assert changed is False and cache == {}, "fallback names must not be cached"
    assert all(x["name"] for v in g["views"].values() for x in v["groups"])
