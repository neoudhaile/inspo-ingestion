# Iterations — how the bookmark pipeline actually got built

This is the running engineering log of the bookmark-ingestion project (2026-06-04 → ongoing): a system that turns X/Twitter bookmarks into a queryable design-inspiration knowledge base. It started as a hand-curated markdown file and became a launchd daemon that watches `~/Downloads`, diffs bookmark exports against a ledger, harvests real URLs out of Twitter's metadata blob, drives a headless Claude + Playwright enrichment pass that tears down each site (DOM-probed colors, fonts, tech stack, media descriptions), and renders everything into this Obsidian vault where 155 sites connect through four controlled facets. Nothing here went right the first time. This file documents every pathway — including the dead ends — as raw material for a future write-up.

## System at a glance (current)

- **Trigger:** launchd `WatchPaths` agent on `~/Downloads` → `run.sh`, serialized with a `mkdir` lock (macOS ships no `flock`).
- **Deterministic core:** `tools/ingest/ingest.py` diffs the newest `twitter-Bookmarks-*.json` against `inspo/_ledger.json` (332 tweet ids processed so far), deep-walks each record for URLs, and emits chunks of at most 5 items.
- **Judgment layer:** `claude -p` (Sonnet, via `NEOUD_ENRICH_MODEL`) with an isolated headless Playwright MCP — picks the primary URL, writes prose teardowns, probes the DOM for real tokens, views/describes attached media, and classifies each site against `tools/ingest/taxonomy.json`.
- **Deterministic writers:** merge into `inspiration.json` (256 items, 156 site teardowns — the source of truth), splice a managed region into `inspiration.md`, advance the ledger, archive the export, and rebuild this vault (`render_vault.py`).
- **The vault:** one note per site, connected by four facets — vertical (11 values), vibe (10), topic (18), mode (3). 40 tag nodes, 919 explainable site↔site edges. See `INDEX.md`.
- **Backed up:** private repo at github.com/neoudhaile/bookmark-ingestion (232 MB including full-page screenshots).

---

## Iteration 0 — Manual curation and the color-heavy teardown (2026-06-04)

**What we built.** X bookmarks manually exported to JSON, then hand-assembled into `inspiration.md` + `inspiration.json` with categories and tags. Alongside it, the idea of a per-site "design teardown": open the site in a browser and record how it's built. The first live teardown was [[weirdfolders.com]] via the Playwright MCP, using a heavily structured, color-token-centric schema — palette arrays, design tokens, a type scale.

**What broke.** The schema optimized for the wrong thing. Owner feedback, verbatim: "this schema is really color heavy… I want it to be about the website, what it does, how it's designed, in text." A teardown that's mostly hex codes tells you nothing about why a site is worth bookmarking.

**What replaced it.** The prose pivot below. Lesson zero of the project: the first schema you design will encode what's easy to extract, not what you actually want to know.

## Iteration 1 — The prose-forward schema (2026-06-04)

**What we built.** The teardown was redesigned around four prose fields — `what_it_is` / `what_it_shows` / `how_it_works` / `how_its_designed` — plus a one-line palette, a one-line fonts note, and a `pattern_keywords[]` array. Color got demoted from arrays of tokens to a single sentence.

**Why it stuck.** This is still the spine of every site note in the vault (see any note, e.g. [[mo1.app]]). Everything added later — DOM probes, tech stack, media — hangs off these four paragraphs rather than replacing them. It was an explicitly human decision point, and it shaped the whole system: the database is for *reading about* websites, with structured data in a supporting role.

## Iteration 2 — Automating ingestion: the daemon (design 2026-06-04)

**What we built.** With the schema settled, the manual loop needed closing. Brainstormed bookmark sources: the paid X API, logged-in scraping of x.com, a share-sheet webhook, or manual re-export auto-processed. Chose manual re-export — free, no API tier, and the user controls cadence.

The feasibility test on a real 154-item export produced the finding the whole architecture rests on: tweet text carries only `t.co` stubs, and the top-level `entities.urls` recovers real destinations for just **16/154** bookmarks. But a deep recursive walk of the export's full metadata blob — card unfurls, quoted tweets, author bios — recovers **127/154** (~82%). The remaining ~27 are genuinely link-free tweets. So: a deterministic script can harvest links, but choosing the *primary* site (a tweet linking both `12matcha.com` and the author's portfolio should file under [[12matcha.com]]), writing titles, and tagging still need a model. Hence the hybrid split.

