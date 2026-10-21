# bookmark-ingestion

Self-updating design-inspiration system: a launchd daemon watches ~/Downloads for X
bookmark exports, ingests new bookmarks (tools/ingest), tears down design-worthy sites
via headless claude -p + Playwright, classifies them against tools/ingest/taxonomy.json,
and regenerates an Obsidian knowledge-graph vault at inspo/vault/.

**Read `CONTEXT.md` first:** it covers the purpose, current state, direction and a map of every doc.

## Standing rules

- **Iteration log (mandatory):** after any meaningful change to the pipeline, SOP,
  schema, taxonomy, vault format, or daemon infra, append an entry to
  `inspo/vault/ITERATIONS.md` (structure: What we built / What broke or learned /
  What replaced it and why; update Open threads). Do this unprompted, in the same
  piece of work. See the global skill `inspo-iterations-log`.
- `inspo/inspiration.json` is the single source of truth; `inspiration.md` and
  `inspo/vault/` are generated views (never hand-edit generated notes; ITERATIONS.md
  is the hand-written exception and is preserved by rebuilds).
- Run tests with `.venv/bin/python -m pytest -q` before committing.
- The daemon runs unattended: keep run.sh chunked + resumable, keep enrichment on
  Sonnet (NEOUD_ENRICH_MODEL), never let a failure advance the ledger.
- Commit + push to the private repo (github.com/neoudhaile/bookmark-ingestion) after
  substantive changes.
