from tools.ingest.render_vault import build_vault


def _site(patterns, palette, font, tech="Next.js"):
    return {
        "url": "https://x", "title": "T", "tagline": "tag", "screenshot": "screenshots/xcom.png",
        "what_it_is": "w", "what_it_shows": "w", "how_it_works": "w", "how_its_designed": "w",
        "palette": palette, "fonts": font,
        "pattern_keywords": patterns, "tech_stack": [tech], "fonts_loaded": [f"{font} 400"],
        "media_mix": {"img": 3, "video": 0}, "extracted_at": "2026-06-05",
    }


DOC = {
    "items": [
        {"primary_domain": "a.com", "category": "personal"},
        {"primary_domain": "b.com", "category": "design"},
    ],
    "site_designs": {
        "_schema": {"note": "ignored"},
        "a.com": _site(["dark-mode", "minimalist", "portfolio"], "near-black dark ground", "Geist"),
        "b.com": _site(["dark-mode", "minimalist", "editorial"], "cream warm ground", "Inter"),
        "c.com": _site(["dark-mode", "minimalist", "single-screen"], "near-black dark", "Geist"),
    },
}


def test_flat_layout_no_hub_dirs(tmp_path):
    counts = build_vault(DOC, tmp_path)
    assert counts["sites"] == 3
    # one note per website, flat in the vault root, plus INDEX; NO hub subdirectories
    assert (tmp_path / "a.com.md").exists() and (tmp_path / "INDEX.md").exists()
    assert [p.name for p in tmp_path.iterdir() if p.is_dir()] == []


def test_site_note_has_all_data_tags_and_related(tmp_path):
    build_vault(DOC, tmp_path)
    a = (tmp_path / "a.com.md").read_text()
    # nested categorizing tags in frontmatter AND inline (the connective tissue)
    assert "  - aesthetic/dark" in a and "  - pattern/portfolio" in a and "  - category/personal" in a
    assert "#aesthetic/dark" in a and "#tech/next-js" in a
    # full extracted data present (not just prose)
    assert "## Design data" in a and "**Media mix:**" in a and "**Tech stack:**" in a
    # screenshot embed (flat vault -> ../../screenshots) + related-site links
    assert "![a.com](../../screenshots/xcom.png)" in a
    assert "## Related sites" in a and "[[c.com]]" in a


def test_index_is_a_tag_map(tmp_path):
    build_vault(DOC, tmp_path)
    idx = (tmp_path / "INDEX.md").read_text()
    # tags shared by >=3 sites listed as connective tags; each note is a website
    assert "#aesthetic/dark" in idx and "(3)" in idx
    assert "## pattern" in idx
