"""Draining inspo/_queue/: ordering, counting, and the resume-on-failure contract.

The runner and remover are injected, so these tests prove the drain policy without
invoking claude -p or touching git.
"""
import pytest

from tools.ingest import drain_queue as dq


@pytest.fixture(autouse=True)
def _no_network(monkeypatch):
    """Keep the suite offline. Tests that exercise the prefilter inject a checker."""
    monkeypatch.setenv("NEOUD_SKIP_URLCHECK", "1")


@pytest.fixture
def repo(tmp_path):
    (tmp_path / "inspo" / "_queue").mkdir(parents=True)
    return tmp_path


def write(repo, name, text):
    p = repo / "inspo" / "_queue" / name
    p.write_text(text)
    return p


def test_queue_files_is_empty_when_the_dir_is_absent(tmp_path):
    assert dq.queue_files(tmp_path) == []


def test_queue_files_sorted_and_only_txt(repo):
    write(repo, "20261017-b.txt", "https://b.com\n")
    write(repo, "20261016-a.txt", "https://a.com\n")
    write(repo, "README.md", "not a queue file\n")
    assert [p.name for p in dq.queue_files(repo)] == ["20261016-a.txt", "20261017-b.txt"]


def test_count_urls_ignores_comments_and_blanks(repo):
    p = write(repo, "q.txt", "\n".join([
        "# source: a video", "", "https://a.com",
        "# ^ the hero does a cursor-tracked displacement",
        "  https://b.com  ", "   ", "#trailing",
    ]))
    assert dq.count_urls(p) == 2


def test_count_urls_counts_bare_domains_since_normalize_adds_scheme(repo):
    p = write(repo, "q.txt", "example.com\n")
    assert dq.count_urls(p) == 1


def test_drain_removes_only_files_that_ingested(repo):
    write(repo, "a.txt", "https://a.com\n")
    write(repo, "b.txt", "https://b.com\n")
    removed = []
    ok = {"queue/a.txt": True, "queue/b.txt": False}
    drained, urls, failed = dq.drain(
        repo,
        runner=lambda r, path, label: ok[label],   # path is now the checked copy
        remover=lambda r, path: removed.append(path.name) or True,
        log=lambda *_: None,
    )
    assert (drained, urls, failed) == (1, 1, 1)
    assert removed == ["a.txt"], "a failed file must stay queued for the next fire"


def test_drain_continues_past_a_failure(repo):
    write(repo, "a.txt", "https://a.com\n")
    write(repo, "b.txt", "https://b.com\n")
    write(repo, "c.txt", "https://c.com\n")
    seen = []
    drained, _, failed = dq.drain(
        repo,
        runner=lambda r, path, label: seen.append(label) or (label != "queue/a.txt"),
        remover=lambda r, path: True,
        log=lambda *_: None,
    )
    assert seen == ["queue/a.txt", "queue/b.txt", "queue/c.txt"], \
        "one bad file must not block the batch"
    assert (drained, failed) == (2, 1)


def test_drain_discards_a_comment_only_file_without_ingesting(repo):
    write(repo, "empty.txt", "# muse found nothing worth keeping\n")
    called = []
    drained, urls, failed = dq.drain(
        repo,
        runner=lambda r, path, label: called.append(path.name) or True,
        remover=lambda r, path: True,
        log=lambda *_: None,
    )
    assert called == [], "no URLs means no enrichment call"
    assert (drained, urls, failed) == (0, 0, 0)


def test_drain_labels_each_file_for_provenance(repo):
    write(repo, "20261017-muse.txt", "https://a.com\n")
    labels = []
    dq.drain(repo,
             runner=lambda r, path, label: labels.append(label) or True,
             remover=lambda r, path: True, log=lambda *_: None)
    assert labels == ["queue/20261017-muse.txt"]


def test_drain_reports_a_file_it_could_not_remove(repo):
    write(repo, "a.txt", "https://a.com\n")
    logs = []
    drained, _, failed = dq.drain(
        repo, runner=lambda r, path, label: True,
        remover=lambda r, path: False, log=logs.append)
    assert (drained, failed) == (1, 0)
    assert any("QUEUE_RM_FAILED" in m for m in logs)


def test_list_mode_prints_file_and_url_counts(repo, capsys):
    write(repo, "a.txt", "https://a.com\nhttps://b.com\n")
    write(repo, "b.txt", "# nothing\n")
    import sys
    argv = sys.argv
    sys.argv = ["drain_queue", "--repo", str(repo), "--list"]
    try:
        assert dq.main() == 0
    finally:
        sys.argv = argv
    assert capsys.readouterr().out.strip() == "QUEUE 2 2"


def test_git_rm_falls_back_to_unlink_for_an_untracked_file(repo):
    """A hand-dropped queue file is untracked; `git rm` fails and it must still go.

    Without the fallback such a file re-ingests on every daemon fire forever.
    """
    p = write(repo, "untracked.txt", "https://a.com\n")
    assert dq.git_rm(repo, p) is True      # repo fixture is not a git repo at all
    assert not p.exists()


