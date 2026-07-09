---
url: https://www.typo.love/
title: "typo.love — a digital library of lost love letters"
category: uncategorized
aesthetics: [experimental]
tags: [infinite-canvas, pan-zoom, stationery, love-letters, serif, mono-ui, nextjs, lofi, interactive-art]
extracted_at: 2026-07-05
---
# typo.love — a digital library of lost love letters
> For all the words left unsaid.  ·  [typo.love](https://www.typo.love/)

![typo.love](../../../screenshots/typolove.png)

**What it is** — typo.love — 'a digital library of love letters … for all the words left unsaid,' a project by @lychkel. It's the 'library of love letters' from Jonas's list.

**What it shows** — An infinite, pannable and zoomable canvas ('SPACE + DRAG TO PAN · SCROLL TO ZOOM') scattered with dozens of pastel, wax-sealed envelopes and a polaroid ('the stars and the moon'); each opens a stranger's submitted love letter. A lofi track (Lost Library — OMORI OST) plays and submissions are currently closed.

**How it works** — Next.js (App Router — next/font fallbacks and App-Router opengraph-image/icon conventions), self-hosted with no third-party analytics scripts. The board is a single <canvas> (1 canvas) carrying 23 envelope images; it's a fixed, full-viewport experience (scrollHeight 0).

**How it's designed** — A tender, analog-stationery aesthetic. From getComputedStyle the html/body backgrounds render transparent (rgba(0,0,0,0)) so the off-white paper canvas shows through, with near-black ink (body rgb(26,26,26)) and muted-grey UI (rgb(153,153,153)). The wordmark 'typo.love' is set 48px/400 in a vintage newspaper serif, OldNewspaper; UI labels ([INFO], [SUBMISSIONS CLOSED], the player) use Fragment Mono; and the letter body copy is Libre Baskerville (Instrument Serif is also declared).

**Palette** — An off-white paper canvas with near-black ink (rgb(26,26,26)) and muted-grey UI (rgb(153,153,153)); the envelope pastels (blush, sage, powder-blue, cream) supply the colour.
**Fonts** — OldNewspaper (vintage serif wordmark), Fragment Mono (UI/labels) and Libre Baskerville (letters); Instrument Serif declared but unloaded.

## Connections
**Aesthetics:** [[aesthetics/experimental|experimental]]
**Patterns:** `infinite-canvas` `pan-zoom` `stationery` `love-letters` `serif` `mono-ui` [[patterns/nextjs|nextjs]] `lofi` `interactive-art`
**Category:** [[categories/uncategorized|uncategorized]]
**Tech:** `Next.js (App Router, next/font)` [[tech/self-hosted|self-hosted]]
**Colors:** [[colors/warm|warm]] [[colors/cool|cool]]
**Fonts:** `OldNewspaper` [[fonts/fragment-mono|Fragment Mono]] [[fonts/libre-baskerville|Libre Baskerville]]

## Related sites
[[sites/animations.dev|animations.dev]] [[sites/cafe.endofday.studio|cafe.endofday.studio]] [[sites/emilkowal.ski|emilkowal.ski]] [[sites/fey.com|fey.com]] [[sites/humanoid-index.com|humanoid-index.com]]
