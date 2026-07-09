---
url: https://spacetypegenerator.com/
title: "SPACE TYPE GENERATOR"
category: favorites
aesthetics: [experimental, developer-product]
tags: [kinetic-typography, type-tool, canvas, 3d-type, generative, monospace-ui, control-panel, slider-driven, ibm-plex-mono, white-canvas]
extracted_at: 2026-06-06
---
# SPACE TYPE GENERATOR
> "a kinetic type generator from kielm" — type a phrase and bend it through 3D space with dozens of live sliders and presets.  ·  [spacetypegenerator.com](https://spacetypegenerator.com/)

![spacetypegenerator.com](../../../screenshots/spacetypegeneratorcom.png)

**What it is** — Space Type Generator (STG) by kielm — a browser-based kinetic typography tool. You enter a string and it is extruded and warped through 3D space on a canvas, here in its "_V.CYLINDER 1.1" mode wrapping the text "I-TRY-ALL-THINGS;-I-ACHIEVE-WHAT-I-CAN.//" around a cylinder.

**What it shows** — A bright white stage with the live black type composition floating in the centre. A dense left rail of red-handled sliders controls the geometry — grouped CYLINDER (radius/count/rotate/offset), WAVE (count/speed/latitude/longitude/ripple/x-y scale), TYPE (x/y scale, weight) and TWEAK (x/y/z rotation) — while a bottom rail adds CAMERA rotation/zoom sliders and a row of one-click preset buttons (Simple, Jellyfish, Crown, Complex, Weave, Zebra, Hoops). Top-right holds a "Select..." preset dropdown and a "PRIDE!" button plus Type Color / Background swatches; the bottom-right card carries the title, the text input, a "Buy me a coffee" support link and a ReadMe button. The mode menu (CYLINDER / FIELD / STRIPES / COIL / FLAG / MORISAWA / CASCADE / RIBBON / LAYERS / DANGER / STRING / BADGE / CLUTTER) routes to a dozen sibling generators.

**How it works** — The composition renders to a single <canvas>; window.THREE is not exposed as a global, so the 3D type is drawn on a self-contained canvas pipeline rather than the global Three.js object. Each generator mode is its own route (/field, /stripes, /coil, /flag, /morisawa, …). Libraries are pulled from cdnjs (Cloudflare), the site is fronted by Cloudflare (with cloudflareinsights beacon), and Google Analytics / Tag Manager are loaded. IBM Plex Mono is served from Google Fonts.

**How it's designed** — A deliberately tool-like, almost engineering-UI look: stark white canvas, everything set in IBM Plex Mono (weights 100/300/400) so the labels read like a control panel, and saturated red slider thumbs as the single accent against the monochrome black-on-white type. The pitch copy is set as a highlighted h1 ("SPACE TYPE GENERATOR", white on a dark chip) in the lower-right. The chrome frames the stage on all four edges, keeping the kinetic type centred and uncluttered while exposing an intimidatingly deep parameter set.

**Palette** — White stage with black rendered type; UI labels in black IBM Plex Mono and saturated red (slider thumbs) as the lone accent; the title chip inverts to white-on-dark
**Fonts** — IBM Plex Mono (weights 100 / 300 / 400, served from Google Fonts) throughout the UI

## Connections
**Aesthetics:** [[aesthetics/experimental|experimental]] [[aesthetics/developer-product|developer-product]]
**Patterns:** `kinetic-typography` `type-tool` [[patterns/canvas|canvas]] `3d-type` [[patterns/generative|generative]] [[patterns/monospace-ui|monospace-ui]] `control-panel` `slider-driven` `ibm-plex-mono` `white-canvas`
**Category:** [[categories/favorites|favorites]]
**Tech:** `Canvas-based 3D type renderer (no global THREE detected)` `Libraries via cdnjs (Cloudflare)` `Cloudflare CDN + cloudflareinsights beacon` `Google Analytics + Google Tag Manager` `Google Fonts (IBM Plex Mono)`
**Colors:** [[colors/neutral|neutral]]
**Fonts:** [[fonts/ibm-plex-mono|IBM Plex Mono]]

## Related sites
[[sites/ditther.com|ditther.com]] [[sites/killedbyopenai.com|killedbyopenai.com]] [[sites/bird.onethreenine.net|bird.onethreenine.net]] [[sites/colf.dev|colf.dev]] [[sites/hw.cafe|hw.cafe]]
