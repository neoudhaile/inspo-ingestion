# Design: one source, many vault views

**Date:** 2026-10-17
**Status:** proposed, awaiting approval
**Supersedes:** the single four-facet vault graph (Iteration 10, "Vault v3: controlled facets")

## Why

The vault is for finding design references during a real design task. Four concrete
searches failed, and they failed for the same reason:

| The search | What happened |
|---|---|
| "personal websites" | No such category. Split across `portfolio` (41) and `personal-blog` (12), so neither tag answers it and an agent has to read the whole vault. |
| "websites that use books as a motif" | No data at all. Yet `book` appears in the teardown prose of **68 of 201 sites** — it was written down, never structured. |
| "good light minimalist design" | `minimal` is carried by **93 of 186** classified sites. A filter matching half the corpus narrows nothing. There is no notion of *good* anywhere in the schema. |
| "visualise the clusters" | Only reachable through an agent, which defeats the point of having it in Obsidian. |

Two root causes:

1. **The rich description is prose, not structure.** `what_it_is`, `what_it_shows`,
   `how_it_works` and `how_its_designed` are present on all 201 sites and are good.
   Nothing extracts queryable axes out of them.
2. **`pattern_keywords` was meant to be that extraction and collapsed.** It is
   uncontrolled free text: **930 distinct keywords across 201 sites, 746 used by
   exactly one site, only 46 used by five or more.** `dark` / `dark-mode` /
   `dark-theme` are three keys; so are `minimal` / `minimalist`. The terms that do
   recur mostly duplicate the facets. A vocabulary whose mass is singletons cannot
   cluster.

And one structural cause: `render_vault.edge_score` computes relatedness from the
four facets only (`W_VERTICAL=3, W_VIBE=2, W_TOPIC=2, W_MODE=1`, `EDGE_MIN=5`,
`EDGE_TOP=6`). `tech_stack`, `fonts_loaded`, `palette_tokens`, `media_mix` and the
verbatim `headings` are collected on every site and used for none of it.

## Goals

- One search like "personal websites", "sites that use books as a motif" or "light
  minimal portfolios" resolves to a tag or a folder, not a full-vault read.
- Two graphs, each with one job: **purpose/idea** and **design/look-and-feel**.
- Clusters are fine-grained but *spatially related* — `portfolio` and `personal-blog`
  are separate lobes that sit next to each other.
- Every node in every graph is a website. No theme or tag nodes.
- One source of truth; views are regenerated, never edited, never diverged.
- A third "how it's built" view remains cheap to add later.

## Non-goals

- Not building an Obsidian plugin. Two vaults give the dimension switch natively.
- Not reverse-engineering Obsidian (REA or otherwise). Nothing here needs its internals.
- Not a standalone web viewer. Clicking a node must open the full note, which Obsidian
  already does.
- Not the build view. Designed for, not built now.
- Not changing how bookmarks arrive. Ingestion, the queue medium and the daemon are
  untouched.

## Anti-goals

Things that would make this a failure even if it shipped:

- **Eleven dense blobs.** If purpose is the only edge signal, every personal site is
  equidistant from every other and the graph says nothing. Sub-structure inside a
  cluster is the requirement, not a nice-to-have.
- **A second source of truth.** If any view holds a fact that `inspiration.json`
  doesn't, the system has forked.
- **A vocabulary that collapses again.** If the new axes end up mostly singletons,
  this has reproduced `pattern_keywords` with extra steps.
- **Re-tearing-down 201 sites.** A browser re-visit of the whole corpus is slow,
  expensive, and unnecessary — the prose needed for reclassification is already stored.
- **Breaking agent search.** `rg` over markdown must keep working.

## Decisions already made (by the owner)

Recorded as decided, not open:

- **Purpose/idea is the primary clustering.** Marketplaces together, personal sites
  together, company sites together.
- **Design is a separate vault**, and design means *how it looks and feels* — it is
  the vault consulted when starting a new design, to find sites "within the sphere
  I'm looking into". Not how it's built.
- **How-it's-built is a third vault, later.**
- **Fine-grained is wanted**, with related types near each other in space, rather than
  coarse types merged.
- **Nodes are site names only.** Design themes (`dark`, `light`, `minimal`) must stop
  being the things that connect sites.
- **One data source, many views.** No copying the data.
- **The graph's value is that it looks good.** Finding things is the agent's job via
  `rg`; the visual is for enjoyment. This is why no plugin and no bespoke viewer are
  justified.
- **`mode` and `topics` are kept, not dropped.** Nothing in the existing schema is
  deleted. `mode` feeds design-view similarity (it is the only place "light" lives,
  and "good light minimalist design" was one of the four motivating searches);
  `topics` stays a searchable tag and may bridge *within* the design view.
- **A quality/craft axis is deferred.** The absence of any notion of "good" is real
  and named in Why, but everything in the corpus is there because it was bookmarked,
  so taste is already pre-filtered. Revisit if the finished vaults still feel
  undiscriminating. Adding it later is one more text pass, not a re-teardown.

