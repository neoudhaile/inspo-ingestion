"""Draining inspo/_queue/: ordering, counting, and the resume-on-failure contract.

The runner and remover are injected, so these tests prove the drain policy without
invoking claude -p or touching git.
"""
import pytest

from tools.ingest import drain_queue as dq


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
    ok = {"a.txt": True, "b.txt": False}
    drained, urls, failed = dq.drain(
        repo,
        runner=lambda r, path, label: ok[path.name],
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
        runner=lambda r, path, label: seen.append(path.name) or (path.name != "a.txt"),
        remover=lambda r, path: True,
        log=lambda *_: None,
    )
    assert seen == ["a.txt", "b.txt", "c.txt"], "one bad file must not block the batch"
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
