#!/usr/bin/env bash
# Invoke Claude headless to turn new-items.json into enriched-items.json,
# including Playwright design teardowns.
#
# Two things the daemon's restricted environment needs:
#  1. The REAL claude binary (not the cmux wrapper, which only works in a cmux tty).
#  2. node/npx on PATH so the project-scoped Playwright MCP server (npx
#     @playwright/mcp@latest) can actually launch — otherwise browser tools are
#     unavailable and teardowns silently skip.
set -euo pipefail
cd "$(dirname "$0")/../.."   # repo root

# Put node/npx (nvm) on PATH for the MCP server launch.
NODE_BIN="${NEOUD_NODE_BIN:-$HOME/.nvm/versions/node/v18.20.8/bin}"
[ -d "$NODE_BIN" ] && export PATH="$NODE_BIN:$PATH"

CLAUDE="${CLAUDE_BIN:-$HOME/.local/bin/claude}"
if [ ! -x "$CLAUDE" ]; then
  CLAUDE="$(command -v claude || true)"
fi
if [ -z "$CLAUDE" ] || [ ! -x "$CLAUDE" ]; then
  echo "enrich: no usable claude binary found (set CLAUDE_BIN)" >&2
  exit 127
fi

PROMPT="$(cat tools/ingest/enrich_prompt.md)"
# --model: enrichment is structured extraction + teardown prose + media description;
#   Sonnet handles it well at much lower token cost than Opus. Override with
#   NEOUD_ENRICH_MODEL=opus for a run that wants max quality.
# --dangerously-skip-permissions: required for unattended runs so Playwright MCP
#   browser tools and file writes don't hit interactive permission prompts.
# --mcp-config + --strict-mcp-config: use ONLY a dedicated, isolated+headless
#   Playwright instance so the daemon never collides with the persistent browser
#   profile of an interactive Claude session (which caused a profile-lock error).
"$CLAUDE" -p "$PROMPT" \
  --model "${NEOUD_ENRICH_MODEL:-sonnet}" \
  --dangerously-skip-permissions \
  --mcp-config tools/ingest/mcp.playwright.json \
  --strict-mcp-config