Architecture: launchd `WatchPaths` on `~/Downloads` → deterministic Python ingest (diff by tweet id against a ledger; recursive URL harvest; utility-domain denylist so `linktr.ee`/`cal.com` never become the primary URL) → `claude -p` enrichment (title/category/tags/primary-URL judgment + Playwright teardowns) → deterministic writers (merge JSON, splice a managed region into the md so hand-written prose is never touched, ledger update, archive the raw export). Built via a 13-task TDD plan executed with subagent-driven development, 20+ unit tests, then validated live on a 33-bookmark delta before the daemon was ever armed. The daemon was deliberately built *last* — it's just a trigger, and a background job should not be automated until the pipeline it triggers is proven by hand.

## Iteration 3 — The daemon hardening saga: macOS fights back (June 2026)

The pipeline worked when run by hand. Making it work *unattended under launchd* took six distinct fixes, each of which is its own small war story:

1. **TCC.** launchd jobs get no Downloads/Documents access by default — the daemon died with "Operation not permitted" reading the very folder it watches.
2. **The killed bash.** Solution to #1: copy the interpreter to a dedicated path (`~/.local/bin/neoud-bash`) so TCC permissions can be granted to *it* specifically. Except macOS SIGKILLed the copy (exit 137): a copied `/bin/bash` executes its **arm64e** slice, an ABI reserved for platform binaries. Fix: `lipo`-thin the copy to x86_64 and ad-hoc codesign it — the daemon's shell now runs under Rosetta, on an Apple Silicon Mac, on purpose.
3. **The wrong `claude`.** The `claude` on PATH was a cmux terminal wrapper that fails headless. The daemon must point at the real binary (`~/.local/bin/claude`).
4. **The missing `npx`.** Playwright MCP wouldn't launch because `npx` lives inside nvm, which a daemon PATH knows nothing about. The plist now hardcodes the node bin dir (`~/.nvm/versions/node/v18.20.8/bin`).
5. **Profile locks.** The daemon's browser collided with interactive Claude sessions using the same profile. Fix: a dedicated MCP config running `--isolated --headless`, loaded with `--strict-mcp-config` so nothing else leaks in.
6. **Permissions.** `--dangerously-skip-permissions` for unattended tool use — acceptable because the deterministic writers, not the model, own every file mutation.

The meta-lesson: "works in my terminal" and "works as a launchd daemon" are separated by the entire macOS security model.

## Iteration 4 — Audit-driven extraction: stop eyeballing (early June 2026)

**What broke.** An adversarial audit subagent was pointed at the extraction SOP and scored it **6/10**, with receipts: a teardown claimed an "orange accent" where the site's CSS variable was actually grey `#666`; EB Garamond was loaded but never mentioned; the tech stack was visible in script tags and discarded; no mobile pass existed. The model had been *eyeballing* screenshots and hallucinating plausible design tokens.

**What replaced it.** A mandatory DOM probe: one `browser_evaluate` call pulls CSS custom properties, `document.fonts`, sampled computed colors, meta/OG tags, element counts, headings, `scrollHeight`, framework globals, and script hosts. Plus fullPage screenshots, a text-first mobile resize pass (390×844), and an explicit anti-hallucination rule: colors and fonts MUST come from the DOM, never from looking at pixels. New structured fields landed: `tech_stack`, `palette_tokens` (each marked `var` or `rendered`), `fonts_loaded`, `meta`, `media_mix`, `page_height_px`, `headings`, `responsive_note`, `links_out`, `weight`. The [[mo1.app]] note shows the payoff — it correctly reports `--highlight-color: #fe9024`, `--accent: #666`, and that the site ships *no webfont at all*, the exact class of facts the old SOP got wrong.

This also established the project's working method: **audit → fix → re-verify**, with the audit run by an agent instructed to be adversarial rather than agreeable.

## Iteration 5 — Media understanding (June–July 2026)

**What broke.** Many bookmarked tweets showcase the cool thing in an image or video with *no link at all*. The pipeline was filing them as "uncategorized, link-free" — losing exactly the content they were bookmarked for.

