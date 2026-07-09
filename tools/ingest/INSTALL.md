# Install the bookmark-ingest daemon

The daemon watches `~/Downloads` and runs the ingestion pipeline whenever a new
`twitter-Bookmarks-*.json` export lands.

## Install

1. Copy the plist into LaunchAgents:
   ```bash
   cp tools/ingest/net.neoud.bookmark-ingest.plist ~/Library/LaunchAgents/
   ```
2. Load it:
   ```bash
   launchctl load ~/Library/LaunchAgents/net.neoud.bookmark-ingest.plist
   ```
3. Confirm it's registered:
   ```bash
   launchctl list | grep neoud
   ```
4. Test: re-export your X bookmarks to `~/Downloads`, then watch the log:
   ```bash
   tail -f /tmp/neoud-ingest.log
   ```

## macOS permissions: scoped dedicated interpreter (`neoud-bash`)

A LaunchAgent runs in a restricted TCC context and is blocked from executing scripts
under `~/Documents` / reading `~/Downloads` unless its interpreter has access. Rather
than grant Full Disk Access to the system `/bin/bash` (which would privilege every
script you ever run), the plist points at a **dedicated copy used only by this daemon**:
`~/.local/bin/neoud-bash`.

Create it (one time). On Apple Silicon you MUST thin to x86_64 and re-sign — a raw copy
of `/bin/bash` runs its `arm64e` slice, which macOS reserves for platform binaries and
SIGKILLs (exit 137):

```bash
mkdir -p ~/.local/bin
cp /bin/bash ~/.local/bin/neoud-bash
chmod u+w ~/.local/bin/neoud-bash
lipo ~/.local/bin/neoud-bash -thin x86_64 -output ~/.local/bin/neoud-bash   # Apple Silicon only
codesign --force --sign - ~/.local/bin/neoud-bash                            # ad-hoc re-sign
~/.local/bin/neoud-bash -c 'echo OK'   # must print OK (runs under Rosetta on Apple Silicon)
```

Then (re)load the agent and test:

```bash
launchctl unload ~/Library/LaunchAgents/net.neoud.bookmark-ingest.plist 2>/dev/null
launchctl load   ~/Library/LaunchAgents/net.neoud.bookmark-ingest.plist
date +%s > ~/Downloads/neoud-trigger.txt; sleep 3; rm -f ~/Downloads/neoud-trigger.txt
cat /tmp/neoud-ingest.log   # want: "nothing to do: NO_NEW_ITEMS"
cat /tmp/neoud-ingest.err   # want: empty
```

Requires Rosetta on Apple Silicon (`softwareupdate --install-rosetta --agree-to-license`
if missing). The deterministic-ingest half runs fine this way.

### Fallback: if you ever see `Operation not permitted`

If `/tmp/neoud-ingest.err` shows `neoud-bash: .../run.sh: Operation not permitted`
(can happen in a different login context), grant Full Disk Access to the dedicated
copy — one GUI step, scoped to just this binary:

1. **System Settings → Privacy & Security → Full Disk Access → `+`**
2. Press **⌘⇧G**, enter `~/.local/bin/neoud-bash`, add it, toggle **ON**.
3. Reload the agent (the two `launchctl` lines above).

## Requirements / caveats

- **Real `claude`, not a wrapper:** `enrich.sh` invokes the real binary at
  `$HOME/.local/bin/claude` (override with `CLAUDE_BIN`). It deliberately avoids the
  cmux `claude` wrapper, which only works inside a cmux terminal and fails from launchd.
- **node/npx on PATH for Playwright:** the teardown step runs an `--isolated --headless`
  Playwright MCP via `npx @playwright/mcp@latest` (config: `tools/ingest/mcp.playwright.json`,
  pinned with `--strict-mcp-config`). The plist PATH includes the nvm node bin so `npx`
  resolves; update `NEOUD_NODE_BIN` / the plist PATH if your node version dir changes.
  Isolated+headless means the daemon's browser never collides with an interactive Claude
  session's persistent profile (which otherwise throws a profile-lock error). If Playwright
  is unavailable, enrichment still ingests + tags and simply skips teardowns.
- **Unattended permissions:** `enrich.sh` passes `--dangerously-skip-permissions` so
  browser + file tools run without interactive prompts. It's a self-authored prompt on
  your own machine; remove it if you'd rather approve each run.
- **`~/Downloads` is busy:** `WatchPaths` fires on any change there. `run.sh` no-ops
  cheaply (it runs only the fast deterministic ingest and exits early on
  `NO_EXPORT` / `NO_NEW_ITEMS`), and serializes concurrent fires with a `mkdir` lock.
- **macOS only** (launchd). The deterministic core (`ingest.py`, writers) is portable;
  only this trigger is platform-specific.

## Reply/comment links (optional, off by default)

The daemon's Playwright runs **isolated and logged out** of X. It captures links from the
tweet body (resolved to real URLs via the export metadata) and attached media — but it
cannot read links that appear *only* in the author's replies/comments, since X hides those
from logged-out viewers. In practice almost all design bookmarks put the link in the tweet
body, so this is a rare gap, and staying logged out is safer for your X account.

If you later decide you want reply-link reading, switch the daemon to a dedicated logged-in
profile: in `tools/ingest/mcp.playwright.json` replace `"--isolated"` with
`"--user-data-dir", "/Users/<you>/.neoud/x-profile"`, then log in once with
`npx --yes playwright open --user-data-dir="$HOME/.neoud/x-profile" "https://x.com/i/flow/login"`.

## Uninstall

```bash
launchctl unload ~/Library/LaunchAgents/net.neoud.bookmark-ingest.plist
rm ~/Library/LaunchAgents/net.neoud.bookmark-ingest.plist
```
