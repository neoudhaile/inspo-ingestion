# Context: what this repo is, where it stands, and why

Read this first if you're a person or an agent picking the project up cold. It
explains the purpose, what has been built, what is being worked on now, and how. It
doesn't repeat the other docs; it tells you which one to open for each detail.

_Last updated 2026-10-20._

---

## 1. Purpose

A self-updating **design-inspiration library**, built from the owner's own taste.

The owner saves things they like: X bookmarks, saved Instagram reels, links sent
by friends. Normally that judgment disappears into a feed nobody scrolls back
through. This repo treats each save as the start of a pipeline. Every site that
gets saved becomes a **teardown**: what the site is and does, its real palette, fonts
and stack (read from the DOM, never guessed from a screenshot), a full-page
capture, and a place in a graph of related sites.

It serves two uses:

- **Looking it up while designing.** "Light minimal portfolios", "personal sites",
  "sites that use books as a motif". An agent answers these by grepping markdown
  notes, through the global `design-inspiration` skill.
- **Seeing it.** An Obsidian graph where similar sites cluster together. This part
  exists because it looks good. Search is the agent's job.

## 2. Map of the docs

| File | What it's for |
|---|---|
| `CONTEXT.md` | This file: purpose, state, direction. |
| `CLAUDE.md` | **Standing rules for any agent.** Iteration log is mandatory, the source of truth, tests before commit, daemon constraints, push after substantive changes. |
| `README.md` | The front door: what it does, how to use the vault, how to add inspiration, setup. |
| `inspo/vault/ITERATIONS.md` | **The full build history**, Iterations 0–19, kept as what was built, what broke and what replaced it, plus the live **Open threads**. Hand-written; rebuilds preserve it. |
| `tools/ingest/enrich_prompt.md` | The SOP the enrichment agent follows for every new site. If the data is wrong, the cause is usually here. |
| `tools/ingest/INSTALL.md` | Setting up the launchd daemon on a new machine. |
| `inspo/_queue/README.md` | The format for the in-repo queue that remote agents fill by pull request. |
| `docs/autonomous-growth.md` | Ideas only, nothing built: a corpus that finds its own inputs, and a public design search engine. Also lists the five invariants of v1. |
| `docs/superpowers/specs/2026-06-04-bookmark-auto-ingestion-design.md`, `docs/superpowers/plans/2026-06-04-bookmark-auto-ingestion.md` | The original June design and the 13-task build plan for the ingestion daemon. Historical. |
| `docs/superpowers/specs/2026-10-17-vault-views-design.md` | The design for purpose and design vaults built on a controlled vocabulary. **Superseded in part**: the owner chose embeddings over a curated taxonomy (see §5). Its view model and edge mechanics still apply. |
| `inspo/inspiration.md` | Generated readable digest of every bookmark. Don't edit. |
| `inspo/vault/*.md` | Generated Obsidian notes, one per site, plus `INDEX.md`. Don't edit, except `ITERATIONS.md`. |
| `inspo/bestdesignsonx.md` | A one-off dump of bestdesignsonx.com's curated feed from 2026-05-28. Reference material; not part of the pipeline. |
| `inspo/landing-page.md` | A short hand-kept list of references for the neoud.net landing page. |

## 3. How it works today

```
   producers                                   one socket
   ─────────                                   ──────────
   X bookmarks export ──► ~/Downloads/twitter-Bookmarks-*.json ─┐
   a list of URLs     ──► ~/Downloads/inspo-urls*.txt ──────────┤
   a remote agent     ──► PR adding inspo/_queue/<date>.txt ────┤   (e.g. Muse,
                                                                │    watching reels)
                    launchd daemon (run.sh): on a Downloads     │
                    change, and every 30 minutes                ▼
   sync ──► fetch origin, merge, drain the queue (urlcheck drops dead links first)
     ▼
   ingest (Python) ──► diff against the ledger, resolve real URLs, chunks of 5
     ▼
   enrich (claude -p, Sonnet, isolated headless Playwright)
          per site: ESSENCE first → prose → DOM probe → full-page screenshot
     ▼
   writers (Python) ──► inspo/inspiration.json   ◄── the single source of truth
     ▼                    ├─► inspiration.md      (generated)
   commit + push          ├─► inspo/vault/        (generated facet vault)
                          └─► inspo/cluster-<n>/  (generated cluster vaults, experiments)
```

