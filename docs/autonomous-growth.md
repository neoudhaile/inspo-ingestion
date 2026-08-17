# Autonomous growth + the public design search engine

**Status: idea dump. Nothing here is decided or built.** Written 2026-08-17 as a
thinking document, not a plan. The one thing it is trying to preserve is the
distinction between *what we have* (Part 1) and *what we're imagining* (Parts 2–3),
so the current design stays referenceable while the ambition moves.

---

## 0. The bottleneck we're actually trying to escape

The system is fully automated **downstream** of a manual act. Everything from
"a JSON export lands in ~/Downloads" onward runs unattended and well. But the
corpus can only ever contain sites that:

1. crossed my X timeline,
2. I remembered to bookmark,
3. and I remembered to export.

So the corpus is a **sample of my attention**, not a sample of good web design.
Concretely, that shows up as bias in the vault today: 168 sites, but 84 tagged
`#vibe/minimal` and only 3 `#vibe/brutalist`; `#topic/design` (55) / `#topic/ai` (44)
/ `#topic/engineering` (41) dwarf `#topic/fashion` (1) and `#topic/photography` (1).
That isn't the shape of the web — it's the shape of my feed. A DJ-site lookup last
week returned strong references but had to reach into tool-apps and WebGL toys
because there is essentially no music/nightlife cluster to draw on.

Two separate ambitions fall out of this, and they're worth keeping separate because
they have different difficulty and different failure modes:

- **Ambition A — autonomous growth:** the corpus finds its own inputs. (Mostly an
  engineering + cost + quality-gate problem.)
- **Ambition B — the public thing:** a website anyone can search for cool sites by
  design characteristic. Open source. (Mostly a product + hosting + legal +
  community problem.)

A is a prerequisite for B being interesting. B is what makes A worth paying for.

---

## Part 1 — The original design, for the record

This is the baseline to measure any change against. Fuller versions live in
[`../README.md`](../README.md) (architecture diagram + how to use),
[`../inspo/vault/ITERATIONS.md`](../inspo/vault/ITERATIONS.md) (Iterations 0–13 —
every dead end and why it was replaced), and
[`superpowers/specs/2026-06-04-bookmark-auto-ingestion-design.md`](superpowers/specs/2026-06-04-bookmark-auto-ingestion-design.md)
(the original spec). Summarized here so this document stands alone:

### The pipeline (v1, as it exists today)

```
manual act:  bookmark on X  →  twitter-web-exporter  →  ~/Downloads/*.json
                                                              │
                          launchd WatchPaths → run.sh ────────┘
                                     │
   deterministic Python  ──  diff export vs _ledger.json by tweet id
   (tools/ingest)             → harvest real URLs (t.co → destination)
                              → new-items.json, chunks of 5
                                     │
   claude -p (Sonnet,      ──  per bookmark: title/category/tags, primary-URL
   headless, isolated          judgment, view+describe attached media
   Playwright MCP)         ──  per design-worthy site: fullPage screenshot,
                               DOM probe (CSS vars, document.fonts, computed
                               colors, meta, framework globals), mobile pass,
                               prose teardown, facet classification
                                     │
   deterministic writers   ──  merge → inspo/inspiration.json (source of truth)
                              → regenerate inspiration.md + inspo/vault/
                              → advance ledger → archive raw export
```

### The five invariants that made it work

These are the load-bearing decisions. **Any autonomous or public version must keep
all five**, or it stops being this system.

1. **Deterministic / judgment split.** Anything idempotent and file-mutating is
   plain Python with tests. The model only does what a script can't: pick the
   subject site, write prose, classify facets, describe a video.
2. **Anti-hallucination extraction.** Palette and fonts come from
   `getComputedStyle` / `document.fonts` / CSS custom properties — *never* from
   looking at the screenshot. This is why the data is liftable straight into CSS.
   (Iteration 4 exists because we got this wrong first.)
3. **Chunked + resumable, ledger last.** 5 bookmarks per `claude -p` call; the
   ledger advances per chunk; a failure never advances it. Rate-limit stops resume
   exactly where they left off.
4. **One source of truth, everything else generated.** `inspo/inspiration.json`.
   `inspiration.md` and the whole vault are views and are safe to delete.
   (`ITERATIONS.md` is the one hand-written exception, preserved across rebuilds.)
5. **Controlled facet vocabulary.** Four facets — `vertical` / `vibe` / `topic` /
   `mode` — fixed in `tools/ingest/taxonomy.json`, extended sparingly. Vault v2
   used free tags and the graph turned to mush (Iteration 9→10). Granular detail
   (`bento`, `webgl`) lives as searchable *text inside* notes, not as tags.

### What v1 already got right that helps here

- **The seam is a normalized item list, not a tweet.** Iteration 13's universal URL
  adapter (`tools/ingest/add_urls.py` + the `~/Downloads/inspo-urls.txt` drop-file)
  means *anything that emits URLs can feed the pipeline.* Autonomous discovery does
  not require touching the ingest core at all — it's a new producer in front of an
  existing socket. This is the single biggest reason Ambition A is tractable.
