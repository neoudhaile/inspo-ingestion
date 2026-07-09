#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
VENV=.venv/bin/python
LOCKDIR=/tmp/neoud-ingest.lock.d
CHUNK=5   # enrich at most this many new items per claude -p call

# Cheap no-op guard (before locking): is there anything new at all?
if ! GUARD="$("$VENV" -m tools.ingest.ingest --limit "$CHUNK" 2>&1)"; then
  echo "ingest failed"; echo "$GUARD"; exit 1
fi
case "$(printf '%s\n' "$GUARD" | head -n1)" in
  NO_EXPORT|NO_NEW_ITEMS) echo "nothing to do"; exit 0 ;;
esac

# Serialize runs (Downloads fires WatchPaths repeatedly). Portable atomic lock
# via mkdir — macOS has no flock by default.
if ! mkdir "$LOCKDIR" 2>/dev/null; then
  echo "another run in progress"; exit 0
fi
trap 'rmdir "$LOCKDIR" 2>/dev/null || true' EXIT

# Enrich in resumable chunks: each pass ingests up to CHUNK new items, enriches,
# and applies (which advances the ledger), so the next pass returns the NEXT chunk
# until none remain. A big catch-up export (dozens of new bookmarks) thus never goes
# through one giant claude -p call; if a chunk fails (rate limit), earlier chunks are
# already applied and the next daemon fire resumes from where it stopped.
while true; do
  if ! OUT="$("$VENV" -m tools.ingest.ingest --limit "$CHUNK" 2>&1)"; then
    echo "ingest failed: $OUT"; exit 1
  fi
  case "$(printf '%s\n' "$OUT" | head -n1)" in
    NO_EXPORT|NO_NEW_ITEMS) break ;;
  esac
  echo "chunk: $(printf '%s\n' "$OUT" | head -n1)"
  bash tools/ingest/enrich.sh
  "$VENV" -m tools.ingest.apply_enriched
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
echo "ingest run complete"