## The data model

### Purpose: two levels, family and type

Replaces `vertical`. Family creates the neighbourhood; type creates the lobe.

```
personal/     portfolio · blog · cv-resume · link-hub
company/      product-marketing · studio-agency · brand
collection/   directory-gallery · marketplace
build-with/   library-framework · tool-utility · course-learning
publish/      publication · newsletter
play/         toy-experiment · art-piece
```

Derived from reading all 201 `what_it_is` descriptions. Three changes carry the goals:

- `portfolio` + `personal-blog` sit under one **family**, which is what makes
  "personal websites" answerable, while staying separate **types**, which is what the
  owner asked for.
- `marketplace` exists. It did not before; Templatoria, Weird Folders,
  backgrounds.supply and the prompt libraries had nowhere to go.
- `tool-app` splits. GSAP (a library you build with) and Ditther (a thing you open)
  were the same tag and are not alike.

Exactly one `purpose` per site, written as `family/type`.

### Motif: what the site depicts

New axis, and the one that makes "books as a motif" possible. Controlled vocabulary,
0–3 values, omitted when a site has no strong motif. Seed values to be derived from
the corpus during implementation rather than invented here; `book`-adjacent imagery is
known to appear in ~68 sites' prose, which is the existence proof.

### Mood: a sharpened `vibe`

`vibe` survives but must stop having one value on half the corpus. `minimal` (93/186)
splits into distinguishable moods during the backfill. Target: no single mood value on
more than ~25% of sites.

### `mode` and `topics`: kept

Owner decision. Neither is deleted.

- `mode` (dark/light/mixed, 189/201 sites) becomes an input to **design-view
  similarity**. It stays a queryable field, because "light" is something the owner
  searches on directly.
- `topics` stays as searchable frontmatter and tags. It forms **no edges in the
  purpose view** — that view forbids cross-family links by design — but may bridge
  within the design view.

### Retire `pattern_keywords`, and `vertical` after migration

Non-destructive. **Builder's call:** "retire" means *stop forming graph edges and
stop being rendered as a primary axis*, **not** delete the keys from
`inspiration.json`. Both fields stay in the source through at least one full
release, so the change is reversible and no information is lost before the new axes
are proven. `vertical` is also what `classify_facets.py` and the backfill read *from*
when deriving `purpose`, so it must survive the migration that depends on it.

`pattern_keywords`' useful recurring terms migrate into `purpose`, `motif`, `mood` or
`tech_stack`; its 746 singletons simply stop being treated as an axis.

### Deferred: quality / craft

Not in this change. See Decisions.

### Unchanged

`what_it_is` / `what_it_shows` / `how_it_works` / `how_its_designed`,
`palette_tokens` (180/201 sites), `fonts_loaded` (163/201), `tech_stack`, `media_mix`,
`headings`, `screenshot`. The anti-hallucination rule is untouched: colours and fonts
come from the DOM, never from the screenshot. **New axes are classification, which is
judgment, and may be derived from prose — they must never assert measured facts.**

## The view model

```
teardown (one visit, one enrichment)
        │
        ▼
inspo/inspiration.json            ← the only place facts live
        │
        ├─► purpose view ─► inspo/vault/           edges: sibling-aware purpose proximity
        ├─► design view  ─► inspo/vault-design/    edges: mood + mode + palette + fonts + media_mix
        └─► build view   ─► inspo/vault-build/     (later; data already collected)
```

**Builder's call: the purpose view keeps the existing `inspo/vault/` path.** It is the
primary view, and keeping the path means the user-global `design-inspiration` skill,
`README.md`, `CLAUDE.md` and `sync_repo.py`'s comments keep working unchanged, and
`ITERATIONS.md` never moves. Only genuinely new trees get new paths.

`render_vault.py` becomes a renderer that takes a view definition. Each view decides
only **which facts become edges** and **which fields the note foregrounds**. No view
stores a fact the source lacks; deleting a vault and rebuilding must be a no-op.

Notes exist once per view on disk. They are generated artifacts under the existing
rule ("never hand-edit generated notes"), the same contract `inspiration.md` lives
under. The source is not duplicated.

**Builder's call: one canonical `ITERATIONS.md`, at `inspo/vault/ITERATIONS.md`.**
`CLAUDE.md`'s standing rule, the `inspo-iterations-log` skill and `README.md` all name
that exact path. The log is the system's only hand-written artifact and must not fork
into one per view. New views preserve `.obsidian/` only; they get no `ITERATIONS.md`.

**Builder's call: new vaults are committed, and each ships a `.obsidian/graph.json`.**
"It looks good" is a recorded owner decision, and in Obsidian that look comes from the
graph config — colour groups, node sizing, forces. `PRESERVE` only protects an
`.obsidian/` that already exists, so a fresh `vault-design/` would otherwise open with
defaults. A checked-in config per view makes the look a deliverable of this work
rather than something to set up by hand. Cost to accept: committed file count roughly
doubles, on every daemon run.

