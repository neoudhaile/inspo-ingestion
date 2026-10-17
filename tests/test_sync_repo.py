"""Sync logic: the commit-then-ff-merge ordering, and the hand-edit guard.

The merge/divergence cases run against real throwaway git repos — the whole point of
this module is how git behaves on a dirty tree, which a mock would not prove.
"""
import subprocess
import pytest

from tools.ingest import sync_repo as sr


# ---------- pure parts ----------

def test_parse_porcelain_handles_modified_untracked_and_rename():
    text = " M inspo/inspiration.json\n?? screenshots/a.png\nR  inspo/old.md -> inspo/new.md\n"
    assert sr.parse_porcelain(text) == [
        "inspo/inspiration.json", "screenshots/a.png", "inspo/new.md"]


def test_parse_porcelain_unquotes_paths_with_spaces():
    assert sr.parse_porcelain(' M "inspo/vault/a b.md"\n') == ["inspo/vault/a b.md"]


def test_parse_porcelain_ignores_short_lines():
    assert sr.parse_porcelain("\n \nM\n") == []


def test_split_ownership_separates_daemon_paths_from_hand_edits():
    daemon, foreign = sr.split_ownership([
        "inspo/inspiration.json", "screenshots/x.png", "inspo/vault/a.md",
        "run.sh", "tools/ingest/add_urls.py", "tests/test_x.py",
    ])
    assert daemon == ["inspo/inspiration.json", "screenshots/x.png", "inspo/vault/a.md"]
    assert foreign == ["run.sh", "tools/ingest/add_urls.py", "tests/test_x.py"]


def test_split_ownership_does_not_match_lookalike_prefix():
    _, foreign = sr.split_ownership(["inspo-notes/x.md", "screenshots.md"])
    assert foreign == ["inspo-notes/x.md", "screenshots.md"]


# ---------- real git repos ----------

def git(repo, *args):
    return subprocess.run(["git", *args], cwd=str(repo), capture_output=True,
                          text=True, check=True)


@pytest.fixture
def origin(tmp_path):
    """A bare remote with one commit on main, plus a clone wired to it."""
    bare = tmp_path / "origin.git"
    seed = tmp_path / "seed"
    git(tmp_path, "init", "--bare", "-b", "main", str(bare))
    git(tmp_path, "clone", str(bare), str(seed))
    git(seed, "config", "user.email", "t@t.t")
    git(seed, "config", "user.name", "t")
    (seed / "inspo").mkdir()
    (seed / "inspo" / "inspiration.json").write_text("{}\n")
    (seed / "run.sh").write_text("#!/bin/sh\n")
    git(seed, "add", "-A")
    git(seed, "commit", "-m", "seed")
    git(seed, "push", "-u", "origin", "main")
    return bare, seed


@pytest.fixture
def repo(origin, tmp_path):
    bare, _ = origin
    work = tmp_path / "work"
    git(tmp_path, "clone", str(bare), str(work))
    git(work, "config", "user.email", "d@d.d")
    git(work, "config", "user.name", "daemon")
    return work


def head(r):
    return git(r, "rev-parse", "HEAD").stdout.strip()


def test_commit_generated_commits_daemon_output(repo):
    (repo / "inspo" / "inspiration.json").write_text('{"a":1}\n')
    (repo / "screenshots").mkdir()
    (repo / "screenshots" / "a.png").write_text("x")
    before = head(repo)
    assert sr.commit_generated(repo, "msg").startswith("COMMITTED")
    assert head(repo) != before
    assert sr.dirty_paths(repo) == []


def test_commit_generated_is_clean_noop_on_clean_tree(repo):
    before = head(repo)
    assert sr.commit_generated(repo, "msg") == "CLEAN"
    assert head(repo) == before


def test_commit_generated_refuses_when_a_hand_edit_is_dirty(repo):
    (repo / "inspo" / "inspiration.json").write_text('{"a":1}\n')
    (repo / "run.sh").write_text("#!/bin/sh\n# my work in progress\n")
    before = head(repo)
    assert sr.commit_generated(repo, "msg") == "FOREIGN 1"
    assert head(repo) == before, "a hand edit must never be swept into a daemon commit"
    assert "run.sh" in sr.dirty_paths(repo)


def test_pull_brings_a_queued_file_in_over_a_dirty_tree(repo, origin):
    """The whole reason this module exists: dirty tree + new remote commit.

    The daemon's output is committed first, which makes the branches diverge, so this
    lands as a merge rather than a fast-forward. What matters is the queued file
    arriving and the generated output being preserved, not which of the two it was.
    """
    bare, seed = origin
    qdir = seed / "inspo" / "_queue"
    qdir.mkdir(parents=True, exist_ok=True)
    (qdir / "20261017-muse.txt").write_text("https://example.com\n")
    git(seed, "add", "-A")
    git(seed, "commit", "-m", "queue: 1 site")
    git(seed, "push", "origin", "main")

    (repo / "inspo" / "inspiration.json").write_text('{"dirty":true}\n')
    status = sr.do_pull(repo)

    assert "COMMITTED" in status, status
    assert "MERGE_OK" in status or "FF_OK" in status, status
    assert (repo / "inspo" / "_queue" / "20261017-muse.txt").exists(), \
        "the queued file must arrive in the working tree"
    assert (repo / "inspo" / "inspiration.json").read_text() == '{"dirty":true}\n', \
        "the daemon's generated output must survive the integration"
    assert sr.dirty_paths(repo) == []