**The invariants.** Every change has to respect these (from
`docs/autonomous-growth.md` and `CLAUDE.md`):

1. **Deterministic/judgment split.** Anything file-mutating is plain Python with
   tests. The model only does what a script can't.
2. **Anti-hallucination extraction.** Colours and fonts come from
   `getComputedStyle`, `document.fonts` and CSS variables, never from the screenshot.
3. **Chunked and resumable, ledger last.** A failure never advances the ledger.
4. **One source of truth.** Everything else is a view of `inspiration.json`.
   Delete any vault and the next run rebuilds it.
5. ~~A controlled facet vocabulary.~~ **Being replaced** by discovered clusters (§5).

**Models.** Sonnet does everything that reads or writes meaning: enrichment, the
essence, the backfill. Gemini (`gemini-embedding-001`, free tier) does only
embeddings. The key lives in the gitignored `.env`.

## 4. What has been done

The full story is in `ITERATIONS.md`. In outline:

| Phase | When | What |
|---|---|---|
| **Automated ingestion** | June | A launchd daemon watches `~/Downloads` for X exports. A deterministic Python ingest feeds headless `claude -p` enrichment, which feeds deterministic writers. Hardened against macOS (TCC, PATH, Node). Teardowns moved from eyeballed colour palettes to prose plus DOM-grounded data. Media gets viewed and described. Moved from Opus to Sonnet on cost. Notifications and a README followed in July. *Iterations 0–7, 11–12.* |
| **The vault as a graph** | July | Three vault formats: hub-and-spoke, then flat notes with free tags, then four **controlled facets** (`vertical`, `vibe`, `topic`, `mode`). The current `inspo/vault/` is the last of these (ITERATIONS calls it "Vault v3"). *Iterations 8–10.* |
| **Inputs beyond X** | Jul–Oct | Any list of URLs can feed the pipeline. Then an **in-repo queue**, so a remote agent with no access to this Mac can feed it by opening a PR. The daemon got git sync, a 30-minute poll and a dead-link prefilter. First real use: Muse watched 44 Instagram reels and queued 17 sites, and 16 were ingested. *Iterations 13–18.* |
| **Discovered structure** | Oct, current | The facets couldn't answer real searches. "Personal websites" didn't exist as a category, "books as a motif" had no field, and `minimal` was on 99 of 201 sites. So we embed each teardown, cluster the vectors, and render each clustering as numbered Obsidian vaults. Then we found the prose described the **page**, not the **thing**, and added the **essence**. *Iteration 19.* |

## 5. What we're trying to do now

**Make sites cluster by what they are, in two separate graphs.**

- **A purpose graph.** Sites cluster by what they're for: marketplaces together,
  personal sites together, company sites together. Fine-grained types (portfolio,
  blog, studio) form their own lobes, and related types sit near each other.
- **A design graph.** Sites cluster by how they look and feel. This is the graph
  the owner opens when starting a new design.
- **A build graph, later**, for how sites are made. The data for it is already
  collected.
- **Every node is a website.** No theme or tag nodes. Edges come from measured
  similarity, not shared tags.
- **One data source, several views.** Each vault is a renderer over
  `inspiration.json`.

