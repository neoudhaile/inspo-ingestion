---
url: https://www.typo.love/
domain: typo.love
title: "typo.love — a digital library of lost love letters"
vertical: directory-gallery
mode: light
vibe: [organic-warm, retro]
topics: [writing]
extracted_at: 2026-07-05
tags:
  - vertical/directory-gallery
  - vibe/organic-warm
  - vibe/retro
  - topic/writing
  - mode/light
---
# typo.love — a digital library of lost love letters
> For all the words left unsaid.  ·  [typo.love](https://www.typo.love/)

![typo.love](../../screenshots/typolove.png)

**Vertical:** #vertical/directory-gallery  ·  **Vibe:** #vibe/organic-warm #vibe/retro  ·  **Topics:** #topic/writing  ·  **Mode:** #mode/light

## What it is
typo.love — 'a digital library of love letters … for all the words left unsaid,' a project by @lychkel. It's the 'library of love letters' from Jonas's list.

## What it shows
An infinite, pannable and zoomable canvas ('SPACE + DRAG TO PAN · SCROLL TO ZOOM') scattered with dozens of pastel, wax-sealed envelopes and a polaroid ('the stars and the moon'); each opens a stranger's submitted love letter. A lofi track (Lost Library — OMORI OST) plays and submissions are currently closed.

## How it works
Next.js (App Router — next/font fallbacks and App-Router opengraph-image/icon conventions), self-hosted with no third-party analytics scripts. The board is a single <canvas> (1 canvas) carrying 23 envelope images; it's a fixed, full-viewport experience (scrollHeight 0).

## How it's designed
A tender, analog-stationery aesthetic. From getComputedStyle the html/body backgrounds render transparent (rgba(0,0,0,0)) so the off-white paper canvas shows through, with near-black ink (body rgb(26,26,26)) and muted-grey UI (rgb(153,153,153)). The wordmark 'typo.love' is set 48px/400 in a vintage newspaper serif, OldNewspaper; UI labels ([INFO], [SUBMISSIONS CLOSED], the player) use Fragment Mono; and the letter body copy is Libre Baskerville (Instrument Serif is also declared).

## Design data
- **Palette:** An off-white paper canvas with near-black ink (rgb(26,26,26)) and muted-grey UI (rgb(153,153,153)); the envelope pastels (blush, sage, powder-blue, cream) supply the colour.
- **Palette tokens:** body color: rgb(26, 26, 26) (rendered), label/button color: rgb(153, 153, 153) (rendered), body background: rgba(0, 0, 0, 0) (rendered)
- **Fonts:** OldNewspaper (vintage serif wordmark), Fragment Mono (UI/labels) and Libre Baskerville (letters); Instrument Serif declared but unloaded.
- **Fonts loaded:** OldNewspaper 400, Fragment Mono 400, Libre Baskerville 400
- **Tech stack:** Next.js (App Router, next/font), self-hosted
- **Keywords:** infinite-canvas, pan-zoom, stationery, love-letters, serif, mono-ui, nextjs, lofi, interactive-art
- **Media mix:** img 23 · canvas 1 · svg 1
- **Page height:** 900px (single-screen: True)
- **Responsive:** At 390x844 it stays a full-viewport pannable canvas (scrollHeight 0) with the same [INFO]/[SUBMISSIONS CLOSED] chrome; touch pan/pinch-zoom simply replaces mouse drag — no hamburger.
- **Headings:** typo.love
- **Extracted:** 2026-07-05 · Playwright MCP, 1440x900 + 390x844 mobile pass, logged_out: true

## Related sites
- [[coolsites.ai]] — shared: directory-gallery, organic-warm, light
- [[the-cafelist.com]] — shared: directory-gallery, organic-warm, light
- [[kiira.in]] — shared: organic-warm, retro, light
- [[millermanintelligence.com]] — shared: organic-warm, writing, light
- [[noahzender.com]] — shared: organic-warm, writing, light
- [[sinceerly.com]] — shared: organic-warm, writing, light
