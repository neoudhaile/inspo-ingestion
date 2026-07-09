---
url: https://designtools.fyi/
title: "designtools.fyi — 'Explore and compare every design tool', a role-ranked design-tool comparison directory"
category: tools-build
aesthetics: [editorial, playful]
tags: [directory, comparison, role-ranked, editorial, pixel-type, typewriter, halftone, dither, white, geist]
extracted_at: 2026-07-08
---
# designtools.fyi — 'Explore and compare every design tool', a role-ranked design-tool comparison directory
> Find the right tool for your role, ranked by what actually matters.  ·  [designtools.fyi](https://designtools.fyi/)

![designtools.fyi](../../../screenshots/designtoolsfyi.png)

**What it is** — A curated, opinionated comparison directory whose h1 is 'Explore and compare every design tool' and whose meta description reads 'Compare design tools across different capabilities. Find the best tools for designers, design engineers, and non-designers.' It positions itself as a place to 'Browse all 85 tools', read editorial 'dispatches', and find the right tool for your role rather than a flat link dump.

**What it shows** — A bright, playful hero (typewriter/pixel display type over a dithered halftone cloud texture) with a nav of Tools / Archetypes / Facets / News / About plus 'Add a tool', and CTAs 'Browse all 85 tools' and 'Read dispatches'. Below the fold (h2s): 'Latest tools' as scored cards - Mobbin (3.5 / 25%), Avnac (3.3 / 50%), Quiver AI - a 'From the desk' editorial strip, and 'Browse by role' broken into archetypes: All Rounder, Art Director, Craft Specialist, Design Engineer, Design Ops, Non Designer. The scores/percentages frame it as a ranked, faceted comparison engine.

**How it works** — Fonts and styles are self-hosted (plus fonts.googleapis.com); analytics run through Fathom (cdn.usefathom.com) and Cloudflare (static.cloudflareinsights.com). No app-framework global is exposed in the DOM, but the CSS uses an oklch() color system (Tailwind-style) and a Geist + custom 'Geist Pixel Square' type pairing. Media mix: 56 <img>, 5 <canvas> (the dithered/halftone cloud texture), 1 <iframe>, 6 <svg>, 0 video, over a 3,839px page.

**How it's designed** — A crisp editorial 'zine' look on white with a retro pixel-typewriter headline. getComputedStyle reports body background rgb(255,255,255) with near-black text oklch(0.205 0 0); the h1 renders in 'Geist Pixel Square' (monospace, 48px/500) - the blocky typewriter face that gives the hero its character - while body copy is Geist. No :root custom properties are exposed (Tailwind v4-style oklch is applied inline), so colours are read from the rendered page. Grain/dither and generous whitespace keep the dense comparison data feeling light.

**Palette** — White background with near-black text (oklch 0.205), a monochrome grayscale base warmed only by a dithered halftone cloud texture; scores/pills add small hits of contrast.
**Fonts** — Geist (400/500/600, loaded) for body + 'Geist Pixel Square' (loaded, 100-900) as the pixel/typewriter display face used in the hero h1.

## Connections
**Aesthetics:** [[aesthetics/editorial|editorial]] [[aesthetics/playful|playful]]
**Patterns:** [[patterns/directory|directory]] `comparison` `role-ranked` [[patterns/editorial|editorial]] [[patterns/pixel-type|pixel-type]] `typewriter` `halftone` `dither` `white` [[patterns/geist|geist]]
**Category:** [[categories/tools-build|tools-build]]
**Tech:** `Geist + Geist Pixel Square (self-hosted)` `Tailwind-style oklch color system` `Fathom Analytics` [[tech/cloudflare|Cloudflare]] [[tech/google-fonts|Google Fonts]]
**Colors:** [[colors/monochrome|monochrome]] [[colors/warm|warm]]
**Fonts:** [[fonts/geist|Geist]] `Geist Pixel Square 100-900`

## Related sites
[[sites/designengineer.tools|designengineer.tools]] [[sites/humanoid-index.com|humanoid-index.com]] [[sites/killedbyopenai.com|killedbyopenai.com]] [[sites/sensory-ui.com|sensory-ui.com]] [[sites/12matcha.com|12matcha.com]]