def test_git_rm_reports_failure_when_the_file_cannot_go(repo):
    missing = repo / "inspo" / "_queue" / "nope.txt"
    assert dq.git_rm(repo, missing) is False


# ---------- prefilter: block parsing and rejection ----------

QUEUE_TEXT = """# source: instagram saved "tech" collection
# why: design-teardown-worthy sites
https://good.example/
# ^ the hero does a cursor-tracked displacement
#   second line of the same note
https://parked.example/
# ^ the whole video is a breakdown of this one
https://alsogood.example/
"""


def fake_checker(reject=(), redirect=None):
    from tools.ingest import urlcheck as uc

    def check_many(urls):
        out = []
        for u in urls:
            if u in reject:
                out.append(uc.Verdict(u, False, "parked (page is a '/lander' stub)"))
            else:
                out.append(uc.Verdict(u, True, "ok", (redirect or {}).get(u, u)))
        return out
    return check_many


def test_parse_blocks_keeps_each_note_with_its_url(repo):
    header, blocks = dq.parse_blocks(QUEUE_TEXT)
    assert len(header) == 2 and all(h.startswith("#") for h in header)
    assert [u for u, _ in blocks] == [
        "https://good.example/", "https://parked.example/", "https://alsogood.example/"]
    assert blocks[0][1] == ["# ^ the hero does a cursor-tracked displacement",
                            "#   second line of the same note"]
    assert blocks[2][1] == []


def test_prefilter_drops_the_bad_url_and_its_note_not_the_neighbours(repo):
    p = write(repo, "q.txt", QUEUE_TEXT)
    kept, n, rejects = dq.prefilter(repo, p, log=lambda *_: None,
                                    checker=fake_checker(reject={"https://parked.example/"}))
    text = kept.read_text()
    assert n == 2
    assert "https://good.example/" in text and "https://alsogood.example/" in text
    assert "https://parked.example/" not in text
    assert "the hero does a cursor-tracked displacement" in text, \
        "a surviving URL must keep its own note"
    assert "the whole video is a breakdown of this one" not in text, \
        "a rejected URL's note must not dangle onto the next URL"


def test_prefilter_archives_rejects_with_reasons(repo):
    p = write(repo, "q.txt", QUEUE_TEXT)
    dq.prefilter(repo, p, log=lambda *_: None,
                 checker=fake_checker(reject={"https://parked.example/"}))
    archived = list((repo / "inspo" / "_archive").glob("*.rejected.txt"))
    assert len(archived) == 1
    body = archived[0].read_text()
    assert "https://parked.example/" in body
    assert "reason: parked" in body
    assert "the whole video is a breakdown of this one" in body, \
        "the agent's note is the evidence; it must survive the rejection"


def test_prefilter_rewrites_a_redirected_url_to_its_real_address(repo):
    p = write(repo, "q.txt", "https://palmier.io/\n# ^ note\n")
    kept, n, _ = dq.prefilter(repo, p, log=lambda *_: None,
                              checker=fake_checker(redirect={"https://palmier.io/": "https://www.palmier.io/"}))
    assert "https://www.palmier.io/" in kept.read_text()
    assert n == 1


def test_prefilter_returns_none_when_everything_is_rejected(repo):
    p = write(repo, "q.txt", "https://parked.example/\n")
    kept, n, rejects = dq.prefilter(repo, p, log=lambda *_: None,
                                    checker=fake_checker(reject={"https://parked.example/"}))
    assert kept is None and n == 0 and len(rejects) == 1


def test_drain_never_calls_the_runner_when_all_urls_fail(repo, monkeypatch):
    """The whole point: a parked domain must not cost an enrichment chunk."""
    write(repo, "q.txt", "https://parked.example/\n")
    monkeypatch.setattr(dq.urlcheck, "check_many", fake_checker(reject={"https://parked.example/"}))
    called, removed = [], []
    drained, urls, failed = dq.drain(
        repo, runner=lambda r, p, l: called.append(p) or True,
        remover=lambda r, p: removed.append(p) or True, log=lambda *_: None)
    assert called == [], "claude -p must never be invoked for a rejected batch"
    assert len(removed) == 1, "the file is handled, so it must not be retried forever"
    assert (drained, urls, failed) == (0, 0, 0)


def test_drain_passes_the_checked_file_not_the_original(repo, monkeypatch):
    write(repo, "q.txt", QUEUE_TEXT)
    monkeypatch.setattr(dq.urlcheck, "check_many", fake_checker(reject={"https://parked.example/"}))
    seen = []
    drained, urls, failed = dq.drain(
        repo, runner=lambda r, p, l: seen.append(p) or True,
        remover=lambda r, p: True, log=lambda *_: None)
    assert len(seen) == 1
    assert "https://parked.example/" not in seen[0].read_text()
    assert urls == 2, "only the URLs that passed should be counted as ingested"