- **Dedup is by URL hash + by domain against existing teardowns**, so a firehose of
  repeat suggestions is harmless.
- **The teardown output is already machine-queryable** (`palette_tokens`,
  `fonts_loaded`, `pattern_keywords`, `tech_stack`, `media_mix`, `page_height_px`).
  That's a search index in waiting.

---

## Part 2 — Ambition A: make the corpus grow itself

### 2.1 Where new sites could come from

Roughly in order of signal-to-noise (best first). All of these reduce to "emit URLs
into the existing adapter", which is the point.

| Source | Why it's good | Watch out for |
|---|---|---|
| **Award galleries** — Awwwards, CSSDA, Godly, Httpster, Land-book, One Page Love, SiteInspire, Minimal.gallery, Typewolf | Pre-curated by humans for *design*; exactly our subject matter; stable HTML lists | ToS / scraping etiquette; heavy overlap between them; award-bait bias (lots of WebGL agency sites, few personal blogs) |
| **The vault's own `links_out[]`** | Free, zero-network discovery — we already store where every torn-down site points. Designers link to designers. | Stays inside the existing bubble; needs a "distance from seed" cap |
| **Directory-gallery sites already in the corpus** (we have 16 `#vertical/directory-gallery`) | Same as above but denser | Same |
| **Show HN / r/web_design / Designer News / Bluesky+Mastodon design tags** | Fresh, non-award, weirder; catches personal sites | Very low precision; needs a hard quality gate |
| **X, but automated** — follow specific accounts that post site showcases rather than my own bookmarks | Same source as today, no manual step | API cost/access; this is the thing we're trying to stop depending on |
| **Webring / blogroll crawling** from personal sites | Best possible source for the *personal-site* cluster, which is our strongest vertical | Slow, sparse, lots of dead links |
| **Font/tech fingerprint crawling** — e.g. sites shipping a known display face, or built with Framer | Great for filling *specific* taxonomy gaps on demand | Feels adversarial; rate limits |

Idea worth keeping: **gap-driven discovery.** Don't crawl broadly — read
`INDEX.md`, find the thin facets (`#vibe/brutalist` = 3, `#topic/fashion` = 1,
music/nightlife ≈ 0), and go looking *specifically* for those. The taxonomy becomes
the crawl planner. This directly fixes the "no DJ references" failure and it keeps
volume low, which keeps cost low.

### 2.2 The hard part is not discovery, it's the quality gate

Discovery is easy and cheap. Teardowns are expensive (Playwright + Sonnet + a
fullPage PNG). And "is this site *actually good*" is the one judgment the whole
system's value rests on — and the one thing I currently do for free, implicitly, by
choosing to bookmark.

So the real design question: **what replaces my taste?**

Sketches, cheapest first — probably a cascade, not a single gate:

1. **Cheap mechanical prefilter (free, no model).** Reject on: dead/parked/404,
   login wall, obvious templates (default Wix/Squarespace/Linktree markup), no
   custom CSS variables *and* no webfont *and* no canvas, page is a single
   stock-hero + form. `curl` + grep gets most of this — the "design dig without a
   browser" recipe from the `design-inspiration` skill already does exactly these
   probes.
2. **Screenshot-only triage (cheap model call).** One viewport screenshot, one
   question: *is this visually distinctive enough to be worth a full teardown?*
   Note this deliberately breaks invariant #2's spirit — but only for *routing*, not
   for extracting facts. Worth being explicit that judging-from-pixels is allowed
   for triage and forbidden for data.
3. **Full teardown** only for survivors.
4. **Post-hoc pruning.** A periodic pass that demotes sites which, in hindsight,
   nothing ever links to and no query ever surfaces. The corpus should be able to
   shrink.

Open question I don't have an answer to: **do I want a "curated" tier and a
"crawled" tier as distinct things?** A `provenance: manual | discovered` field with
the manual set treated as the taste anchor (and maybe as few-shot examples for the
triage gate) feels right, and it means the thing I built for myself doesn't get
diluted by the thing built for everyone.

### 2.3 Budget, cadence, safety

- **A hard spend ceiling per day, enforced in the runner, not in a prompt.** N
  teardowns/day max. The existing chunk-and-ledger design already gives natural
  stopping points.
- **Discovery and teardown as separate schedules.** Discovery is cheap and can run
  often into a *queue* (`inspo/_inbox/` already exists for mid-flight items).
  Teardown drains the queue at whatever rate the budget allows. Decoupling them
  means a rich discovery day doesn't spike cost.
- **Politeness by default:** robots.txt, real UA, no concurrency against one host,
  cache aggressively. If this ever goes public, this stops being etiquette and
  becomes a requirement.
- **Never let autonomy touch the invariants.** In particular: discovered items go
  through the *same* writers, the same tests, the same ledger discipline. No
  parallel path.
- **Screenshots are already 232 MB and growing** (existing open thread). Autonomous
  growth turns that from "eventually a problem" into "immediately the problem."
  Retention policy / compression / object storage has to be decided *before* volume,
  not after.

### 2.4 What would tell us it's working

