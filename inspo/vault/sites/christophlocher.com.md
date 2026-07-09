---
url: https://christophlocher.com/
title: "Christoph Locher — Interaction Designer (a bold split-screen editorial portfolio)"
category: product
aesthetics: [portfolio, editorial, minimal, developer-product]
tags: [portfolio, interaction-designer, editorial, swiss, split-screen, chartreuse, monospace-accent, self-hosted, no-tracking, minimalist]
extracted_at: 2026-07-08
---
# Christoph Locher — Interaction Designer (a bold split-screen editorial portfolio)
> I am an Interaction Designer living and working in Hamburg, Europe. My goal is making complex problems manageable through accessible abstractions.  ·  [christophlocher.com](https://christophlocher.com/)

![christophlocher.com](../../../screenshots/christophlochercom.png)

**What it is** — The personal site of Christoph Locher, an interaction designer based in Hamburg — the destination this design-inspiration-app tweet's export metadata resolves to (his own hub). The rendered h1 reads 'Christoph Locher / Interaction Designer', and the site is where his work, notes and the file-system-based inspiration app shown in the video presumably live. It is deliberately un-instrumented: the footer literally reads '2026 — No tracking.'

**What it shows** — A split-screen editorial homepage: a slate blue-grey hero panel carrying the black 'CHRISTOPH LOCHER / Interaction Designer' wordmark, a chartreuse/lime intro block ('I am an Interaction Designer living and working in Hamburg…'), a black left rail with thin connector lines pointing to contact labels (mail@christophlocher.com, @ch_locher, See all Notes, Colophon), a dark 'Continue reading' bar (About / Notes & Thoughts / Bookshelf / Map of Inquiry), and a 'Recent Notes' table (Notes from Glenn Parsons' The Philosophy of Design; Travel Notes: Medellín / Grottole / Athens; The Bilingual Mind).

**How it works** — A fully self-hosted static site — every <script> and stylesheet is served from christophlocher.com itself, with no third-party host. No app-framework global is present (Next / Nuxt / Vue / Svelte / React all absent) and there is no analytics at all (the footer states 'No tracking'). It is media-light: 0 <img>, 4 inline <svg>, 0 canvas/video/iframe, over a compact 1,336px page.

**How it's designed** — Crisp Swiss/editorial layout with an unusually confident colour block. The palette is declared explicitly in :root — --yellow #e1fa4d (the chartreuse intro block), --blue-gray #415264 (the hero panel), --red #ff4c43 (accent), --black #000 and --white #fff, plus a full grayscale ramp (rgba(0,0,0,.03) → .9). getComputedStyle confirms body text is rgb(0,0,0) and the h1 renders at 63px/400 in near-black rgb(18,22,26). Type comes from two self-hosted, loaded faces (document.fonts): 'Untitled Sans' (--font-family-sans) for display and body, and 'iA Writer Duospace' (--font-family-mono) for the mono labels/metadata — a designerly grotesque-plus-monospace pairing carrying a nearly image-free page.

**Palette** — Slate blue-grey hero (#415264) beside a chartreuse/lime intro block (#e1fa4d) on black/white, with a warm red accent (#ff4c43) — high-contrast editorial.
**Fonts** — Untitled Sans (display & body) + iA Writer Duospace (mono labels) — both self-hosted and loaded; no icon font.

## Connections
**Aesthetics:** [[aesthetics/portfolio|portfolio]] [[aesthetics/editorial|editorial]] [[aesthetics/minimal|minimal]] [[aesthetics/developer-product|developer-product]]
**Patterns:** [[patterns/portfolio|portfolio]] `interaction-designer` [[patterns/editorial|editorial]] [[patterns/swiss|swiss]] `split-screen` `chartreuse` `monospace-accent` [[patterns/self-hosted|self-hosted]] `no-tracking` [[patterns/minimalist|minimalist]]
**Category:** [[categories/product|product]]
**Tech:** `Self-hosted static (no JS framework detected)` `No analytics / no tracking`
**Colors:** [[colors/warm|warm]] [[colors/cool|cool]]
**Fonts:** `Untitled Sans` `iA Writer Duospace`

## Related sites
[[sites/asekachov.com|asekachov.com]] [[sites/ravalabs.com|ravalabs.com]] [[sites/ryancarson.com|ryancarson.com]] [[sites/daviskeene.com|daviskeene.com]] [[sites/designengineer.tools|designengineer.tools]]
