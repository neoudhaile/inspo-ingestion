"""Rendering a clustering run as Obsidian vaults.

The load-bearing property: every node in the graph is a website. Anything that could
become a node and isn't a site — a tag, an unresolved link — is a bug, because
removing theme-nodes from the graph is the point of the redesign.
"""
import json
import re

import pytest

from tools.ingest import render_clusters as rc


@pytest.fixture
def result():
    return {
        "space": "design", "provider": "gemini", "model": "m",
        "levels": [2, 4], "k": 2,
        "sites": {
            "a.com": {"path": "1.1", "neighbors": [{"domain": "b.com", "score": 0.91}]},
            "b.com": {"path": "1.1", "neighbors": [{"domain": "a.com", "score": 0.91}]},
            "c.com": {"path": "2.1", "neighbors": [{"domain": "a.com", "score": 0.4}]},
        },
        "cluster_names": {"1": "warm paper", "1.1": "terracotta ink",
                          "2": "stark mono", "2.1": "default blue"},
    }


@pytest.fixture
def doc():
    return {"site_designs": {
        "a.com": {"url": "https://a.com", "title": "A", "how_its_designed": "Warm.",
                  "what_it_is": "A thing.", "screenshot": "screenshots/a.png"},
        "b.com": {"url": "https://b.com", "title": "B", "how_its_designed": "Also warm."},
        "c.com": {"url": "https://c.com", "title": "C", "how_its_designed": "Stark."},
    }}


def test_next_version_skips_existing(tmp_path):
    assert rc.next_version(tmp_path) == 1
    (tmp_path / "cluster-1").mkdir()
    (tmp_path / "cluster-2").mkdir()
    assert rc.next_version(tmp_path) == 3


def test_tags_for_gives_one_tag_per_level():
    assert rc.tags_for("3.2.1") == ["cluster/3", "cluster/3-2", "cluster/3-2-1"]


def test_graph_config_hides_tags_so_they_cannot_become_nodes():
    g = rc.graph_config(["1", "2", "3"])
    assert g["showTags"] is False
    assert len(g["colorGroups"]) == 3
    assert g["colorGroups"][0]["query"] == "tag:#cluster/1"


def test_cluster_colors_are_distinct():
    cols = {rc.cluster_color(i, 8) for i in range(8)}
    assert len(cols) == 8


def test_note_links_only_to_other_sites(result, doc):
    note = rc.render_note("a.com", doc["site_designs"]["a.com"],
                          result["sites"]["a.com"], result["cluster_names"],
                          "design", "../../../screenshots")
    links = re.findall(r"\[\[([^\]]+)\]\]", note)
    assert links == ["b.com"], "a wikilink to anything but a site would add a node"


def test_note_leads_with_the_space_and_keeps_the_rest(result, doc):
    note = rc.render_note("a.com", doc["site_designs"]["a.com"],
                          result["sites"]["a.com"], result["cluster_names"],
                          "design", "../../../screenshots")
    assert note.index("How it's designed") < note.index("Everything else")
    assert "A thing." in note, "the other half of the teardown must still be there"


def test_render_version_writes_both_vaults_and_a_readme(result, doc, tmp_path):
    out = rc.render_version([result], doc, tmp_path / "cluster-1")
    assert (out / "README.md").exists()
    assert (out / "design" / "INDEX.md").exists()
    assert (out / "design" / ".obsidian" / "graph.json").exists()
    assert {p.stem for p in (out / "design").glob("*.md")} == {
        "a.com", "b.com", "c.com", "INDEX"}


def test_every_wikilink_resolves_to_a_note(result, doc, tmp_path):
    """An unresolved link still draws a node in Obsidian, so none may dangle."""
    out = rc.render_version([result], doc, tmp_path / "cluster-1")
    notes = {p.stem for p in (out / "design").glob("*.md")}
    for p in (out / "design").glob("*.md"):
        for link in re.findall(r"\[\[([^\]]+)\]\]", p.read_text()):
            assert link in notes, f"{p.name} links to missing note {link}"


def test_readme_records_the_settings_that_made_this_version(result, doc, tmp_path):
    out = rc.render_version([result], doc, tmp_path / "cluster-1")
    txt = (out / "README.md").read_text()
    assert "gemini:m" in txt and "[2, 4]" in txt and "k: `2`" in txt


def test_graph_json_is_valid_json(result, doc, tmp_path):
    out = rc.render_version([result], doc, tmp_path / "cluster-1")
    json.loads((out / "design" / ".obsidian" / "graph.json").read_text())
