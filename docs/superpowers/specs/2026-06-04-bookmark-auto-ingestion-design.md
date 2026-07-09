# Bookmark Auto-Ingestion Pipeline — Design

**Date:** 2026-06-04
**Status:** Approved design, pending spec review
**Repo:** neoud.net

## Goal

Close the loop on the inspiration bucket. Today, ingesting X (Twitter) bookmarks
into `inspo/inspiration.json` / `inspiration.md` is manual and model-assisted.
This pipeline makes it automatic: whenever a fresh bookmarks export lands, new
bookmarks are diffed, parsed, enriched (title / category / tags / primary URL),
optionally torn down for design tokens (`site_designs`), and merged into the
inspiration bucket — automatically, idempotently, and traceably.

## Decisions (locked during brainstorming)

| Decision | Choice | Rationale |
|---|---|---|
| Bookmark source | Manual re-export, auto-processed | Free, no X API tier, user controls cadence |
| Per-item scope | Ingest + auto-teardown | Richest; teardown runs only on resolvable homepages |
| Trigger | Folder-watch daemon (`launchd` `WatchPaths`) | Fires the instant an export lands |
| Watched folder | `~/Downloads` directly | Zero habit change; browser saves exports there |
| Filter strictness | Keep all, tag aggressively | Nothing lost; tags/category do the filtering later |
| Script/model split | Hybrid: deterministic `ingest.py` + `claude -p` enrichment | Script can't reproduce inferred URLs / titles / tags |

## Feasibility findings (from the real export)

Source export inspected: `~/Downloads/twitter-Bookmarks-1779930252646.json` (154 items).

- **Flat list** of bookmark objects, each with stable `id`, `created_at`,
  `full_text`, `screen_name`, `name`, `url`, and a full `metadata` GraphQL blob.
- **Full snapshot every export** (not a delta) → diffing by `id` against a ledger
  is trivial and reliable.
- `full_text` carries only `t.co` links. Top-level `entities.urls` recovers real
  external links for only **16/154**. A **deep walk of the whole record**
  (card unfurls, quoted tweets, bios inside `metadata`) recovers external URLs for
  **127/154** — including the contextual ones like `weirdfolders.com`. The
  remaining ~27 are genuinely link-free text/quote tweets.
- Conclusion: deterministic harvest gets ~82% of links; choosing the *primary*
  site, writing titles, and assigning category/tags still need the model. Hence
  the hybrid design.

## Architecture

Four stages. Only stage 1 is always-on.

```
[1] launchd WatchPaths daemon ──new file──▶ [2] ingest.py (deterministic, no network)
      watches ~/Downloads                        • glob twitter-Bookmarks-*.json, newest
                                                  • diff vs _ledger.json by tweet id
                                                  • deep-walk metadata → harvest URLs
                                                  • normalize → _inbox/new-items.json
                                                            │
[4] write-back ◀── enriched items ── [3] claude -p (judgment + browser)
   • merge inspiration.json              • keep-all filter; flag noise via tags
   • regenerate inspiration.md           • pick PRIMARY url from candidates
   • append site_designs                 • write title, category, tags
   • update _ledger.json                 • Playwright teardown on resolvable homepages
   • archive raw export
```

## Components

### 1. Watcher — `launchd` agent
- A `~/Library/LaunchAgents/net.neoud.bookmark-ingest.plist` with `WatchPaths`
  set to `~/Downloads`.
- `~/Downloads` is noisy, so the launched script must **cheaply no-op** when no
  new/unprocessed `twitter-Bookmarks-*.json` is present (glob + ledger check
  before any real work).
- Runs `run.sh`, which runs `ingest.py` then, only if new items exist, invokes
  `claude -p` for enrichment.

### 2. `ingest.py` — deterministic ingest (unit-testable, no network, no model)
- **Input:** newest `twitter-Bookmarks-*.json` in `~/Downloads`.
- **Diff:** load `inspo/_ledger.json` (set of processed tweet ids); compute new ids.
- **Harvest:** for each new item, deep-walk the record for `https?://` strings;
  drop twitter/t.co/twimg; dedup; keep ordered candidate list.
- **Normalize:** emit `inspo/_inbox/new-items.json` — one object per new bookmark
  with `id`, `date`, `author`, `name`, `author_profile`, `tweet`, `full_text`,
  `candidate_urls`, `media_kinds`.
- **Output contract is the seam** between deterministic and model stages.

