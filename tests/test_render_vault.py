from tools.ingest.render_vault import build_vault, slug


def _site(patterns, palette, font, tech="Next.js"):
    return {
        "url": "https://x", "title": "T", "tagline": "tag", "screenshot": "screenshots/xcom.png",
        "what_it_is": "w", "what_it_shows": "w", "how_it_works": "w", "how_its_designed": "w",
        "palette": palette, "fonts": font,
        "pattern_keywords": patterns, "tech_stack": [tech], "fonts_loaded": [f"{font} 400"],
    }


DOC = {
    "items": [
        {"primary_domain": "a.com", "category": "personal"},
        {"primary_domain": "b.com", "category": "design"},
    ],
    "site_designs": {
        "_schema": {"note": "ignored"},
        "a.com": _site(["dark-mode", "minimalist", "portfolio", "single-screen"],
                       "near-black dark ground", "Geist"),
        "b.com": _site(["dark-mode", "minimalist", "editorial"], "cream warm ground", "Inter"),
        "c.com": _site(["dark-mode", "minimalist", "single-screen"], "near-black dark", "Geist"),
    },
}


def test_build_vault_counts_and_index(tmp_path):
    counts = build_vault(DOC, tmp_path)
    assert counts["sites"] == 3
    idx = (tmp_path / "INDEX.md").read_text()
    assert "By pattern" in idx and "dark-mode" in idx


def test_site_note_edges(tmp_path):
    build_vault(DOC, tmp_path)
    a = (tmp_path / "sites" / "a.com.md").read_text()
    # shared pattern (3 sites) is a hub link; rare pattern (1 site) is an inline tag
    assert "[[patterns/dark-mode|dark-mode]]" in a
    assert "`portfolio`" in a and "[[patterns/portfolio" not in a
    # derived aesthetic + color hubs
    assert "[[aesthetics/dark|dark]]" in a
    assert "[[colors/dark|dark]]" in a
    # related-sites edges + screenshot embed with the vault-relative path
    assert "## Related sites" in a and "[[sites/c.com|c.com]]" in a
    assert "![a.com](../../../screenshots/xcom.png)" in a


def test_hub_round_trip_and_thresholds(tmp_path):
    build_vault(DOC, tmp_path)
    # a pattern shared by >=3 sites gets a hub that links back to its members
    assert (tmp_path / "patterns" / "dark-mode.md").exists()
    assert "[[sites/a.com|a.com]]" in (tmp_path / "patterns" / "dark-mode.md").read_text()
    # single-screen (2 sites) is below the pattern threshold (3) -> no hub file
    assert not (tmp_path / "patterns" / "single-screen.md").exists()
    # font shared by 2 sites (Geist) is a hub; the singleton (Inter) is not
    assert (tmp_path / "fonts" / slug("Geist")).with_suffix(".md").exists()
    assert not (tmp_path / "fonts" / slug("Inter")).with_suffix(".md").exists()
