#!/usr/bin/env python3
"""Drain inspo/_queue/*.txt — the in-repo inbox a remote agent can fill by PR.

The point of this medium: an agent with no access to this Mac (Muse watching videos,
say) can still feed the pipeline by opening a PR that adds one file here. The daemon
fetches main, drains the queue through the same add_urls adapter every other medium
uses, and `git rm`s each file it finishes.

Format is deliberately identical to the ~/Downloads/inspo-urls*.txt drop-files that
already work: one URL per line, '#' comments ignored. add_urls.normalize() does the
parsing, so there is no second format to keep in step. Agents put their per-site
observations in comment lines, which is the part a headless screenshot cannot get.

A file is removed only after its ingest succeeds, so a rate-limited or crashed run
leaves the queue intact and the next fire resumes it. Nothing here advances the
ledger; apply_enriched does that.
"""
import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tools.ingest.config import REPO
from tools.ingest.add_urls import normalize
from tools.ingest import urlcheck

QUEUE_DIRNAME = "_queue"


def queue_dir(repo):
    return Path(repo) / "inspo" / QUEUE_DIRNAME


def queue_files(repo):
    """Queued files, oldest name first so a batch ingests in a stable order."""
    d = queue_dir(repo)
    if not d.is_dir():
        return []
    return sorted(p for p in d.glob("*.txt") if p.is_file())


def count_urls(path):
    """How many real URLs a queue file carries (comments/blanks excluded). Pure."""
    text = Path(path).read_text(errors="replace")
    return sum(1 for line in text.splitlines() if normalize(line))


def parse_blocks(text):
    """Split a queue file into (header_lines, [(url, [its comment lines])]).

    A queue file's value is not the URLs — it is the agent's note about what the
    video showed, written as `#` comments under each URL. So filtering has to move
    those notes with their URL rather than leave them dangling under the next one.
    Comments before the first URL are the file header and are always kept. Pure.
    """
    header, blocks = [], []
    for line in text.splitlines():
        url = normalize(line)
        if url:
            blocks.append((url, []))
        elif blocks:
            blocks[-1][1].append(line)
        else:
            header.append(line)
    return header, blocks


def render_blocks(header, blocks):
    out = list(header)
    for url, comments in blocks:
        out.append(url)
        out.extend(comments)
    return "\n".join(out).rstrip("\n") + "\n"


def prefilter(repo, path, log=print, checker=urlcheck.check_many):
    """Drop URLs that are not worth an enrichment chunk, keeping their notes together.

    Returns (kept_file | None, n_kept, rejects). Rejected blocks are written to
    inspo/_archive/ with the reason, so a wrong call is auditable rather than a
    silent disappearance — and so a domain that comes back to life can be re-queued.
    A URL whose final address differs (a redirect) is rewritten to the real one.
    """
    header, blocks = parse_blocks(Path(path).read_text(errors="replace"))
    if not blocks:
        return None, 0, []
    verdicts = {v.url: v for v in checker([u for u, _ in blocks])}
    kept, rejects = [], []
    for url, comments in blocks:
        v = verdicts.get(url)
        if v is None or v.ok:
            final = v.final_url if (v and v.final_url != url) else url
            if final != url:
                log(f"QUEUE_REDIRECT {url} -> {final}")
            kept.append((final, comments))
        else:
            rejects.append((url, comments, v.reason))
            log(f"QUEUE_REJECT {url} — {v.reason}")
    if rejects:
        archive = Path(repo) / "inspo" / "_archive"
        archive.mkdir(parents=True, exist_ok=True)
        stamp = time.strftime("%Y%m%d-%H%M%S")
        dest = archive / f"{stamp}-{Path(path).stem}.rejected.txt"
        dest.write_text(render_blocks(
            [f"# rejected by tools.ingest.urlcheck at {stamp}",
             f"# from {Path(path).name} — re-queue any of these if the site comes back"],
            [(u, [f"# reason: {why}"] + c) for u, c, why in rejects]))
        log(f"QUEUE_REJECTS_ARCHIVED {dest.name} ({len(rejects)})")
    if not kept:
        return None, 0, rejects
    inbox = Path(repo) / "inspo" / "_inbox"
    inbox.mkdir(parents=True, exist_ok=True)
    kept_file = inbox / f"queue-checked-{Path(path).stem}.txt"
    kept_file.write_text(render_blocks(header, kept))
    return kept_file, len(kept), rejects


def default_runner(repo, path, label):
    """Hand one queue file to the shared URL adapter. Replaced in tests."""
    return subprocess.run(
        [".venv/bin/python", "-m", "tools.ingest.add_urls",
         "--file", str(path), "--no-render", "--label", label],
        cwd=str(repo),
        env={**os.environ, "NEOUD_HAVE_LOCK": "1"},
    ).returncode == 0


def git_rm(repo, path):
    """Remove a drained file: `git rm` when tracked, plain unlink when not.

    A file that arrived by PR is tracked, so `git rm` stages its deletion for the
    run's publish commit. A file dropped in by hand is untracked, and `git rm` fails
    on it — which would silently re-ingest it on every fire. Hence the fallback.
    """
    path = Path(path)
    r = subprocess.run(["git", "rm", "-f", "--quiet", "--", str(path)],
                       cwd=str(repo), capture_output=True, text=True)
    if r.returncode == 0:
        return True
    try:
        path.unlink()
    except OSError:
        return False
    return not path.exists()


def drain(repo, runner=default_runner, remover=git_rm, log=print,
          checker=None):
    """Ingest each queued file, removing only the ones that succeed.

    Returns (drained_files, drained_urls, failed_files). Keeps going past a failure
    so one bad file cannot block the rest of the batch. URLs are prefiltered first,
    so a parked or dead domain never costs an enrichment chunk.
    """
    drained, urls, failed = 0, 0, 0
    for path in queue_files(repo):
        n = count_urls(path)
        if n == 0:
            log(f"QUEUE_EMPTY {path.name} — removing")
            remover(repo, path)
            continue
        label = f"queue/{path.name}"
        checked, n_kept, rejects = prefilter(
            repo, path, log=log, checker=checker or urlcheck.check_many)
        if checked is None:
            # Everything in the file failed the check: nothing to enrich, and the
            # file is handled — the rejects are archived with their reasons.
            log(f"QUEUE_ALL_REJECTED {path.name} ({len(rejects)} url(s)) — removing")
            remover(repo, path)
            continue
        log(f"QUEUE_INGEST {path.name} ({n_kept} of {n} url(s) passed the check)")
        if runner(repo, checked, label):
            if not remover(repo, path):
                log(f"QUEUE_RM_FAILED {path.name} — may re-ingest next run")
            drained += 1
            urls += n_kept
        else:
            failed += 1
            log(f"QUEUE_FAILED {path.name} — kept, will retry next fire")
    return drained, urls, failed


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", default=str(REPO))
    ap.add_argument("--list", action="store_true", help="count queued files and exit")
    args = ap.parse_args()
    repo = Path(args.repo)
    if args.list:
        files = queue_files(repo)
        print(f"QUEUE {len(files)} {sum(count_urls(p) for p in files)}")
        return 0
    drained, urls, failed = drain(repo)
    print(f"QUEUE_DONE {drained} file(s) {urls} url(s) {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
