#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
VENV=.venv/bin/python
LOCKDIR=/tmp/neoud-ingest.lock.d
CHUNK=5   # enrich at most this many new items per claude -p call

# macOS pop-up (top-right) so the owner can see the daemon working. Never fatal.
notify() { /usr/bin/osascript -e "display notification \"$1\" with title \"Inspiration Daemon\"" >/dev/null 2>&1 || true; }

# Serialize runs (Downloads fires WatchPaths repeatedly). Portable atomic lock
# via mkdir — macOS has no flock by default.
if ! mkdir "$LOCKDIR" 2>/dev/null; then
  echo "another run in progress"; exit 0
fi
trap 'rmdir "$LOCKDIR" 2>/dev/null || true' EXIT

# Sync with origin/main FIRST, so a PR merged on GitHub (an agent queueing sites it
# found in a video, say) is visible to this run. Must hold the lock: it commits.
# Never fatal — a sync problem degrades to "work on local items only".
SYNC="$("$VENV" -m tools.ingest.sync_repo pull 2>&1 | tail -n1)"
echo "sync: $SYNC"
case "$SYNC" in
  *FOREIGN*)    notify "Sync skipped — uncommitted hand edits outside inspo/" ;;
  *MERGE_CONFLICT*) notify "Sync blocked — merge conflict with origin; needs a human" ;;
  *FETCH_FAILED*) notify "Sync failed (offline?) — working on local items only" ;;
esac

# Other-medium adapter: any file of URLs (one per line) dropped in ~/Downloads as
# inspo-urls*.txt gets ingested through the same pipeline. Every medium — browser
# bookmarks, Raindrop/Pocket exports, pasted links — reduces to a URL list.
URLFILES=()
for f in "$HOME"/Downloads/inspo-urls*.txt; do [ -e "$f" ] && URLFILES+=("$f"); done

# Cheap no-op guard: is there anything new at all, from any medium? Runs under the
# lock now (the sync above commits, and the queue is only knowable after fetching).
QLIST="$("$VENV" -m tools.ingest.drain_queue --list 2>/dev/null)"
QUEUED="$(printf '%s\n' "$QLIST" | awk '/^QUEUE/ {print $2}')"      # queued files
QUEUED_URLS="$(printf '%s\n' "$QLIST" | awk '/^QUEUE/ {print $3}')" # urls in them
QUEUED="${QUEUED:-0}"; QUEUED_URLS="${QUEUED_URLS:-0}"

if ! GUARD="$("$VENV" -m tools.ingest.ingest --limit "$CHUNK" 2>&1)"; then
  notify "Ingest failed — check /tmp/neoud-ingest.err"
  echo "ingest failed"; echo "$GUARD"; exit 1
fi
HEAD="$(printf '%s\n' "$GUARD" | head -n1)"
case "$HEAD" in
  NO_EXPORT|NO_NEW_ITEMS)
    if [ "${#URLFILES[@]}" -eq 0 ] && [ "$QUEUED" -eq 0 ]; then
      # The sync above may have committed generated output; push it before leaving,
      # or it sits unpushed and the next sync has to merge instead of fast-forward.
      echo "no-op publish: $("$VENV" -m tools.ingest.sync_repo publish \
            --message "Data: daemon output (no new items)" 2>&1 | tail -n1)"
      echo "nothing to do"; exit 0
    fi
    HEAD="NEW_ITEMS 0 of 0" ;;
esac
TOTAL="$(printf '%s\n' "$HEAD" | awk '/^NEW_ITEMS/ {print $4}')"   # "NEW_ITEMS 5 of 53 ..."
TOTAL="${TOTAL:-?}"

notify "Started — $TOTAL new bookmark(s) to process"
DONE=0