**What we built.** Photos are downloaded and actually viewed by the model; videos are frame-sampled at 25/55/85% of duration via Chromium seek-and-screenshot — after discovering the hard way that Playwright's bundled ffmpeg cannot demux tweet mp4s. Each media item gets a stored description. Link provenance also got formalized: `resolved_links[]` records every URL with a `role` (primary / author-portfolio / related / reply-link) and `source` (tweet-body / reply / metadata).

**A deliberate dead end not taken:** logging into X from the automation browser would surface reply-only links, but risks the account. Decision: stay logged out and accept that reply links are best-effort. Another explicit human call.

## Iteration 6 — Scale and economics (June–July 2026)

**What we built.** The full backfill: the corpus went from **12 → 115 teardowns** across resumable chunked runs, surviving two rate-limit stops by design (the ledger only advances on success, so a killed run simply resumes).

**What broke along the way.**
- **The churn bug:** domains the enricher *declined* to tear down were never recorded, so every run re-queued them forever. Fixed with an attempted-set (`inspo/_backfill_attempted.json`, now 108 entries) — "we tried" is state worth persisting, distinct from "we succeeded".
- **The 53-bookmark near-miss:** a catch-up export almost went through as ONE giant `claude -p` call — one rate limit away from losing everything. `run.sh` was redesigned to loop in chunks: `ingest --limit 5` per enrich pass, apply, advance the ledger, repeat. A failed chunk costs one chunk.
- **Economics:** enrichment switched from Opus to Sonnet via `NEOUD_ENRICH_MODEL`. On subscription billing there's no per-token cost, but rate limits are real — and screenshots (images) turned out to be the dominant token cost, not text.

## Iteration 7 — The move, or: how we lost our own history (~2026-07-05)

The project was relocated out of its parent repo (neoud.net) into a standalone directory — and the `.git` stayed behind. All commit history from the first month is gone; `git log` here starts 2026-07-05 with a single squashed "Initial commit". The daemon also broke (its plist pointed at absolute paths in the old location) and the venv had to be recreated.

Lesson, and a real one: **absolute paths plus externally-registered daemons make a project move-hostile.** launchd doesn't know your repo moved; TCC grants don't follow; venvs embed their own path. The fix was mechanical (re-point the plist, rebuild the venv, fresh `git init`, private GitHub backup — 232 MB with screenshots), but the early history is unrecoverable, which is partly why this file exists.

## Iteration 8 — Vault v1: hub-and-spoke (July 2026)

**What we built.** The first knowledge-graph rendering of the corpus: one note per site plus *hub notes* per pattern, category, tech, color, font, and aesthetic, all joined by wikilinks, with an INDEX as the entry point. Inspired by Karpathy's llm-wiki (index → small linked pages) and PuppyGraph's knowledge-graph-agent (walk typed edges instead of scanning): an agent should read ~20 KB per lookup instead of grepping the 1.1 MB `inspiration.json`.

**What broke.** The first build exploded: **779 pattern hubs, 292 tech hubs, 203 font hubs** — the overwhelming majority linking exactly one site. A hub with one spoke is just a file. Share-thresholds (only create a hub if N+ sites share the value) cut it to ~210 notes, but the underlying problem remained: free-text keywords produce a graph of singletons.

## Iteration 9 — Vault v2: flat notes + free tags (July 2026)

**What we built.** Owner direction: "each node is a website; tags connect them." So: kill the hubs, one note per site carrying ALL its data, connected by nested tags (`#pattern/x`, `#tech/x`, `#font/x`, …). Committed as "Redesign vault: one flat note per website, connected by nested tags".

**What broke.** The Obsidian graph was a hairball: **1,277 tag nodes, 76% of them singletons** connecting nothing, at **~18.6 tags per note**. Same disease as v1 in different clothes — moving free-text vocabulary from hub notes into tags doesn't make it a controlled vocabulary. Also a comedy gotcha: Obsidian silently created a fresh empty vault in a subfolder, so the owner opened the graph and saw *nothing* — the first debugging session was against the wrong vault.

## Iteration 10 — Vault v3: controlled facets (July 2026, current)

