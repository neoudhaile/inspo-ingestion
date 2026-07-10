from tools.ingest.render_vault import build_vault, edge_score


def _site(facets, palette="dark ground", font="Geist"):
    return {
        "url": "https://x", "title": "T", "tagline": "tag", "screenshot": "screenshots/xcom.png",
        "what_it_is": "w", "what_it_shows": "w", "how_it_works": "w", "how_its_designed": "w",
        "palette": palette, "fonts": font,
        "pattern_keywords": ["kw-one", "kw-two"], "tech_stack": ["Next.js"],
        "fonts_loaded": [f"{font} 400"], "media_mix": {"img": 3},
        "extracted_at": "2026-06-05", "facets": facets,
    }


DOC = {
    "items": [],
    "site_designs": {
        "_schema": {"note": "ignored"},
        # two dark minimal portfolios -> strongly related (vertical+vibe+mode = 6)
        "a.com": _site({"vertical": "portfolio", "mode": "dark",
                        "vibe": ["minimal"], "topics": ["design"]}),
        "b.com": _site({"vertical": "portfolio", "mode": "dark",
                        "vibe": ["minimal"], "topics": []}),
        # a personal blog ABOUT startups: bridges via topic, not vertical
        "c.com": _site({"vertical": "personal-blog", "mode": "light",
                        "vibe": ["editorial"], "topics": ["startups"]}),
        # a startup site sharing the startups topic with c.com
        "d.com": _site({"vertical": "startup-product", "mode": "light",
                        "vibe": ["corporate-clean"], "topics": ["startups"]}),
    },
}


def test_facet_tags_only_no_keyword_tags(tmp_path):
    counts = build_vault(DOC, tmp_path)
    assert counts["sites"] == 4
    a = (tmp_path / "a.com.md").read_text()
    # facet tags present (frontmatter + inline)
    assert "  - vertical/portfolio" in a and "#vibe/minimal" in a and "#mode/dark" in a
    # granular keywords are searchable TEXT, never tags
    assert "**Keywords:** kw-one, kw-two" in a
    assert "#pattern/" not in a and "#tech/" not in a and "#font/" not in a


def test_related_edges_are_weighted_and_explained(tmp_path):
    build_vault(DOC, tmp_path)
    a = (tmp_path / "a.com.md").read_text()
    # a<->b share vertical(3)+vibe(2)+mode(1)=6 >= threshold, with the WHY printed
    assert "[[b.com]] — shared: portfolio, minimal, dark" in a
    # a<->c share nothing above threshold
    assert "[[c.com]]" not in a


def test_topic_bridges_clusters(tmp_path):
    # c (personal blog about startups) and d (startup site) connect ONLY via topic+mode
    s, shared = edge_score(
        {"vertical": "personal-blog", "mode": "light", "vibe": ["editorial"], "topics": ["startups"]},
        {"vertical": "startup-product", "mode": "light", "vibe": ["corporate-clean"], "topics": ["startups"]},
    )
    assert s == 3 and "startups" in shared  # topic(2)+mode(1): visible in graph via shared tag
    build_vault(DOC, tmp_path)
    c = (tmp_path / "c.com.md").read_text()
    assert "#topic/startups" in c  # the bridge tag exists even when below direct-edge threshold


def test_index_reports_facet_map(tmp_path):
    build_vault(DOC, tmp_path)
    idx = (tmp_path / "INDEX.md").read_text()
    assert "#vertical/portfolio` (2)" in idx and "#topic/startups` (2)" in idx
    assert "## vibe" in idx and "## mode" in idx