# Enrich in resumable chunks: each pass ingests up to CHUNK new items, enriches,
# and applies (which advances the ledger), so the next pass returns the NEXT chunk
# until none remain. A big catch-up export (dozens of new bookmarks) thus never goes
# through one giant claude -p call; if a chunk fails (rate limit), earlier chunks are
# already applied and the next daemon fire resumes from where it stopped.
while true; do
  if ! OUT="$("$VENV" -m tools.ingest.ingest --limit "$CHUNK" 2>&1)"; then
    notify "Ingest failed mid-run — will resume next fire"
    echo "ingest failed: $OUT"; exit 1
  fi
  LINE="$(printf '%s\n' "$OUT" | head -n1)"
  case "$LINE" in
    NO_EXPORT|NO_NEW_ITEMS) break ;;
  esac
  N="$(printf '%s\n' "$LINE" | awk '/^NEW_ITEMS/ {print $2}')"
  REM="$(printf '%s\n' "$LINE" | awk '/^NEW_ITEMS/ {print $4}')"
  echo "chunk: $LINE"
  notify "Parsing ${N:-?} website(s)… $((DONE)) done, ${REM:-?} remaining"
  if ! bash tools/ingest/enrich.sh; then
    notify "Enrichment failed (rate limit?) — $DONE done, will resume next fire"
    echo "enrich failed"; exit 1
  fi
  "$VENV" -m tools.ingest.apply_enriched
  DONE=$((DONE + ${N:-0}))
done

# URL drop-files (the universal non-X medium): ingest each, then archive the file.
for f in "${URLFILES[@]:-}"; do
  [ -e "$f" ] || continue
  N_URLS="$(grep -cvE '^\s*(#|$)' "$f" || true)"
  notify "Ingesting $N_URLS URL(s) from $(basename "$f")"
  if NEOUD_HAVE_LOCK=1 "$VENV" -m tools.ingest.add_urls --file "$f" --no-render \
       --label "$(basename "$f")"; then
    mkdir -p inspo/_archive && mv "$f" "inspo/_archive/$(date +%Y%m%d-%H%M%S)-$(basename "$f")"
    DONE=$((DONE + N_URLS))
  else
    notify "URL ingest failed — file kept, will retry next fire"
  fi
done

# In-repo queue (the PR medium): files a remote agent added under inspo/_queue/.
# Drained through the same add_urls adapter; each file is git-rm'd only once it lands.
if [ "$QUEUED" -gt 0 ]; then
  notify "Ingesting $QUEUED_URLS queued URL(s) from inspo/_queue ($QUEUED file(s))"
  if QOUT="$("$VENV" -m tools.ingest.drain_queue 2>&1)"; then
    echo "$QOUT"
    QN="$(printf '%s\n' "$QOUT" | awk '/^QUEUE_DONE/ {print $4}')"
    DONE=$((DONE + ${QN:-0}))
  else
    echo "$QOUT"
    notify "Some queued files failed — kept for the next fire"
  fi
fi

# Rebuild the Obsidian graph vault from the updated JSON (once per run, deterministic).
"$VENV" -m tools.ingest.render_vault >/dev/null || echo "vault rebuild failed (non-fatal)"

# Archive the processed export.
EXPORT="$($VENV - <<'PY'
from tools.ingest.ingest import newest_export
print(newest_export() or "")
PY
)"
if [ -n "$EXPORT" ]; then
  mkdir -p inspo/_archive && cp "$EXPORT" "inspo/_archive/$(basename "$EXPORT")"
fi
# Publish the run's output. Pushing is what keeps the fast-forward path open for the
# next sync — an unpushed daemon commit plus a new PR on origin = diverged main.
PUB="$("$VENV" -m tools.ingest.sync_repo publish \
        --message "Data: daemon run — $DONE item(s) ingested + vault rebuild" 2>&1 | tail -n1)"
echo "publish: $PUB"
case "$PUB" in
  *PUSH_FAILED*) notify "Committed locally but push failed — next sync may be blocked" ;;
  *FOREIGN*)     notify "Nothing published — uncommitted hand edits outside inspo/" ;;
  *ADD_FAILED*)  notify "Publish aborted — could not stage the run (git index busy)" ;;
esac

notify "Done ✓ $DONE bookmark(s) processed — vault updated"
echo "ingest run complete"