def test_pull_fast_forwards_a_clean_tree(repo, origin):
    """No local output to commit, remote ahead — the genuine fast-forward path."""
    bare, seed = origin
    (seed / "inspo" / "_queue").mkdir(parents=True, exist_ok=True)
    (seed / "inspo" / "_queue" / "q.txt").write_text("https://example.com\n")
    git(seed, "add", "-A"); git(seed, "commit", "-m", "queue"); git(seed, "push", "origin", "main")

    assert sr.do_pull(repo) == "SYNC CLEAN FF_OK"
    assert (repo / "inspo" / "_queue" / "q.txt").exists()


def test_pull_skips_the_merge_entirely_when_hand_edits_are_dirty(repo, origin):
    bare, seed = origin
    (seed / "newfile.md").write_text("remote\n")
    git(seed, "add", "-A"); git(seed, "commit", "-m", "remote"); git(seed, "push", "origin", "main")

    (repo / "run.sh").write_text("#!/bin/sh\n# wip\n")
    before = head(repo)
    assert sr.do_pull(repo) == "SYNC_SKIPPED_FOREIGN 1"
    assert head(repo) == before
    assert not (repo / "newfile.md").exists()


def test_pull_merges_when_disjoint_paths_diverged(repo, origin):
    """Unpushed daemon commit + new remote commit: merge, since paths don't overlap."""
    bare, seed = origin
    qdir = seed / "inspo" / "_queue"; qdir.mkdir(parents=True, exist_ok=True)
    (qdir / "20261017-muse.txt").write_text("https://example.com\n")
    git(seed, "add", "-A"); git(seed, "commit", "-m", "queue"); git(seed, "push", "origin", "main")

    (repo / "inspo" / "inspiration.json").write_text('{"local":1}\n')
    git(repo, "add", "-A"); git(repo, "commit", "-m", "local daemon commit")

    assert "MERGE_OK" in sr.do_pull(repo)
    assert (repo / "inspo" / "_queue" / "20261017-muse.txt").exists()


def test_pull_aborts_and_reports_a_real_conflict(repo, origin):
    """Both sides edited the same generated file: abort, leave it to a human."""
    bare, seed = origin
    (seed / "inspo" / "inspiration.json").write_text('{"remote":1}\n')
    git(seed, "add", "-A"); git(seed, "commit", "-m", "remote edit"); git(seed, "push", "origin", "main")

    (repo / "inspo" / "inspiration.json").write_text('{"local":1}\n')
    git(repo, "add", "-A"); git(repo, "commit", "-m", "local daemon commit")
    local_head = head(repo)

    assert "MERGE_CONFLICT" in sr.do_pull(repo)
    assert head(repo) == local_head
    assert sr.dirty_paths(repo) == [], "an aborted merge must leave no half-merged tree"


def test_pull_reports_local_ahead_without_touching_history(repo, origin):
    (repo / "inspo" / "inspiration.json").write_text('{"local":1}\n')
    git(repo, "add", "-A"); git(repo, "commit", "-m", "local daemon commit")
    local_head = head(repo)
    assert "LOCAL_AHEAD" in sr.do_pull(repo)
    assert head(repo) == local_head


def test_publish_commits_and_pushes_so_the_next_ff_still_works(repo, origin):
    bare, _ = origin
    (repo / "inspo" / "inspiration.json").write_text('{"new":1}\n')
    assert sr.do_publish(repo, "Data: run") == "PUBLISH COMMITTED 1 PUSH_OK"
    remote_head = subprocess.run(["git", "rev-parse", "main"], cwd=str(bare),
                                 capture_output=True, text=True).stdout.strip()
    assert remote_head == head(repo)


def test_publish_is_a_noop_when_the_run_produced_nothing(repo):
    assert sr.do_publish(repo, "Data: run") == "PUBLISH_NOTHING"


def test_main_never_fails_the_run(repo, capsys):
    """Exit code 0 even on a sync problem — a bad sync must not advance the ledger."""
    (repo / "run.sh").write_text("#!/bin/sh\n# wip\n")
    import sys
    argv = sys.argv
    sys.argv = ["sync_repo", "pull", "--repo", str(repo)]
    try:
        assert sr.main() == 0
    finally:
        sys.argv = argv
    assert "FOREIGN" in capsys.readouterr().out