Not "number of sites". Better: **does a real lookup get better?** The honest test is
the one from actual use — ask the corpus for "artistic references for a DJ site" and
see whether the answer is drawn from a genuine music/nightlife cluster instead of
improvised out of adjacent verticals. Facet balance in `INDEX.md` is the cheap proxy.

---

## Part 3 — Ambition B: the public, open-source design search engine

The pitch, roughly: **search the web by design characteristic.** Not "cool sites,
by category" (that's every gallery that already exists, and they're all
human-curated, shallow, and unqueryable). The differentiator is that every entry is
a *structured, machine-extracted teardown* — so you can ask things galleries
fundamentally can't answer:

- dark portfolios that ship **no webfont**
- sites using a **serif display + monospace UI** pairing
- everything with a **mint accent on near-black**
- **single-screen, no-scroll** layouts (`is_single_screen`)
- built with **Framer** but that don't *look* like Framer
- sites whose measured palette is within ΔE of *this hex I'm holding*
- "more like this site" — the vault's Related-sites edge, but for the whole web

That last one is the real product, I think. **Reverse-image / reverse-vibe search for
web design.** Paste a URL or a screenshot, get the twenty closest-feeling sites with
their actual tokens.

### 3.1 What already transfers

More than expected. The private system is basically the crawler + extractor + schema
for the public one:

- `site_designs{}` is the record schema; its `_schema` key is already
  self-documenting.
- The facet taxonomy is the browse UI's navigation, ready-made.
- The teardown prose is the human-readable layer; the tokens are the filter layer.
- The `design-inspiration` skill is, in effect, the API's usage docs — and hints that
  **the agent-facing interface matters as much as the human one.** An MCP server
  over this corpus might be a bigger deal than the website. "Ground your build in
  real designs" is a thing every coding agent now wants and none can do well.

### 3.2 What's genuinely new work

- **Public search UX.** Faceted filter + a visual grid of screenshots is the obvious
  v1. The interesting version is color/type/vibe similarity search, which needs
  embeddings over (screenshot, tokens, prose) rather than tag filters.
- **Scale changes the architecture.** JSON-file-as-database and a launchd daemon on
  a Mac are correct for 168 sites and wrong for 100k. That's a real port (Postgres
  + object storage + a queue), and the honest question is whether to do it at all or
  keep the private thing private and *start* the public thing at the right scale.
- **Screenshot hosting and rights.** Thumbnails of other people's sites, at scale,
  publicly. Fair-use-ish and universally done by galleries, but it needs a takedown
  path and a `?no-index` respect policy before launch, not after.
- **Open source = contribution shape.** The most valuable contribution isn't code,
  it's *sites* and *taxonomy*. So: PR-a-URL? A submit form feeding the same drop-file
  adapter? Community facet curation? The taxonomy-drift open thread becomes ten
  times harder with strangers involved, and the Vault-v2 free-tag failure is the
  warning — **do not let a public version have open tags.**
- **Who pays for teardowns?** Every submitted URL costs a model call and a browser
  session. Someone has to eat that, or contributors bring their own key, or
  teardowns get batched/rate-limited hard.

### 3.3 Prior art to actually go look at

Awwwards / SiteInspire / Land-book / Godly / Httpster / Minimal.gallery / One Page
Love (curated galleries — pretty, unqueryable), Typewolf (type-led, closest in
spirit), Fonts In Use, BuiltWith + Wappalyzer (tech fingerprinting at scale, zero
aesthetics), HTTP Archive / Web Almanac (the model for *measured* web data at
enormous scale — worth studying hard, since it proves the crawl-and-measure part is
a solved problem), Are.na (in the corpus already; the community-curation model).

Nobody appears to combine **measured design data + aesthetic judgment + queryable
structure.** That's the gap.

---

## 4. Open questions I'd want to answer before building anything

1. **Two systems or one?** Does the private vault become the public corpus's seed
   set, or stay a separate personal thing that just shares code? (Leaning: separate
   data, shared extractor. My bookmarks are a taste signal I don't want averaged
   away.)
2. **Is the gate model-judged or human-judged?** A public site could crowdsource the
   quality signal (upvotes) and skip the hard AI-taste problem entirely — but then
   it needs users before it's good, which is the usual cold-start trap.
3. **Website first or MCP/API first?** The agent-facing version is less work, has a
   clearer user (anyone building UI with Claude), and doesn't need a design of its
   own. It may also be the better wedge.
4. **What's the smallest honest test of Ambition A?** Probably: gap-driven
   discovery against *one* thin facet, ~20 candidates through a cheap prefilter,
   whatever survives torn down by the existing pipeline, then judge whether the new
   cluster is actually useful in a real lookup. No new infrastructure, no schema
   change, one new script in front of `add_urls.py`.
5. **Does autonomy make the vault worse to use?** More sites ≠ better traversal. If
   Related-sites edges get noisier, the thing loses its main advantage over a
   gallery. Growth needs a quality metric, not just a count.

---

## 5. Explicitly out of scope for now

Not decided against — just not what this document is for: any schema change, any
change to `taxonomy.json`, any new daemon, any hosting choice, any framework pick
for a public site. Part 4 question 4 is the only thing here that's cheap enough to
try without a real decision first.
