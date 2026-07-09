---
url: https://interfaces.dev/
title: "Interfaces › Design Engineering Magazine"
category: tools-build
aesthetics: [editorial]
tags: [editorial, long-scroll, typographic, svg-illustration, design-engineering, magazine]
extracted_at: 2026-06-06
---
# Interfaces › Design Engineering Magazine
> Interfaces  ·  [interfaces.dev](https://interfaces.dev/)

![interfaces.dev](../../../screenshots/interfacesdev.png)

**What it is** — A design engineering magazine — its own meta describes it as 'a design engineering magazine about building great interfaces that covers topics such as animation, typography, layout and color.' It is the showcased subject of Jakub Krehel's tweet, where the animated app icon is the brand mark.

**What it shows** — A long editorial homepage that opens on the single-word wordmark 'Interfaces' and scrolls through pitch sections — 'What Makes an Interface Feel Great?', 'About Interfaces' and 'How It Works' — illustrated with inline SVG diagrams (62 svg elements) rather than photography.

**How it works** — A tall (~7,900px) single-page scroll. No client-side framework global is exposed (no Nuxt/Next/Vue/Svelte/React markers) and every script and stylesheet is served from interfaces.dev itself, pointing to a static/SSG build; the OG image is hosted on Vercel blob storage.

**How it's designed** — Near-white paper (body background rgb(252,252,252)) with near-black ink, set in Inter Variable (the only loaded sans, 100–900) for both the 60px/weight-500 h1 and the body. A deep stack of accent webfonts is wired up through CSS variables — Libre Baskerville, Berkeley Mono, Redaction, Heldane and Openrunde — though only Inter Variable, Libre Baskerville and Berkeley Mono had actually loaded on first paint. Buttons are white-on-ink pills (14px). Quiet, typographic, editorial.

**Palette** — Off-white paper (#fcfcfc) with near-black ink and white pill buttons
**Fonts** — Inter Variable (body + headings); Libre Baskerville and Berkeley Mono as loaded accent families

## Connections
**Aesthetics:** [[aesthetics/editorial|editorial]]
**Patterns:** [[patterns/editorial|editorial]] [[patterns/long-scroll|long-scroll]] [[patterns/typographic|typographic]] `svg-illustration` [[patterns/design-engineering|design-engineering]] `magazine`
**Category:** [[categories/tools-build|tools-build]]
**Tech:** `Static/SSG (no client framework global)` `Vercel (blob storage)`
**Colors:** [[colors/neutral|neutral]]
**Fonts:** [[fonts/inter-variable-100-900|Inter Variable 100-900]] [[fonts/libre-baskerville|Libre Baskerville]] `Berkeley Mono`

## Related sites
[[sites/asekachov.com|asekachov.com]] [[sites/designengineer.tools|designengineer.tools]] [[sites/mercuryos.com|mercuryos.com]] [[sites/offthewall.studio|offthewall.studio]] [[sites/shedsgns.me|shedsgns.me]]