**The open problem is meaning, not mechanics.** Embedding, clustering and rendering
all work. What decides quality is the text that represents each site. The first
purpose clustering grouped sites by how their pages were built: shared Next.js and
analytics vocabulary put a desktop-pet app next to a gifting toy, and fabra.com, a
3D fashion design tool, never surfaced as fashion. The fix is the **essence**:
`subject, host, does, for_whom, domain, kind`, written by the agent that has the
live site. `domain` and `kind` are separate fields because a single blended
embedding loses whichever one the prose says less about.

## 6. How we're doing it

**Spike, look, adjust, repeat.** The owner chose this over writing design docs
first.

1. Change one thing: the text recipe, the linkage, the cut depths, `k`.
2. Render a new **numbered version**: `inspo/cluster-<n>/purpose/` and `/design/`,
   each opened as its own Obsidian vault. Earlier versions are never overwritten,
   so two attempts can be compared side by side. These folders are gitignored; they
   rebuild in seconds.
3. Review it against ground truth. Read each cluster's members next to their
   `essence` and judge whether it hangs together.

The tools, all in `tools/ingest/`:

| Tool | Job |
|---|---|
| `embed.py` | Builds the text for each site in each space, embeds it with Gemini, and caches vectors by exact text so re-runs are nearly free. |
| `cluster.py` | Cosine similarity, a Ward dendrogram cut at any depth (so clusters nest inside clusters), symmetric nearest-neighbour edges, auto-generated names. |
| `render_clusters.py` | Writes one clustering as two Obsidian vaults with site-only nodes and its own graph config. |
| `essence.py` | The essence: one validator, a live re-scrape mode, a prose backfill mode. Each headless run gets its own empty directory, and site state (live, gone, sunset) protects captures of sites that later died. |

**Why these choices.** Ward over average linkage, because average put 183 of 201
sites in one cluster. Agglomerative clustering over UMAP and HDBSCAN, because at
201 sites dimensionality reduction buys nothing and both are stochastic, while this
pipeline rebuilds deterministically. The essence is written at scrape time rather
than inferred later, because the scrape is the only stage that has the source.

## 7. Where things stand

As of 2026-10-20:

- **320 items, 201 site teardowns, 189 screenshots, 161 tests.**
- **Every site has an essence.** 39 come from a live re-scrape of sites whose
  stored teardown described the wrong thing; 162 were backfilled from stored prose.
  Confidence: 155 high, 40 medium, 5 low. 3 sites have died or shut down since
  capture and keep their original prose. Spend so far is about $8.
- **`cluster-1` was reviewed.** It's the only version rendered, and it predates the
  essence. By reading, about four in five sites are placed sensibly. Portfolios,
  studios, newsletters, dev libraries, courses and personal hubs are near-perfect.
  The failures share one cause: companies, small indie apps and marketplaces
  cluster on their pitch, not their domain.
- **The essence is not yet what the purpose space clusters on.** That's the next
  step: `cluster-2`.

## 8. Next steps and pending decisions

1. **`cluster-2`.** Embed the essence for the purpose space, name clusters from
   their members' own `kind` and `domain` instead of word frequency, render it, and
   review it the same way as `cluster-1`.
2. **The owner's paused requests:**
   - a **directory cleanup** into versions. The naming has to avoid colliding with
     the existing "Vault v1/v2/v3" in `ITERATIONS.md`;
   - a **canonical list of sites** as the global source of truth for the corpus,
     easy to add to;
   - adding **workspaces.xyz** to the corpus.
3. **Promotion.** Nothing from the cluster experiments has replaced
   `inspo/vault/` yet, and the role of `taxonomy.json` facets after that is
   undecided.
4. **Everything else** is in `ITERATIONS.md` → *Open threads*: free-text `domain`
   values, unmarked dead sites, five low-confidence essences, the dependency on two
   vendors, and whether daemon commits should stay on `main`.

**Before you change anything,** read `CLAUDE.md`. Log meaningful changes in
`ITERATIONS.md` in the same piece of work, never hand-edit generated files, run
`.venv/bin/python -m pytest -q` before committing, and push.