## Edge mechanics

**Obsidian's graph has no edge weights.** Proximity is topological: nodes sit close
when they share many links. "Separate but close" therefore has to be built out of edge
counts, not weights. This is the central implementation constraint.

Purpose view, per site:

- `k_type` links to nearest neighbours **within its own type** — makes a tight lobe.
- `k_sibling` links (fewer) to nearest sites in **sibling types under the same family**
  — pulls the lobes adjacent without merging them.
- No links across families — families separate on their own.

Design view, per site: nearest neighbours by look-and-feel similarity, computed from
mood overlap, `mode`, palette distance over `palette_tokens`, shared `fonts_loaded`
families, and `media_mix` as a proxy for how motion- and image-led a site is. Hard
numbers where they exist, adjectives only where they don't.

**Builder's call: `motif` forms no edges in either view.** It is frontmatter plus a
tag, and gets its own section in the purpose view's `INDEX.md`. Motifs cut across
families — books appear on a personal blog, a marketplace and an art toy — so making
them edges would reintroduce exactly the cross-family links the purpose view forbids,
and would re-create tag-shaped hubs in a graph whose nodes are meant to be sites. The
motivating search ("websites that use books as a motif") is answered by `rg` and by
Obsidian's tag pane, which is all it ever needed.

"Nearest" needs a similarity function per view. Both views print the why on each link,
as the current vault already does (`[[kmk0.com]] — shared: portfolio, playful, light`).

Tuning `k_type` and `k_sibling` is empirical — the current `EDGE_MIN=5, EDGE_TOP=6`
was also a guess. The builder should expect to look at the rendered graph and adjust.

## Backfill

201 sites need `purpose`, `motif` and sharpened `mood`. **This is a text
reclassification, not a re-teardown.** Every input needed is already in
`inspiration.json`: `what_it_is`, `what_it_shows`, `how_it_works`, `how_its_designed`,
`headings`, plus existing facets. No Playwright, no site visits, no screenshots.

`classify_facets.py` is the precedent and the natural home. 12 of 201 sites currently
have no facets at all and get classified for the first time.

The enricher (`enrich_prompt.md`) must produce the new axes for new sites going
forward, so the backfill is one-time.

**Builder's call: the vocabulary is gated before the expensive pass, and
reclassification is possible.** The derived vocabularies are assigned by a model, so
a first pass landing at 40% on one mood value or 500 singleton motifs is a realistic
outcome — and the targets above ("no mood value on more than ~25% of sites", "motif
must not be mostly singletons") are worth nothing without a way to check and retry.
So:

1. Derive candidate vocabularies from a sample, print a **distribution report**, and
   stop for owner sign-off before classifying all 201.
2. Add a `facets_version` field per site. `classify_facets.py` today skips anything
   that already has `facets`, which makes a second pass against a revised vocabulary
   impossible; version-aware skipping plus a `--force` path fixes that.
3. Expect to run it more than once. Budget for it; it is text-only, so each pass is
   cheap relative to a teardown.

## Constraints

- `inspo/inspiration.json` stays the single source of truth.
- Agents keep using `rg` over markdown. They choose a tree based on the question.
- The daemon runs unattended: chunked, resumable, failure never advances the ledger.
- Deterministic stages stay plain Python with tests; the model only does judgment.
- Changes get an `ITERATIONS.md` entry in the same piece of work.
- `.venv/bin/python -m pytest -q` passes before committing.

## Consumers that must be updated in the same change

Because `vertical` stops being the primary axis, these stop being accurate the moment
the purpose view ships. The anti-goal "breaking agent search" makes updating them part
of the work, not a follow-up:

- `README.md` — documents `rg -l '#vertical/portfolio'` and the four-facet model.
- **`~/.claude/skills/design-inspiration/SKILL.md`** — a *user-global* skill, outside
  this repo. It hardcodes `inspo/vault/`, `#vertical/…`, `#mode/dark` and
  `vault/INDEX.md`. The vault path is preserved deliberately so only the facet
  vocabulary needs rewriting there. Editing it touches a file outside the repo, which
  the plan should call out explicitly since it cannot be reviewed in the same diff.
- `tools/ingest/enrich_prompt.md` — the SOP that classifies new sites.
- `tools/ingest/taxonomy.json` — the controlled vocabulary itself.

## Left to the builder

- The seed vocabularies for `motif` and the sharpened `mood`, derived from the corpus.
- The similarity function per view, and `k_type` / `k_sibling` values.
- Note layout per view — which fields each view foregrounds.
- How `INDEX.md` differs per view.
- Migration order, so no daemon run ever leaves a vault half-rendered.
- Whether `render_vault.py` grows a view parameter or splits into a shared renderer
  plus per-view definitions.
