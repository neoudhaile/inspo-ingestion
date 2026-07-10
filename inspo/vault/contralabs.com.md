---
url: https://contralabs.com/
domain: contralabs.com
title: "Contra Labs — a frontier human data & evaluation lab for creative AI"
category: design
extracted_at: 2026-07-05
tags:
  - category/design
  - aesthetic/editorial
  - pattern/renaissance-art
  - pattern/dithered-halftone
  - pattern/editorial
  - pattern/serif-display
  - pattern/framer
  - pattern/scroll-reveal
  - pattern/logo-wall
  - pattern/ai-brand
  - tech/framer
  - tech/segment
  - tech/unpkg-css
  - tech/framerusercontent-cdn
  - color/warm
  - color/cool
  - font/source-serif-4
  - font/source-serif-4-variable-200-900
  - font/gt-standard-l-regular
  - font/gt-standard-l-medium
  - font/gt-standard-l-semibold
---
# Contra Labs — a frontier human data & evaluation lab for creative AI
> A frontier human data and evaluation lab making AI better for creativity.  ·  [contralabs.com](https://contralabs.com/)

![contralabs.com](../../screenshots/contralabscom.png)

## What it is
Contra Labs (from Contra, the professional network for independent creatives) is a 'frontier human data and evaluation lab' for creative AI — fronting 1.5M+ verified creative experts who benchmark style, tone and taste for AI models and applications. It's the site the bookmarked tweet singles out for its renaissance-oil-painting-meets-dithered-ASCII visual identity.

## What it shows
A long (~13,900px) single-page site. The hero headline 'A frontier human data and evaluation lab making AI better for creativity.' sits with Request-partnership / Research CTAs above a scrolling logo wall of the AI and no-code tools it works with (Framer, Lovable, HeyGen, Ideogram, Glide, Kajabi, Jitter, Kittl and dozens more). Below come sections 'Meet the ContraLabs ecosystem', 'Leading next-gen creative AI research.', 'Trusted by frontier labs and applications.', and a closing manifesto pairing 'Execution is free.' with 'Now, judgment is everything.'

## How it works
Built on Framer — assets served from framerusercontent.com with events.framer.com telemetry and Segment (cdn.segment.com) analytics, plus one unpkg-hosted stylesheet. It is media-dense (6 canvas, 4 video, 19 img, 9 svg) which drives the animated Renaissance imagery and the ordered-dither/halftone panels. No Next/Nuxt/React-root signature was exposed (Framer's own runtime).

## How it's designed
An editorial, gallery-grade aesthetic. From the DOM probe the canvas is a warm off-white (body background rgb(251,250,246) ≈ #FBFAF6) with near-black ink (h1 color rgb(43,43,41)). The display type is Source Serif 4 Variable (the h1 renders at 50px/400 in 'Source Serif 4 Variable', serif) paired with the GT Standard L grotesque (Regular 400 / Medium 500 / Semibold 600 all report loaded) for UI and body; Inter is declared in the stylesheet but reports unloaded. The signature move is compositing classical oil-painting portraits with black-and-white dithered/halftone rectangles that stand in for the laptop and tablet screens the figures hold.

## Design data
- **Palette:** Warm off-white canvas #FBFAF6 with near-black ink (rgb(43,43,41)); the color energy comes from the Renaissance oil imagery (golds, deep reds, teal).
- **Palette tokens:** body background: rgb(251, 250, 246) (rendered), h1 color: rgb(43, 43, 41) (rendered), html color: rgb(0, 0, 0) (rendered)
- **Fonts:** Source Serif 4 Variable for the serif display headings; GT Standard L (Regular/Medium/Semibold) grotesque for UI and body; Inter declared but unloaded.
- **Fonts loaded:** Source Serif 4 400, Source Serif 4 Variable 200-900, GT Standard L Regular 400, GT Standard L Medium 500, GT Standard L Semibold 600
- **Tech stack:** Framer, Segment, unpkg (CSS), framerusercontent CDN
- **Media mix:** img 19 · canvas 6 · video 4 · svg 9 · iframe 1
- **Page height:** 13877px (single-screen: False)
- **Responsive:** At 390x844 the layout reflows to a single column (height stays ~13,640px) and the hero h1 scales from 50px to 36px; no separate hamburger element was detected (Framer breakpoint variant).
- **Headings:** A frontier human data and evaluation lab making AI better for creativity. / Meet the ContraLabs ecosystem / Leading next-gen creative AI research. / Trusted by frontier labs and applications. / Execution is free. / Now, judgment is everything.
- **Extracted:** 2026-07-05 · Playwright MCP, 1440x900 + 390x844 mobile pass, logged_out: true

## Related sites
[[asekachov.com]] [[eko.lumaris.works]] [[joonasvirtanen.com]] [[sinceerly.com]] [[12matcha.com]] [[21st.dev]]

## Tags
#category/design #aesthetic/editorial #pattern/renaissance-art #pattern/dithered-halftone #pattern/editorial #pattern/serif-display #pattern/framer #pattern/scroll-reveal #pattern/logo-wall #pattern/ai-brand #tech/framer #tech/segment #tech/unpkg-css #tech/framerusercontent-cdn #color/warm #color/cool #font/source-serif-4 #font/source-serif-4-variable-200-900 #font/gt-standard-l-regular #font/gt-standard-l-medium #font/gt-standard-l-semibold
