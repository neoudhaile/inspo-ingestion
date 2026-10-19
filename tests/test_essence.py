"""Essence: validation, JSON repair, problem-site selection, and how results land.

No network and no model calls — run_claude is the only boundary, and it is replaced
where a test needs it.
"""
import json
from pathlib import Path

import pytest

from tools.ingest import essence as es


def good(**over):
    e = {"subject": "Fabra", "host": None, "does": "Design garments in 3D.",
         "for_whom": "fashion designers", "domain": "fashion and apparel",
         "kind": "design tool"}
    e.update(over)
    return e


# --- validation -----------------------------------------------------------------

def test_valid_essence_has_no_errors():
    assert es.validate_essence(good()) == []


@pytest.mark.parametrize("kind", ["landing page", "Marketing site", "Website.",
                                  "home page", "product landing page"])
def test_page_shaped_kinds_are_rejected(kind):
    """comnyang came back as kind 'product landing page' — the page, not the cat."""
    errs = es.validate_essence(good(kind=kind))
    assert any("names the page" in e for e in errs)


def test_missing_and_empty_fields_are_reported():
    e = good(); del e["domain"]; e["does"] = "  "
    errs = es.validate_essence(e)
    assert "missing domain" in errs and "does is empty" in errs


def test_host_may_be_null_but_not_a_number():
    assert es.validate_essence(good(host=None)) == []
    assert es.validate_essence(good(host="AppDrop, an app platform")) == []
    assert es.validate_essence(good(host=3))


def test_non_object_essence_is_rejected():
    assert es.validate_essence("fashion") == ["essence is not an object"]


def test_normalize_turns_placeholder_hosts_into_none():
    assert es.normalize_essence(good(host="null"))["host"] is None
    assert es.normalize_essence(good(host="  "))["host"] is None
    assert es.normalize_essence(good(subject="  Fabra "))["subject"] == "Fabra"


@pytest.mark.parametrize("raw,level", [("high — consistent", "high"),
                                       ("Medium: thin notes", "medium"),
                                       ("low", "low"), ("", "unknown"), (None, "unknown")])
def test_confidence_level(raw, level):
    assert es.confidence_level(raw) == level


# --- apply-time check (the daemon path) -----------------------------------------

def test_check_site_design_keeps_a_valid_essence():
    p = {"essence": good(host="")}
    assert es.check_site_design(p) == "ok"
    assert p["essence"]["host"] is None and p["essence_status"] == "ok"


def test_check_site_design_drops_an_invalid_essence_without_raising():
    """A bad essence must never fail an unattended run — drop, mark, backfill later."""
    p = {"essence": good(kind="landing page"), "what_it_is": "kept"}
    status = es.check_site_design(p)
    assert status.startswith("invalid:")
    assert "essence" not in p and p["what_it_is"] == "kept"


def test_check_site_design_marks_a_missing_essence():
    p = {}
    assert es.check_site_design(p) == "missing" and p["essence_status"] == "missing"


# --- JSON repair ----------------------------------------------------------------

def test_loads_loose_repairs_the_stray_quote_seen_in_testing():
    """The exact slip that broke comnyang's run: `"desktop pet app","},`."""
    raw = '{"essence":{"kind":"desktop pet app","},"prose":{"what_it_is":"A cat."}}'
    d = es.loads_loose(raw)
    assert d["essence"]["kind"] == "desktop pet app"
    assert d["prose"]["what_it_is"] == "A cat."


def test_loads_loose_strips_fences_and_surrounding_prose():
    raw = 'Here you go:\n```json\n{"a": 1, "b": [1, 2,],}\n```\nDone.'
    assert es.loads_loose(raw) == {"a": 1, "b": [1, 2]}


def test_loads_loose_raises_when_there_is_no_object():
    with pytest.raises(ValueError):
        es.loads_loose("I could not open the site.")


# --- which sites get a live re-scrape -------------------------------------------

