---
url: https://patterncraft.fun/
domain: patterncraft.fun
title: "Pattern Craft - Modern Background Patterns & Gradients Snippets"
vertical: tool-app
mode: light
vibe: [minimal, corporate-clean]
topics: [design, engineering]
extracted_at: 2026-06-05
tags:
  - vertical/tool-app
  - vibe/minimal
  - vibe/corporate-clean
  - topic/design
  - topic/engineering
  - mode/light
---
# Pattern Craft - Modern Background Patterns & Gradients Snippets
> Create stunning websites with our curated collection of 100+ modern CSS background patterns and gradients.  ·  [patterncraft.fun](https://patterncraft.fun/)

![patterncraft.fun](../../screenshots/patterncraftfun.png)

**Vertical:** #vertical/tool-app  ·  **Vibe:** #vibe/minimal #vibe/corporate-clean  ·  **Topics:** #topic/design #topic/engineering  ·  **Mode:** #mode/light

## What it is
Pattern Craft, an open-source library of 100+ copy-paste CSS background patterns and gradients by Megh Bari (github.com/megh-bari/pattern-craft; featured in Vercel's OSS program). The hero reads 'Craft Beautiful / Patterns Backgrounds'. One of Devster's inspo-dump links.

## What it shows
A hero pitch ('Professional-grade background patterns and gradients. Easily copy the code…') over a very long 'Pattern Library' — a tiled gallery of background swatches in both light and dark variants (dot grids, mesh gradients, ruled grids, glows) where each tile is a live CSS preview you can one-click copy as CSS/Tailwind. A 'Buy Me Coffee / PayPal / UPI' support block and a Carbon ad sit alongside.

## How it works
A long single page (~20,878px) where each pattern is rendered as live SVG/CSS rather than an image — 1,518 inline <svg> tiles drive the gallery — with one-click copy and live preview. Built on the shadcn/ui token system with GeistSans, monetized via Carbon Ads (cdn.carbonads.com) and donations; no JS framework global is exposed (a static/Next build).

## How it's designed
Clean light docs-style UI in a slate palette: white ground (--background #fff) with a near-black slate foreground (--foreground #020618) and a slate primary (--primary #0f172b), so the colourful pattern swatches themselves provide all the visual energy against a quiet chrome. Type is GeistSans throughout; a shadcn chart palette (#f05100, #009588, #fcbb00…) is defined in tokens.

## Design data
- **Palette:** White ground (--background #fff) with near-black slate text (--foreground #020618) and a slate primary (--primary #0f172b); the colour comes entirely from the gallery of pattern swatches.
- **Palette tokens:** --background: #fff (var), --foreground: #020618 (var), --primary: #0f172b (var), --muted-foreground: #62748e (var)
- **Fonts:** GeistSans (variable) is the single loaded webfont, used across the whole UI.
- **Fonts loaded:** GeistSans (variable 100-900)
- **Tech stack:** shadcn/ui tokens, GeistSans, Carbon Ads, Vercel
- **Keywords:** copy-paste, css-patterns, gradients, gallery, open-source, developer-tool, shadcn, light-mode
- **Media mix:** img 4 · svg 1518
- **Page height:** 20878px (single-screen: False)
- **Responsive:** At 390x844 the gallery collapses to a single column and the hero drops from 60px to 30px, so the page balloons to a ~90,309px scroll; the header has no burger.
- **Headings:** Craft Beautiful / Patterns Backgrounds / Pattern Library
- **Links out:** [GitHub (megh-bari/pattern-craft)](https://github.com/megh-bari/pattern-craft) · [Vercel OSS Program feature](https://vercel.com/blog/vercel-open-source-program-fall-2025-cohort#pattern-craft)
- **Extracted:** 2026-06-05 · playwright-mcp @ 1440x900 (fullPage) + mobile 390x844, logged_out: true

## Related sites
- [[itshover.com]] — shared: tool-app, minimal, design, engineering, light
- [[sensory-ui.com]] — shared: tool-app, minimal, design, engineering, light
- [[akira.sachi.dev]] — shared: tool-app, minimal, engineering, light
- [[serif.sh]] — shared: tool-app, minimal, design, light
- [[21st.dev]] — shared: minimal, design, engineering, light
- [[animations.dev]] — shared: minimal, design, engineering, light
