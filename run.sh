#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
VENV=.venv/bin/python
LOCKDIR=/tmp/neoud-ingest.lock.d
CHUNK=5   # enrich at most this many new items per claude -p call

# macOS pop-up (top-right) so the owner can see the daemon working. Never fatal.
notify() { /usr/bin/osascript -e "display notification \"$1\" with title \"Inspiration Daemon\"" >/dev/null 2>&1 || true; }

# Cheap no-op guard (before locking): is there anything new at all?
if ! GUARD="$("$VENV" -m tools.ingest.ingest --limit "$CHUNK" 2>&1)"; then
  notify "Ingest failed — check /tmp/neoud-ingest.err"
  echo "ingest failed"; echo "$GUARD"; exit 1
fi
HEAD="$(printf '%s\n' "$GUARD" | head -n1)"
case "$HEAD" in
  NO_EXPORT|NO_NEW_ITEMS) echo "nothing to do"; exit 0 ;;
esac
TOTAL="$(printf '%s\n' "$HEAD" | awk '/^NEW_ITEMS/ {print $4}')"   # "NEW_ITEMS 5 of 53 ..."
TOTAL="${TOTAL:-?}"

# Serialize runs (Downloads fires WatchPaths repeatedly). Portable atomic lock
# via mkdir — macOS has no flock by default.
if ! mkdir "$LOCKDIR" 2>/dev/null; then
  echo "another run in progress"; exit 0
fi
trap 'rmdir "$LOCKDIR" 2>/dev/null || true' EXIT

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
notify "Done ✓ $DONE bookmark(s) processed — vault updated"
echo "ingest run complete"