def test_problem_sites_finds_deep_urls_and_page_first_prose():
    doc = {"site_designs": {
        "_schema": {},
        "appdrop.com": {"url": "https://www.appdrop.com/marcgmbh/link-bouquet",
                        "what_it_is": "A mini-app."},
        "deel.com": {"url": "https://www.deel.com/",
                     "what_it_is": "The marketing homepage for Deel..."},
        "comnyang.com": {"url": "https://comnyang.com/",
                         "what_it_is": "The product landing page for Comnyang."},
        "fabra.com": {"url": "https://www.fabra.com/",
                      "what_it_is": "A browser-based 3D apparel design platform."},
    }}
    got = es.problem_sites(doc)
    assert got["appdrop.com"] == "deep-url"
    assert got["comnyang.com"] == "page-first"
    assert "fabra.com" not in got


@pytest.mark.parametrize("url,deep", [("https://a.com/", False), ("https://a.com", False),
                                      ("https://a.com/x", True), ("", False)])
def test_is_deep_url(url, deep):
    assert es.is_deep_url(url) is deep


# --- how results land in the source ---------------------------------------------

@pytest.fixture
def doc():
    return {"site_designs": {
        "appdrop.com": {"what_it_is": "old is", "what_it_shows": "old shows",
                        "how_it_works": "old works", "how_its_designed": "DOM design",
                        "palette_tokens": [{"value": "#fff"}]},
    }}


def live_result():
    return {"essence": good(subject="Link Bouquet", host="AppDrop"),
            "prose": {"what_it_is": "new is", "what_it_shows": "new shows",
                      "how_it_works": "new works"},
            "evidence": ["Title: Link Bouquet"], "confidence": "high — clear",
            "site_state": "live"}


def test_live_results_replace_purpose_prose_but_never_design(doc):
    es.apply_results(doc, {"appdrop.com": live_result()}, "live", "m", when="t")
    e = doc["site_designs"]["appdrop.com"]
    assert e["what_it_is"] == "new is" and e["how_it_works"] == "new works"
    assert e["how_its_designed"] == "DOM design", "design prose is DOM-grounded"
    assert e["palette_tokens"] == [{"value": "#fff"}], "the sidecar is never touched"
    assert e["essence"]["host"] == "AppDrop"
    assert e["essence_meta"]["source"] == "live"
    assert e["essence_meta"]["confidence"] == "high"


def test_prose_backfill_adds_essence_and_leaves_all_prose_alone(doc):
    es.apply_results(doc, {"appdrop.com": {"essence": good(), "confidence": "low — thin"}},
                     "prose", "m", when="t")
    e = doc["site_designs"]["appdrop.com"]
    assert e["what_it_is"] == "old is"
    assert e["essence_meta"] == {"source": "prose", "model": "m", "at": "t",
                                 "confidence": "low", "confidence_note": "low — thin"}


def test_apply_ignores_unknown_domains(doc):
    assert es.apply_results(doc, {"nope.com": live_result()}, "live", "m") == 0


# --- isolation ------------------------------------------------------------------

def test_each_claude_run_gets_its_own_empty_directory(monkeypatch):
    """A session can read its working dir; one test run read the other sites' list."""
    seen = []

    class R:
        returncode = 0
        stderr = ""
        stdout = json.dumps({"result": "{}", "is_error": False})

    def fake_run(cmd, cwd, **kw):
        seen.append((cwd, sorted(Path(cwd).iterdir()), cmd))
        return R()

    monkeypatch.setattr(es.subprocess, "run", fake_run)
    es.run_claude("p", browser=True)
    es.run_claude("p", browser=False)
    (cwd1, files1, cmd1), (cwd2, files2, cmd2) = seen
    assert cwd1 != cwd2, "runs must not share a directory"
    assert files1 == [] and files2 == [], "and the directory must start empty"
    assert not Path(cwd1).exists(), "and be removed afterwards"
    assert "mcp__playwright" in cmd1 and "mcp__playwright" not in cmd2
    assert "--strict-mcp-config" in cmd1 and "--strict-mcp-config" in cmd2


def test_run_claude_raises_on_a_reported_error(monkeypatch):
    class R:
        returncode = 0
        stderr = ""
        stdout = json.dumps({"result": "rate limited", "is_error": True})
    monkeypatch.setattr(es.subprocess, "run", lambda *a, **k: R())
    with pytest.raises(RuntimeError):
        es.run_claude("p", browser=False)