### 3. Enricher — `claude -p` headless (in-repo, MCP-enabled)
- Reads `new-items.json`. For each item:
  - **Keep-all filter:** every item is ingested. Items that are pure text / no
    resolvable site are tagged (`uncategorized`, `thread`, etc.) rather than dropped.
  - **Primary URL:** choose the subject site from `candidate_urls`. Apply a
    **utility-domain denylist** (`linktr.ee`, `typefully.com`, `cal.com`,
    `calendly.com`, `medium.com`, `docs.google.com`, `framer.link`, and similar
    booking/footer/bio links) so they never become the primary URL — though they
    may still be kept in `all_urls`. When a tweet links both a showcased site and
    the author's portfolio (e.g. `12matcha.com` + `ryanyee.xyz`), the model picks
    the subject as primary and demotes the rest to `related_urls`.
  - **List tweets (one bookmark → many sites):** some bookmarks are curated lists
    that link many sites at once (observed: a 10-site thread, an 8-site thread).
    These become a single inspiration item whose `all_urls` / `related_urls` hold
    every site, and each design-worthy domain is eligible for its own
    `site_designs` teardown. The item is tagged `directory`/`thread` so it reads
    as a collection, not a single-site bookmark.
  - **Metadata:** write `title`, `category` (from existing category set), `tags`
    (from existing tag glossary; may add new tags).
  - **Teardown:** if the primary URL resolves to a loadable homepage, run the
    Playwright `site_designs` teardown (screenshot + hover + scroll) per the
    locked prose schema (`what_it_is` / `what_it_shows` / `how_it_works` /
    `how_its_designed` + one-line `palette` + `fonts` + `pattern_keywords`).
    On failure, record `teardown_status: failed` and continue.

### 4. Writers
- Merge enriched items into `inspiration.json` `items[]` (append; never rewrite
  existing items), preserving the user's section-12 favorites and manual adds.
- Append new `site_designs` entries keyed by domain (skip if domain already present).
- Regenerate `inspiration.md` from `inspiration.json` (the JSON is source of truth).
- Update `_ledger.json` with the newly processed ids + `source_export` + `ingested_at`.
- Move/copy the raw export to `inspo/_archive/<original-filename>`.

## Data & files

| Path | Role |
|---|---|
| `~/Downloads/twitter-Bookmarks-*.json` | Watched input (existing browser export) |
| `inspo/_inbox/new-items.json` | Hand-off from `ingest.py` → enricher (transient) |
| `inspo/_archive/` | Every raw export, timestamped, kept for provenance |
| `inspo/_ledger.json` | `{ processed_ids, by_id: {id: {source_export, ingested_at}} }` |
| `inspo/inspiration.json` | Source of truth (items + site_designs) |
| `inspo/inspiration.md` | Regenerated view |

**New per-item fields:** `source_export`, `ingested_at` (provenance / traceability).

## Traceability & idempotency

- `_ledger.json` is the dedup authority: re-running on the same or a superset
  export never duplicates.
- Every item records which export it came from and when.
- Raw exports are archived, so the bucket is always reconstructible from sources.

## Failure handling

- `ingest.py` is pure and cannot partially corrupt the bucket — it only writes
  `new-items.json`.
- Enricher writes are atomic per run (write to temp, validate JSON parses, swap).
- Teardown failures are recorded, not fatal.
- If `claude -p` fails entirely, the ledger is NOT updated, so the next run retries
  the same new items.

## Build order

1. **`ingest.py` + ledger + tests** — validate diff/harvest on the real 154-item export.
2. **Enricher prompt/skill + writers** — run as a manual command; validate output
   merges cleanly and matches existing JSON/MD shape on a few new items.
3. **`run.sh` orchestration** — wire stages, atomic writes, archiving.
4. **`launchd` daemon** — wrap as the trigger only after 1–3 are proven by hand.

Rationale: the daemon is just a trigger; proving the pipeline before automating it
prevents a background job from silently mangling the inspiration bucket.

## Out of scope (YAGNI)

- X API integration / live polling.
- Browser-automation scraping of x.com.
- Multi-device sync (revisit only if exporting from non-Mac devices becomes common).
- Re-tearing-down sites already in `site_designs`.

## Open considerations (not blockers)

- `claude -p` headless must have the Playwright MCP server configured and adequate
  permissions to drive the browser unattended.
- `WatchPaths` on `~/Downloads` may fire frequently; the no-op guard must be cheap.
