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
    tm = rc.numeric_tags({"3", "3.2", "3.2.1"})
    assert rc.tags_for("3.2.1", tm) == ["cluster/3", "cluster/3-2", "cluster/3-2-1"]


def test_graph_config_hides_tags_so_they_cannot_become_nodes():
    g = rc.graph_config(["cluster/1", "cluster/2", "cluster/3"])
    assert g["showTags"] is False
    assert len(g["colorGroups"]) == 3
    assert g["colorGroups"][0]["query"] == "tag:#cluster/1"


def test_cluster_colors_are_distinct():
    cols = {rc.cluster_color(i, 8) for i in range(8)}
    assert len(cols) == 8


def test_note_links_only_to_other_sites(result, doc):
    labels, tm = rc.labels_and_tags(result)
    note = rc.render_note("a.com", doc["site_designs"]["a.com"],
                          result["sites"]["a.com"], labels, tm,
                          "design", "../../../screenshots")
    links = re.findall(r"\[\[([^\]]+)\]\]", note)
    assert links == ["b.com"], "a wikilink to anything but a site would add a node"


def test_note_leads_with_the_space_and_keeps_the_rest(result, doc):
    labels, tm = rc.labels_and_tags(result)
    note = rc.render_note("a.com", doc["site_designs"]["a.com"],
                          result["sites"]["a.com"], labels, tm,
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


# --- named clusters -------------------------------------------------------------

from tools.ingest import cluster_titles as ct

TITLES = {"1": "Warm paper and serif", "1.1": "Terracotta ink",
          "2": "Stark mono", "2.1": "Browser-default blue"}


def titled(result):
    r = dict(result); r["cluster_titles"] = dict(TITLES)
    return r


@pytest.mark.parametrize("title,slug", [
    ("Personal portfolios", "personal-portfolios"),
    ("Mixed: hardware, dev tools & aerospace", "mixed-hardware-dev-tools-aerospace"),
    ("  B2B   lead-gen!! ", "b2b-lead-gen"),
    ("2026", "c-2026"),
    ("", "cluster"),
])
def test_slug_tag(title, slug):
    assert ct.slug_tag(title) == slug


def test_named_tags_nest_children_under_their_parent():
    tm = ct.named_tags(TITLES)
    assert tm["1"] == "warm-paper-and-serif"
    assert tm["1.1"] == "warm-paper-and-serif/terracotta-ink"
    assert tm["2.1"] == "stark-mono/browser-default-blue"


def test_named_tags_keep_colliding_slugs_apart():
    tm = ct.named_tags({"1": "Portfolios", "2": "portfolios!", "1.1": "A", "1.2": "a"})
    assert tm["1"] != tm["2"]
    assert tm["1.1"] != tm["1.2"]


def test_titled_render_uses_named_tags_everywhere(result, doc, tmp_path):
    """The group query is the only label Obsidian shows, so the name must be the tag."""
    out = rc.render_version([titled(result)], doc, tmp_path / "cluster-1")
    note = (out / "design" / "a.com.md").read_text()
    assert "  - warm-paper-and-serif\n" in note
    assert "  - warm-paper-and-serif/terracotta-ink" in note
    assert "cluster/" not in note
    g = json.loads((out / "design" / ".obsidian" / "graph.json").read_text())
    assert [x["query"] for x in g["colorGroups"]] == ["tag:#warm-paper-and-serif",
                                                       "tag:#stark-mono"]
    assert "Warm paper and serif › Terracotta ink" in note


def test_titles_are_recorded_beside_the_version(result, doc, tmp_path):
    out = rc.render_version([titled(result)], doc, tmp_path / "cluster-1")
    assert json.loads((out / "titles.json").read_text())["design"] == TITLES
    assert "Stark mono" in (out / "README.md").read_text()


def test_untitled_render_falls_back_to_numeric_tags(result, doc, tmp_path):
    out = rc.render_version([result], doc, tmp_path / "cluster-1")
    assert "  - cluster/1-1" in (out / "design" / "a.com.md").read_text()


def test_partial_titles_fall_back_rather_than_half_rename(result, doc, tmp_path):
    r = dict(result); r["cluster_titles"] = {"1": "Only one"}
    out = rc.render_version([r], doc, tmp_path / "cluster-1")
    assert "cluster/1-1" in (out / "design" / "a.com.md").read_text()


def test_rerender_keeps_the_owners_graph_settings(result, doc, tmp_path):
    """The owner tunes forces and zoom by hand; a relabel must replace only colours."""
    out = rc.render_version([result], doc, tmp_path / "cluster-1")
    gfile = out / "design" / ".obsidian" / "graph.json"
    g = json.loads(gfile.read_text())
    g.update({"repelStrength": 14.79, "centerStrength": 0, "scale": 0.307,
              "showTags": True})
    gfile.write_text(json.dumps(g))
    rc.render_version([titled(result)], doc, out)
    g2 = json.loads(gfile.read_text())
    assert (g2["repelStrength"], g2["centerStrength"], g2["scale"], g2["showTags"]) == \
        (14.79, 0, 0.307, True)
    assert g2["colorGroups"][0]["query"] == "tag:#warm-paper-and-serif"


def test_result_rebuilds_from_the_rendered_notes(result, doc, tmp_path):
    """Relabelling reads the vault, so the clustering cannot silently change."""
    out = rc.render_version([result], doc, tmp_path / "cluster-1")
    back = rc.result_from_vault(out / "design")
    assert {d: i["path"] for d, i in back["sites"].items()} == \
        {d: i["path"] for d, i in result["sites"].items()}
    assert back["sites"]["a.com"]["neighbors"] == [{"domain": "b.com", "score": 0.91}]
    assert (back["levels"], back["k"], back["model"]) == ([2, 4], 2, "m")
    assert back["cluster_names"]["1"] == "warm paper"


def test_relabel_round_trip_changes_names_not_membership(result, doc, tmp_path):
    out = rc.render_version([result], doc, tmp_path / "cluster-1")
    back = rc.result_from_vault(out / "design")
    back["cluster_titles"] = dict(TITLES)
    rc.render_version([back], doc, out)
    again = rc.result_from_vault(out / "design")
    assert {d: i["path"] for d, i in again["sites"].items()} == \
        {d: i["path"] for d, i in result["sites"].items()}
    assert again["cluster_names"]["1"] == "Warm paper and serif"


def test_title_prompt_lists_members_once_and_parents_by_children(result, doc):
    p = ct.build_prompt(result, doc, "design")
    assert "[1] parent of 1.1" in p and "[1.1] (2 sites)" in p
    assert p.count("a.com:") == 1, "each site described once"


def test_title_clusters_fills_gaps_from_keyword_names(result, doc):
    fake = lambda *a, **k: ('{"1": "Warm paper", "1.1": "Terracotta"}', {})
    t = ct.title_clusters(result, doc, run=fake)
    assert t["1"] == "Warm paper" and t["2"] == "stark mono"


def test_purpose_members_are_described_by_their_essence():
    line = ct.member_line("fabra.com", {"essence": {"kind": "design tool",
                                                    "domain": "fashion and apparel",
                                                    "subject": "Fabra"}}, "purpose")
    assert "design tool | fashion and apparel | Fabra" in line