def test_scrape_live_retries_once_on_invalid_output(monkeypatch):
    answers = iter([
        ('{"essence": {"kind": "landing page"}}', {}),
        (json.dumps({"essence": good(), "prose": {"what_it_is": "a", "what_it_shows": "b",
                                                    "how_it_works": "c"},
                     "evidence": ["x"], "confidence": "high", "site_state": "live"}),
         {"total_cost_usd": 0.1}),
    ])
    monkeypatch.setattr(es, "run_claude", lambda *a, **k: next(answers))
    r = es.scrape_live("fabra.com", "https://www.fabra.com/")
    assert r["attempts"] == 2 and r["essence"]["domain"] == "fashion and apparel"


def test_scrape_live_gives_up_after_two_bad_answers(monkeypatch):
    monkeypatch.setattr(es, "run_claude",
                        lambda *a, **k: ('{"essence": {"kind": "website"}}', {}))
    with pytest.raises(RuntimeError):
        es.scrape_live("x.com", "https://x.com/")


def test_backfill_batch_keeps_the_valid_and_reports_the_rest(monkeypatch):
    payload = {"a.com": {"essence": good(), "confidence": "high"},
               "b.com": {"essence": good(kind="home page"), "confidence": "high"}}
    monkeypatch.setattr(es, "run_claude",
                        lambda *a, **k: (json.dumps(payload), {"total_cost_usd": 0.2}))
    out, bad = es.backfill_batch([("a.com", {}), ("b.com", {})])
    assert set(out) == {"a.com"} and set(bad) == {"b.com"}
    assert out["a.com"]["cost_usd"] == pytest.approx(0.1)


def test_material_scrubs_pipeline_narration():
    m = es.material("x.com", {"url": "https://x.com", "title": "X",
                              "what_it_is": "A falling-sand toy. A WebFetch text-fetch succeeded.",
                              "what_it_shows": "Not captured."})
    assert "falling-sand" in m and "WebFetch" not in m and "Not captured" not in m


# --- sites that changed after they were captured --------------------------------

@pytest.mark.parametrize("state", ["gone", "sunset"])
def test_a_dead_or_sunset_site_keeps_its_original_capture(doc, state):
    """The library records what the owner SAW. A 404 or a sunset notice is not a
    better description of a site than the teardown made while it was alive."""
    r = live_result(); r["site_state"] = state
    n = es.apply_results(doc, {"appdrop.com": r}, "live", "m", when="t")
    e = doc["site_designs"]["appdrop.com"]
    assert n == 0
    assert e["what_it_is"] == "old is", "original prose must survive"
    assert "essence" not in e, "left for the backfill to derive from the capture"
    assert e["site_state"]["state"] == state


def test_a_live_result_clears_a_stale_site_state(doc):
    doc["site_designs"]["appdrop.com"]["site_state"] = {"state": "gone"}
    r = live_result(); r["site_state"] = "live"
    es.apply_results(doc, {"appdrop.com": r}, "live", "m")
    assert "site_state" not in doc["site_designs"]["appdrop.com"]


def test_scrape_live_requires_a_site_state(monkeypatch):
    body = {"essence": good(), "prose": {"what_it_is": "a", "what_it_shows": "b",
                                         "how_it_works": "c"}, "confidence": "high"}
    answers = iter([(json.dumps(body), {}),
                    (json.dumps({**body, "site_state": "sunset"}), {})])
    monkeypatch.setattr(es, "run_claude", lambda *a, **k: next(answers))
    r = es.scrape_live("fey.com", "https://fey.com/")
    assert r["attempts"] == 2 and r["site_state"] == "sunset"


def test_problem_sites_skips_sites_a_live_run_already_settled():
    doc = {"site_designs": {
        "a.com": {"url": "https://a.com/x", "essence_meta": {"source": "live"}},
        "b.com": {"url": "https://b.com/x", "site_state": {"state": "gone"}},
        "c.com": {"url": "https://c.com/x", "essence_meta": {"source": "prose"}},
    }}
    assert set(es.problem_sites(doc)) == {"c.com"}
