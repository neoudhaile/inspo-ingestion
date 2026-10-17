---
url: https://shadergradient.co/
domain: shadergradient.co
title: "Shader Gradient"
vertical: tool-app
mode: dark
vibe: [experimental, playful]
topics: [design, art]
extracted_at: 2026-10-17
tags:
  - vertical/tool-app
  - vibe/experimental
  - vibe/playful
  - topic/design
  - topic/art
  - mode/dark
---
# Shader Gradient
> Create beautiful moving gradients on Framer, Figma and React  ·  [shadergradient.co](https://shadergradient.co/)

![shadergradient.co](../../screenshots/shadergradientco.png)

**Vertical:** #vertical/tool-app  ·  **Vibe:** #vibe/experimental #vibe/playful  ·  **Topics:** #topic/design #topic/art  ·  **Mode:** #mode/dark

## What it is
Landing page for Shader Gradient, a library of animated WebGL gradients for Framer, Figma and React, built by ruucm.

## What it shows
A live gradient demo up top, then a stack of use cases (Make live websites on Framer, Randomize, Ruucm, Seungmee, Twitter, Instagram, Halo) and a 'Try on web' call to action.

## How it works
The page is a Framer site (assets on framerusercontent.com, Framer events script) with 8 canvas elements running the gradients, plus one iframe. Letters in every heading are split into separate elements for per-character animation, so the h1/h2 text reads as 'S h a d e r G r a d i e n t' in the DOM.

## How it's designed
Near-black ground (body rgb(15,15,15)) with white text. Type mixes Anton (condensed display), Lora (serif), JetBrains Mono and Roboto Mono, with Inter as body. The colour comes from the gradients themselves rather than from UI chrome.

## Design data
- **Palette:** Near-black ground, white text, colour supplied by live gradient canvases
- **Palette tokens:** body bg: rgb(15, 15, 15) (rendered), h1 color: rgb(255, 255, 255) (rendered)
- **Fonts:** Anton, Lora, JetBrains Mono, Roboto Mono, Inter
- **Fonts loaded:** Anton 400, Lora 400, Lora 600, JetBrains Mono 400, Roboto Mono 400, Inter 300, Inter 400, Inter 500, Inter 600
- **Tech stack:** Framer, WebGL canvas, Framer Events
- **Keywords:** shader gradient, split-letter headings, framer site, webgl canvas, product demo
- **Media mix:** img 7 · canvas 8 · svg 9 · iframe 1
- **Page height:** 15880px (single-screen: False)
- **Responsive:** At 390px the page height barely changes (15880px to 15440px) and nothing overflows; the 8 canvases stay mounted.
- **Headings:** Shader Gradient / Make live websites / on Framer / Randomize / Ruucm / Seungmee / Twitter / Instagram / Halo / Try on web →
- **Extracted:** 2026-10-17 · Playwright 1440x900 full-page + DOM probe; 390x844 text probe; logged_out: true

## Related sites
- [[backgrounds.supply]] — shared: experimental, design, art, dark
- [[clipart.studio]] — shared: tool-app, playful, art
- [[drawably.dev]] — shared: tool-app, playful, design
- [[lelezhang.design]] — shared: tool-app, playful, art
- [[spacetypegenerator.com]] — shared: tool-app, experimental, design
- [[www.unicorn.studio]] — shared: experimental, design, art, dark
