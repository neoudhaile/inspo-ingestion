"""The prefilter's classification rules.

All offline: classify() and looks_like_stub() take an already-fetched result, so the
real signals from PR #1's parked domain are pinned here as data rather than re-fetched.
"""
from tools.ingest import urlcheck as uc


# The exact body terminalindustries.com served — 200 OK, 114 bytes, a JS bounce to
# GoDaddy's lander. This is the case the whole module exists for.
PARKED_BODY = ('<!DOCTYPE html><html><head><script>window.onload=function(){'
               'window.location.href="/lander"}</script></head></html>')

REAL_BODY = ('<!DOCTYPE html><html><head><title>Homepage | GSAP</title>'
             '<link rel="stylesheet" href="/a.css"></head><body>' + "x" * 5000 + '</body></html>')


def test_rejects_the_real_parked_domain_despite_http_200():
    ok, reason = uc.classify(200, "https://terminalindustries.com/", PARKED_BODY)
    assert ok is False
    assert "lander" in reason


def test_allows_a_real_site():
    assert uc.classify(200, "https://gsap.com/", REAL_BODY) == (True, "ok")


def test_rejects_unreachable():
    ok, reason = uc.classify(None, "https://nope.invalid/", None, err="URLError")
    assert ok is False and "unreachable" in reason


def test_rejects_gone_and_server_errors():
    assert uc.classify(404, "https://x.com/", "")[0] is False
    assert uc.classify(410, "https://x.com/", "")[0] is False
    assert uc.classify(503, "https://x.com/", "")[0] is False


def test_allows_bot_blocking_statuses():
    """A 403 is not a dead site — plenty of good ones block a bare urllib request.

    Rejecting these would drop real design sites, which is the expensive mistake.
    """
    for status in (401, 403, 406, 429):
        ok, reason = uc.classify(status, "https://cloudflared.example/", "")
        assert ok is True, status
        assert str(status) in reason


def test_rejects_known_parking_hosts():
    ok, reason = uc.classify(200, "https://www.hugedomains.com/x", REAL_BODY)
    assert ok is False and "parked" in reason


def test_parking_host_match_is_not_a_substring_match():
    """`notafternic.com` is not afternic.com."""
    assert uc.classify(200, "https://notafternic.com/", REAL_BODY)[0] is True


def test_stub_detection_requires_small_and_titleless_and_unstyled():
    assert uc.looks_like_stub("<html><head></head><body></body></html>") is True
    assert uc.looks_like_stub("<html><head><title>Tiny</title></head></html>") is False
    assert uc.looks_like_stub('<html><head><link rel="stylesheet" href="a.css"></head></html>') is False
    assert uc.looks_like_stub("<html>" + "x" * 3000 + "</html>") is False


def test_an_empty_title_does_not_count_as_a_title():
    assert uc.looks_like_stub("<html><head><title>  </title></head></html>") is True


def test_a_real_site_saying_for_sale_is_not_parked():
    """The marker scan only applies to small bodies, so prose is safe."""
    body = REAL_BODY.replace("<body>", "<body><h1>This domain is for sale</h1>")
    assert uc.classify(200, "https://realshop.example/", body)[0] is True


def test_skip_env_bypasses_everything(monkeypatch):
    monkeypatch.setenv("NEOUD_SKIP_URLCHECK", "1")
    v = uc.check_many(["https://whatever.invalid/"])
    assert len(v) == 1 and v[0].ok and "skipped" in v[0].reason


def test_check_many_preserves_order(monkeypatch):
    monkeypatch.setattr(uc, "check", lambda u, timeout=None: uc.Verdict(u, True, "ok"))
    urls = [f"https://s{i}.example/" for i in range(12)]
    assert [v.url for v in uc.check_many(urls)] == urls


def test_check_many_is_empty_for_no_urls():
    assert uc.check_many([]) == []
