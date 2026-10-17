#!/usr/bin/env python3
"""Keep the daemon's checkout in sync with origin/main so queued work arrives.

Why this is not just `git pull`: the daemon commits its own output (inspiration.json,
the vault, screenshots), so the tree is dirty after every run and a plain
`merge --ff-only` would refuse. Hence the ordering this module enforces:

    pull:     commit the daemon's generated output  ->  fetch  ->  ff or merge
    publish:  commit whatever the run produced      ->  push

Push is part of the design, not a nicety: if the daemon committed locally and never
pushed, local main would diverge from origin/main and every later --ff-only would
fail. Pushing keeps the fast-forward path open.

Hand edits are sacred. If anything OUTSIDE the daemon-owned paths is dirty, we commit
nothing and skip the merge — so a work-in-progress edit to run.sh or tools/ is never
swept into a daemon commit, and never clobbered by a merge landing on top of it. The
run then continues on local work only; the next fire picks up the queue once the tree
is clean.

Exit code is always 0: a sync problem must never fail the run or advance the ledger.
Callers read the STATUS line from stdout.
"""
import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tools.ingest.config import REPO

# Paths the daemon owns and may commit unattended. Everything else is the human's.
# inspo/vault/ITERATIONS.md is hand-written but lives here deliberately: it is part of
# the same story as the data it documents, and committing it with a run is harmless.
DAEMON_PREFIXES = ("inspo/", "screenshots/")

REMOTE = "origin"
BRANCH = "main"


def _git(repo, *args, check=False):
    return subprocess.run(["git", *args], cwd=str(repo), capture_output=True,
                          text=True, check=check)


def unquote_path(p):
    """git quotes paths containing specials: "inspo/a b.md" -> inspo/a b.md."""
    if len(p) >= 2 and p.startswith('"') and p.endswith('"'):
        return p[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    return p


def parse_porcelain(text):
    """Paths out of `git status --porcelain` v1. Pure; testable.

    Handles ' M path', '?? path', 'R  old -> new' (we want the new name) and
    quoted paths. Lines too short to carry a path are ignored.
    """
    paths = []
    for line in text.splitlines():
        if len(line) < 4:
            continue
        rest = line[3:]
        if " -> " in rest:
            rest = rest.split(" -> ", 1)[1]
        rest = unquote_path(rest.strip())
        if rest:
            paths.append(rest)
    return paths


def split_ownership(paths):
    """(daemon_owned, foreign) by path prefix. Pure; testable."""
    daemon, foreign = [], []
    for p in paths:
        (daemon if p.startswith(DAEMON_PREFIXES) else foreign).append(p)
    return daemon, foreign


def dirty_paths(repo):
    return parse_porcelain(_git(repo, "status", "--porcelain").stdout)


def commit_generated(repo, message):
    """Commit daemon-owned dirty paths only.

    Returns one of: COMMITTED <n>, CLEAN, FOREIGN <n>. Never commits when a foreign
    path is dirty — that is the guard that keeps hand edits out of daemon commits.
    """
    daemon, foreign = split_ownership(dirty_paths(repo))
    if foreign:
        return f"FOREIGN {len(foreign)}"
    if not daemon:
        return "CLEAN"
    # Stage the detected paths, not the prefixes: `git add -- inspo/ screenshots/`
    # fails as a whole if either directory does not exist, silently staging nothing.
    _git(repo, "add", "--", *daemon)
    # Re-check: an ignored-only change can still leave nothing staged.
    if not _git(repo, "diff", "--cached", "--name-only").stdout.strip():
        return "CLEAN"
    r = _git(repo, "commit", "-m", message)
    if r.returncode != 0:
        return "CLEAN"
    return f"COMMITTED {len(daemon)}"


def fetch_and_integrate(repo):
    """Fetch origin/main and get its commits into the working tree.

    --ff-only alone is not enough: once this run has committed its own generated
    output, local main is no longer an ancestor of origin/main, so a fast-forward is
    impossible by construction whenever the remote also moved. The four cases are
    therefore handled explicitly:

      FF_UP_TO_DATE  same commit, nothing to do
      LOCAL_AHEAD    remote is an ancestor of local — publish will push it
      FF_OK          local is an ancestor of remote — clean fast-forward
      MERGE_OK       genuinely diverged — a real merge commit, which is safe here
                     because the remote only ever adds inspo/_queue/ files while the
                     daemon only ever writes generated output: disjoint paths
      MERGE_CONFLICT the paths did overlap after all — aborted, left to a human

    Returns one of those, or FETCH_FAILED.
    """
    if _git(repo, "fetch", REMOTE, BRANCH).returncode != 0:
        return "FETCH_FAILED"
    local = _git(repo, "rev-parse", "HEAD").stdout.strip()
    remote = _git(repo, "rev-parse", f"{REMOTE}/{BRANCH}").stdout.strip()
    if not local or not remote:
        return "FETCH_FAILED"
    if local == remote:
        return "FF_UP_TO_DATE"
    if _git(repo, "merge-base", "--is-ancestor", remote, local).returncode == 0:
        return "LOCAL_AHEAD"
    if _git(repo, "merge-base", "--is-ancestor", local, remote).returncode == 0:
        if _git(repo, "merge", "--ff-only", f"{REMOTE}/{BRANCH}").returncode == 0:
            return "FF_OK"
        return "MERGE_CONFLICT"
    if _git(repo, "merge", "--no-edit", "-m",
            f"Merge {REMOTE}/{BRANCH} into daemon run", f"{REMOTE}/{BRANCH}").returncode == 0:
        return "MERGE_OK"
    _git(repo, "merge", "--abort")
    return "MERGE_CONFLICT"


def push(repo):
    if _git(repo, "push", REMOTE, BRANCH).returncode != 0:
        return "PUSH_FAILED"
    return "PUSH_OK"


def do_pull(repo):
    c = commit_generated(repo, "Data: daemon output before sync")
    if c.startswith("FOREIGN"):
        return f"SYNC_SKIPPED_FOREIGN {c.split()[1]}"
    return f"SYNC {c} {fetch_and_integrate(repo)}"


def do_publish(repo, message):
    c = commit_generated(repo, message)
    if c.startswith("FOREIGN"):
        return f"PUBLISH_SKIPPED_FOREIGN {c.split()[1]}"
    if c == "CLEAN":
        return "PUBLISH_NOTHING"
    return f"PUBLISH {c} {push(repo)}"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("mode", choices=("pull", "publish"))
    ap.add_argument("--message", default="Data: daemon run (vault rebuild)")
    ap.add_argument("--repo", default=str(REPO))
    args = ap.parse_args()
    repo = Path(args.repo)
    print(do_pull(repo) if args.mode == "pull" else do_publish(repo, args.message))
    return 0   # never fail the run over sync


if __name__ == "__main__":
    raise SystemExit(main())
