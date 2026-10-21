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


def test_named_tags_are_flat_so_the_panel_shows_the_cluster_name():
    """The group panel truncates at ~20 chars; nested, siblings looked identical."""
    tm = ct.named_tags(TITLES)
    assert tm["1"] == "warm-paper-and-serif"
    assert tm["1.1"] == "terracotta-ink"
    assert tm["2.1"] == "browser-default-blue"


def test_named_tags_are_unique_across_the_whole_space():
    tm = ct.named_tags({"1": "Portfolios", "2": "portfolios!", "1.1": "A", "2.1": "a"})
    assert len(set(tm.values())) == 4


def test_titled_render_uses_named_tags_everywhere(result, doc, tmp_path):
    """The group query is the only label Obsidian shows, so the name must be the tag."""
    out = rc.render_version([titled(result)], doc, tmp_path / "cluster-1")
    note = (out / "design" / "a.com.md").read_text()
    assert "  - warm-paper-and-serif\n" in note
    assert "  - terracotta-ink\n" in note
    assert "cluster/" not in note
    g = json.loads((out / "design" / ".obsidian" / "graph.json").read_text())
    assert [x["query"] for x in g["colorGroups"]] == ['"Terracotta ink"',
                                                       '"Browser-default blue"']
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
    assert g2["colorGroups"][0]["query"] == '"Terracotta ink"'


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


# --- colour coordination ----------------------------------------------------------

import colorsys


def hls(rgb):
    r, g, b = ((rgb >> 16) & 255) / 255, ((rgb >> 8) & 255) / 255, (rgb & 255) / 255
    return colorsys.rgb_to_hls(r, g, b)


def hue_gap(a, b):
    """Distance around the colour wheel: hue 0.96 and 0.04 are 0.08 apart, not 0.92."""
    d = abs(a - b) % 1.0
    return min(d, 1.0 - d)


PATHS = {"1", "1.1", "1.2", "1.3", "2", "2.1", "2.2", "3", "3.1"}


def test_every_named_cluster_gets_a_colour_and_no_family_does():
    pal = ct.family_palette(PATHS)
    assert set(pal) == {"1.1", "1.2", "1.3", "2.1", "2.2", "3.1"}


def test_siblings_share_a_hue_and_differ_in_shade():
    """Colour-coordinated: a family reads as one colour region."""
    pal = ct.family_palette(PATHS)
    h11, l11, _ = hls(pal["1.1"]); h13, l13, _ = hls(pal["1.3"])
    assert hue_gap(h11, h13) < 0.09, "same family, near-same hue"
    assert abs(l11 - l13) > 0.15, "but distinguishable shades"
    assert hue_gap(hls(pal["1.1"])[0], hls(pal["2.1"])[0]) > 0.04, "families differ in hue"
    assert len(set(pal.values())) == len(pal)


def test_mixed_clusters_are_washed_out_but_keep_their_family_hue():
    pal = ct.family_palette(PATHS, {"1.2": "Mixed: a, b"})
    _, _, s_mixed = hls(pal["1.2"]); _, _, s_clean = hls(pal["1.1"])
    assert s_mixed < 0.3 < s_clean
    assert hue_gap(hls(pal["1.2"])[0], hls(pal["1.1"])[0]) < 0.09


def test_single_level_clusterings_colour_the_top_level():
    assert set(ct.family_palette({"1", "2", "3"})) == {"1", "2", "3"}


def test_graph_groups_follow_family_order(result, doc, tmp_path):
    out = rc.render_version([titled(result)], doc, tmp_path / "cluster-1")
    g = json.loads((out / "design" / ".obsidian" / "graph.json").read_text())
    assert len(g["colorGroups"]) == 2
    assert all(x["color"]["rgb"] > 0 for x in g["colorGroups"])


def test_index_does_not_link_sites_so_it_cannot_be_a_hub(result, doc, tmp_path):
    """INDEX linking all 201 sites made it the largest node in the graph."""
    out = rc.render_version([result], doc, tmp_path / "cluster-1")
    idx = (out / "design" / "INDEX.md").read_text()
    assert "[[" not in idx
    assert "a.com" in idx, "still lists the sites, as plain text"


def test_families_never_overlap_in_hue():
    """Siblings fan their hue, but never far enough to look like the next family."""
    paths = {str(i) for i in range(1, 9)} | {f"{i}.{j}" for i in range(1, 9) for j in (1, 2, 3)}
    pal = ct.family_palette(paths)
    def hue(p): return hls(pal[p])[0]
    for i in range(1, 8):
        widest_gap_inside = hue_gap(hue(f"{i}.1"), hue(f"{i}.3"))
        to_next = min(hue_gap(hue(f"{i}.{a}"), hue(f"{i + 1}.{b}"))
                      for a in (1, 2, 3) for b in (1, 2, 3))
        assert to_next > 0.03, f"family {i} touches family {i + 1}"
        assert widest_gap_inside < 0.09


def test_index_is_a_colour_legend_for_the_graph(result, doc, tmp_path):
    """The panel truncates group names; INDEX pairs each colour with its full name."""
    out = rc.render_version([titled(result)], doc, tmp_path / "cluster-1")
    idx = (out / "design" / "INDEX.md").read_text()
    g = json.loads((out / "design" / ".obsidian" / "graph.json").read_text())
    for grp in g["colorGroups"]:
        assert f'color:#{grp["color"]["rgb"]:06x}' in idx
    assert "Terracotta ink" in idx


def test_each_group_phrase_matches_exactly_its_own_cluster(result, doc, tmp_path):
    """Groups match by exact name (tag queries matched nothing against a stale tag
    index), so a name appearing in another cluster's note would mis-colour it."""
    out = rc.render_version([titled(result)], doc, tmp_path / "cluster-1")
    d = out / "design"
    g = json.loads((d / ".obsidian" / "graph.json").read_text())
    notes = {f.stem: f.read_text().lower() for f in d.glob("*.md") if f.stem != "INDEX"}
    want = {"Terracotta ink": {"a.com", "b.com"}, "Browser-default blue": {"c.com"}}
    for grp in g["colorGroups"]:
        name = grp["query"].strip('"')
        assert {k for k, t in notes.items() if name.lower() in t} == want[name]


def test_untitled_groups_still_use_tag_queries(result, doc, tmp_path):
    out = rc.render_version([result], doc, tmp_path / "cluster-1")
    g = json.loads((out / "design" / ".obsidian" / "graph.json").read_text())
    assert all(x["query"].startswith("tag:#cluster/") for x in g["colorGroups"])