**What we built.** Stepped back to first principles: what is the vault *for*? Answer: finding sites by **KIND** (vertical — what it is) and **FEEL** (vibe — how it reads), with **TOPIC** bridging clusters (a personal blog *about* startups links into the startup-product cluster) and **mode** (dark/light) as a cheap filter. `tools/ingest/taxonomy.json` became the contract — 11 verticals, 10 vibes, 18 topics, 3 modes, each value defined in prose so both the enricher and a backfill classifier apply them consistently.

The 155 existing sites were backfilled by a chunked, text-only `claude -p` classifier (no browser — it classifies from the already-extracted prose, 20 sites per call, resumable). New sites get facets from the enricher at ingest time.

**The numbers that justify three iterations:** **40 tag nodes (3 singletons)** versus v2's 1,277 (976 singletons); **919 site↔site edges**, each printed with its WHY in the note's Related-sites section ("shared: portfolio, minimal, dark"). The granular detail — keywords, tech, fonts — stays in the notes as searchable text and never becomes graph structure. The taxonomy is the graph; everything else is grep.

## Working methods worth naming

- **The audit → fix → re-verify loop.** An adversarial subagent scoring the SOP (Iteration 4) caught what self-review never would. This became the default way to harden any stage.
- **Deterministic/judgment split.** Everything idempotent, diffable, and file-mutating is plain Python with tests; the model only does what a script cannot (pick the subject site, write prose, classify). The seam between them is a JSON contract in `inspo/_inbox/`.
- **Explicit human decision points.** The prose schema pivot, staying logged out of X, Opus→Sonnet, keeping the backup private — none of these were model decisions, and recording them as decisions is part of the design record.
- **The `design-inspiration` skill.** A global skill in `~/.claude/skills` teaches any future agent how to traverse the vault (facet tags → notes → screenshots), so the corpus is consumable without knowing this project's internals.

## Iteration 11 — Visibility and self-documentation (2026-07-10)

**What we built.** Two operator-experience upgrades. First, the daemon now talks: `run.sh` posts macOS notifications (top-right, via `osascript`) when a run starts ("Started — N new bookmarks"), per chunk ("Parsing 5 websites… 10 done, 38 remaining"), on failure ("will resume next fire"), and on completion ("Done ✓ N processed — vault updated"). A background process that rewrites your data shouldn't be invisible. Second, the project became self-documenting: a global skill (`inspo-iterations-log`) plus a repo `CLAUDE.md` instruct any agent that changes the pipeline to append to this very file unprompted — the log stops depending on the owner remembering to ask.

**What broke or what we learned.** The first real-world test arrived immediately: a fresh bookmark export downloaded as a 2-byte file containing `[]` (X produced an empty export). `newest_export()` picked files purely by mtime, so the corrupt newest file would have shadowed the valid 4.4 MB export behind it — the daemon would have reported "nothing to do" forever.

**What replaced it and why.** `newest_export()` now walks candidates newest-first and returns the first that parses to a non-empty JSON list, logging `SKIPPING invalid/empty export` for the rest. A failed download can no longer wedge the pipeline; it degrades to the last good snapshot.

## Open threads

- **Queued bookmarks:** the enrichment inbox (`inspo/_inbox/`) still holds items mid-flight; confirm the daemon fully drains the current backlog unattended, end to end.
- **Taxonomy evolution:** values may be added "sparingly" per the contract, but there's no consolidation process yet — no review cadence for merging near-duplicate vibes/topics or re-classifying when definitions drift.
- **Media descriptions are uneven:** only items ingested after Iteration 5 have viewed-and-described photos/videos; older items were never backfilled.
- **Backup is manual:** the private GitHub remote exists, but pushes aren't automated; a daemon that writes data hourly deserves an auto-push (or at least a staleness alarm).
- **Screenshot weight:** 232 MB and growing, dominated by fullPage screenshots — eventually needs a retention/compression policy or LFS.
- **Vault v3 in anger:** the facet graph is new; the real test is whether Related-sites edges actually surface the right neighbors during a live design task.

## Appending guide

Add new iterations as `## Iteration N — <name> (<date>)` above **Open threads**, keeping the What-built / What-broke / What-replaced-it shape; prune Open threads as they close.
