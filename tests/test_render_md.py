from tools.ingest.render_md import render_item_block, splice_region
from tools.ingest.config import MD_REGION_START, MD_REGION_END

ITEM = {"title": "Ditther", "primary_url": "http://ditther.com", "author": "blurrhaus",
        "author_profile": "https://twitter.com/blurrhaus", "tweet": "https://twitter.com/blurrhaus/status/1",
        "date": "2026-06-02", "tags": ["tools-build", "design"], "text": "See it"}


def test_render_item_block_has_title_and_link():
    md = render_item_block(ITEM)
    assert "Ditther" in md and "http://ditther.com" in md
    assert "`tools-build`" in md


def test_splice_creates_region_when_absent():
    out = splice_region("# Doc\n\nbody\n", "GENERATED")
    assert MD_REGION_START in out and MD_REGION_END in out
    assert "GENERATED" in out
    assert out.startswith("# Doc")


def test_splice_replaces_existing_region_only():
    base = f"# Doc\n\n{MD_REGION_START}\nOLD\n{MD_REGION_END}\n\nfooter\n"
    out = splice_region(base, "NEW")
    assert "OLD" not in out and "NEW" in out
    assert "footer" in out
