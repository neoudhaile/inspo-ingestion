---
url: https://lelezhang.design/draw
title: "draw — let's draw together (send your sketch to Claude)"
category: uncategorized
aesthetics: [playful]
tags: [drawing-tool, ai-collab, claude-api, glassmorphism, paper, slate-blue, handwriting-font, playful, design-system]
extracted_at: 2026-07-05
---
# draw — let's draw together (send your sketch to Claude)
> Interactive drawing experiments and demos.  ·  [lelezhang.design](https://lelezhang.design/draw)

![lelezhang.design](../../../screenshots/lelezhangdesign-draw.png)

**What it is** — 'draw' — an interactive drawing playground on designer Lele Zhang's personal site where you sketch on screen and 'Send to Claude' to collaborate with AI. It's the 'finger paint on screen' from Jonas's list (surfaced via a quote of @itsjessyin, resolved to lelezhang.design/draw).

**What it shows** — A calm, paper-like drawing board with a floating glass toolbar: you sketch freehand and hit 'Send to Claude' to have the model riff on your drawing ('Let's draw together?'). Guest Claude credits were provided — now '$0.00 remaining' — with a bring-your-own-API-key option.

**How it works** — A self-hosted static build (no client-framework global exposed) with an SVG/DOM drawing surface (0 canvas, 13 svg icons, 8 img) and an extensive '--draw-*' CSS custom-property design system (glassmorphic panels, ink/surface tokens). Type is served via Adobe Typekit + Google Fonts, and it calls the Anthropic/Claude API to interpret drawings. Single-screen (900px).

**How it's designed** — Soft, papery, glassmorphic. From :root tokens the page is warm off-white (--draw-bg-page #efeeec, surface rgb 250,249,247) with slate-blue ink (body rgb(47,53,87) = --slate #2f3557), a single blue accent (--draw-blue #0069d3) and translucent frosted panels (--glass-bg #c6c7d24d). Type pairs untitledSans (a clean grotesque for UI) with Caveat (a handwriting script) — the handwriting carrying the friendly 'let's draw' voice.

**Palette** — Warm off-white paper (#efeeec / rgb 250,249,247) with slate-blue ink (#2f3557), a single blue accent (#0069d3) and frosted-glass panels (#c6c7d24d).
**Fonts** — untitledSans (UI grotesque) with Caveat (handwriting script) for the playful voice.

## Connections
**Aesthetics:** [[aesthetics/playful|playful]]
**Patterns:** `drawing-tool` `ai-collab` `claude-api` `glassmorphism` `paper` `slate-blue` `handwriting-font` [[patterns/playful|playful]] [[patterns/design-system|design-system]]
**Category:** [[categories/uncategorized|uncategorized]]
**Tech:** `Static site (no framework global)` [[tech/adobe-typekit|Adobe Typekit]] [[tech/google-fonts|Google Fonts]] `Anthropic Claude API`
**Colors:** [[colors/warm|warm]] [[colors/cool|cool]]
**Fonts:** `untitledSans` [[fonts/caveat|Caveat]]

## Related sites
[[sites/cafe.endofday.studio|cafe.endofday.studio]] [[sites/chusmargallo.space|chusmargallo.space]] [[sites/heyneuma.com|heyneuma.com]] [[sites/humanoid-index.com|humanoid-index.com]] [[sites/jessa.art|jessa.art]]
