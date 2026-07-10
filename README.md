# bookmark-ingestion

A self-updating **design-inspiration system**. I bookmark tweets that showcase great
websites; this repo turns those bookmarks — automatically — into a searchable,
browsable knowledge graph of **design teardowns**: what each site is, what it shows,
how it works, how it's designed, its real palette/fonts/tech (read from the DOM, not
eyeballed), a full-page screenshot, and a classification that connects it to every
related site.

Current corpus: **256 bookmarks · 155 site teardowns · 155 full-page screenshots**,
rendered into an Obsidian vault where sites cluster by what they are and how they feel.

## How it works

```
you bookmark on X
      │
      ▼
twitter-web-exporter  ──►  ~/Downloads/twitter-Bookmarks-<ts>.json   (full snapshot)
      │                                      │
      │                        launchd daemon (WatchPaths) fires run.sh
      ▼                                      ▼
┌─ deterministic Python (tools/ingest) ──────────────────────────────┐
│ diff export vs _ledger.json by tweet id → harvest real URLs from   │
│ the export metadata (t.co → destination) → new-items.json (chunks  │
│ of 5)                                                              │
└──────────────────────────────┬─────────────────────────────────────┘
                               ▼
┌─ claude -p enrichment (Sonnet, headless, isolated Playwright) ─────┐
│ per bookmark: title/category/tags · primary-URL judgment · view    │
│ attached photos / frame-sample videos and describe them            │
│ per design-worthy site: full teardown — fullPage screenshot, DOM   │
│ probe (CSS vars, document.fonts, computed colors, meta, framework  │
│ globals), mobile pass, prose analysis, and facet classification    │
│ against tools/ingest/taxonomy.json                                 │
└──────────────────────────────┬─────────────────────────────────────┘
                               ▼
┌─ deterministic writers ────────────────────────────────────────────┐
│ merge into inspo/inspiration.json (source of truth) → regenerate   │
│ inspiration.md + the Obsidian vault → advance ledger → archive     │
└─────────────────────────────────────────────────────────────────────┘
```

Design decisions that matter:

- **Deterministic/judgment split.** Everything idempotent and file-mutating is plain
  Python with tests; the model only does what a script can't (pick the subject site,
  write prose, classify facets, describe a video).
- **Chunked + resumable.** Big catch-up exports process 5 bookmarks per `claude -p`
  call; the ledger advances per chunk, so a rate-limit stop resumes exactly where it
  left off. Corrupt/empty exports are skipped, never wedge the pipeline.
- **Anti-hallucination extraction.** Colors and fonts must come from
  `getComputedStyle` / `document.fonts` / CSS custom properties — never from looking
  at the screenshot.
- **Visible.** The daemon posts macOS notifications: run started (N bookmarks),
  per-chunk progress, failures, and "Done ✓ — vault updated".

## How it's organized

| Path | What it is |
|---|---|
| `inspo/inspiration.json` | **Source of truth** — all bookmarks (`items[]`) + all teardowns (`site_designs{}`, schema documented in its `_schema` key) |
| `inspo/vault/` | **Generated Obsidian vault** — one note per website + `INDEX.md` (facet map) + `ITERATIONS.md` (hand-written project history; survives rebuilds) |
| `inspo/inspiration.md` | Generated human-readable digest of the bookmarks |
| `inspo/_ledger.json` | Processed tweet ids + provenance (the dedup authority) |
| `inspo/_archive/` | Raw exports, kept forever |
| `screenshots/` | Full-page PNG per torn-down site |
| `tools/ingest/` | The pipeline: `ingest.py` (diff/harvest) · `enrich.sh` + `enrich_prompt.md` (the model SOP) · `writers.py` / `apply_enriched.py` (merge) · `render_vault.py` (vault) · `taxonomy.json` (the facet vocabulary) · `classify_facets.py` (backfill classifier) · `backfill.py` (teardown backfill) · launchd plist + `INSTALL.md` |
| `run.sh` | Daemon entrypoint: guard → lock → chunk loop → vault rebuild → archive |
| `tests/` | pytest suite for every deterministic stage |

## How to use the inspiration

**In Obsidian:** open `inspo/vault/` as a vault (File → *Open folder as vault* — pick
this exact folder). Turn **Tags** on in Graph view. Sites connect through four
controlled facets (vocabulary in `tools/ingest/taxonomy.json`):

- `#vertical/…` — what the site **is** (portfolio, startup-product, personal-blog, tool-app, studio-agency…)
- `#vibe/…` — how it **feels** (minimal, editorial, playful, brutalist, luxury, technical…)
- `#topic/…` — what it's **about** (startups, ai, design, photography…) — topics *bridge*
  clusters: a personal blog about startups links into the startup world
- `#mode/dark` / `#mode/light`

Each note holds the full teardown (prose + design data + screenshot) and a
**Related sites** list with the reason printed (`[[kmk0.com]] — shared: portfolio,
playful, light`).

**From the command line / an agent:**

```bash
# the vocabulary + counts
cat inspo/vault/INDEX.md

# dark portfolios
rg -l '#vertical/portfolio' inspo/vault | xargs rg -l '#mode/dark'

# anything about startups, whatever kind of site it is
rg -l '#topic/startups' inspo/vault
```

Then read just those notes (~4 KB each) — never the 1 MB JSON. A global Claude Code
skill (`design-inspiration`) teaches agents this traversal automatically; the raw
JSON remains the fallback for complex ad-hoc queries.

## How to add more inspiration (the loop you actually live)

1. **Bookmark** tweets on X that showcase sites you like (works even when the tweet
   is only a video/image — media gets viewed and described).
2. **Export bookmarks** with [twitter-web-exporter](https://github.com/prinsss/twitter-web-exporter)
   (userscript; on your X bookmarks page, export **Bookmarks as JSON**). Save the
   `twitter-Bookmarks-<timestamp>.json` to `~/Downloads` — the default.
3. **That's it.** The daemon notices the file, diffs out only never-seen bookmarks,
   enriches + tears down + classifies them, and rebuilds the vault. Watch the macOS
   notifications, or `tail -f /tmp/neoud-ingest.log`.

Manual controls, if you ever want them:

```bash
./run.sh                                        # run the whole pipeline now
.venv/bin/python -m tools.ingest.render_vault   # just regenerate the vault
.venv/bin/python -m tools.ingest.classify_facets  # (re)classify facets on any sites missing them
.venv/bin/python -m pytest -q                   # test suite
```

### Setting it up fresh (new machine)

See `tools/ingest/INSTALL.md` for the full walkthrough (launchd agent, the dedicated
`neoud-bash` interpreter trick for macOS TCC, and the isolated headless Playwright
config). The short list: Python 3.9+ venv with pytest, **Node ≥ 20** on the daemon's
PATH (`@playwright/mcp` refuses older), Claude Code installed at `~/.local/bin/claude`,
and the plist from `tools/ingest/` loaded via `launchctl`.

## Project history

The full build story — every architecture iteration, dead end, and macOS fight — is
documented in [`inspo/vault/ITERATIONS.md`](inspo/vault/ITERATIONS.md), updated
continuously as the system evolves.
