---
url: https://mapzilla.co.uk/
domain: mapzilla.co.uk
title: "mapzilla — the data-visualisation & cartography portfolio of Craig Taylor"
vertical: portfolio
mode: light
vibe: [minimal, experimental]
topics: [art, design]
extracted_at: 2026-07-08
tags:
  - vertical/portfolio
  - vibe/minimal
  - vibe/experimental
  - topic/art
  - topic/design
  - mode/light
---
# mapzilla — the data-visualisation & cartography portfolio of Craig Taylor
> 3D maps, terrain and movement data rendered as art (derived; the page ships no meta description).  ·  [mapzilla.co.uk](https://mapzilla.co.uk/)

![mapzilla.co.uk](../../screenshots/mapzillacouk.png)

**Vertical:** #vertical/portfolio  ·  **Vibe:** #vibe/minimal #vibe/experimental  ·  **Topics:** #topic/art #topic/design  ·  **Mode:** #mode/light

## What it is
The portfolio of Craig Taylor ('mapzilla'), a Squarespace site with page title simply 'mapzilla' and no meta description or on-page h1/h2 — the page is a project index. The Mapbox + three.js terrain-occlusion demo in the tweet is his recent work; this site collects the broader body of it.

## What it shows
A dense two-column grid of vivid 3D data-visualisation / cartography projects (rendered as h3 titles): 'NBA All-Star Weekend Data Visualisation', '#TransitVizThursdays | Innovative Transit Dataviz', 'Coral Cities: Updated Workflow 2023', 'XMEN Map Pin-Table', 'MTB DataViz & Analytics', 'Fractal Cities', 'Make sense of it all: Mapping Movement', 'The Global Tanaka Project', '2022 Wrapped', 'The BODS Bus Trilogy', '2021 Wrapped', 'Miniature Worlds', 'City Domes', 'Window Cities' and 'Commuter Flowers'. A slim top nav reads Projects / Tutorials / Instagram / Contact.

## How it works
Built on Squarespace (scripts and styles from static1.squarespace.com, assets.squarespace.com and definitions.sqspcdn.com), with webfonts from Adobe Typekit (use.typekit.net) and Google Fonts. The index is static and image-heavy — 45 <img>, 15 <svg>, 0 canvas/video/iframe — over a 12,320px page; the live WebGL/three.js pieces live inside individual project pages rather than on the index.

## How it's designed
A minimal white frame around maximalist imagery. The Squarespace theme sets --siteBackgroundColor hsla(0,0%,100%,1) and getComputedStyle confirms a white body rgb(255,255,255) with black text. There is no h1/h2 — project titles render as h3. Type is Poppins (loaded 300/500) for the UI/nav, with ITC Avant Garde Gothic Pro declared via Typekit but unloaded on the index, plus Squarespace's own UI/social icon fonts. All colour comes from the saturated project thumbnails — glowing city-light maps, coral-like data blooms, iridescent terrain and 'Commuter Flowers' — against the white gallery.

## Design data
- **Palette:** White canvas (--siteBackgroundColor #fff) with black text; every hit of colour comes from the saturated 3D map / data-viz thumbnails.
- **Palette tokens:** --siteBackgroundColor: hsla(0,0%,100%,1) (var), body background: rgb(255, 255, 255) (rendered), body text: rgb(0, 0, 0) (rendered)
- **Fonts:** Poppins (loaded 300/500) for UI and nav; ITC Avant Garde Gothic Pro declared via Adobe Typekit but unloaded on the index; plus Squarespace's UI and social-icon fonts.
- **Fonts loaded:** Poppins 300, Poppins 500
- **Tech stack:** Squarespace, Adobe Typekit, Google Fonts
- **Keywords:** portfolio, data-viz, cartography, 3d, squarespace, gallery-grid, white, poppins, maximalist-imagery, generative
- **Media mix:** img 45 · svg 15
- **Page height:** 12320px (single-screen: False)
- **Responsive:** At 390x844 Squarespace swaps in its mobile header (hamburger menu) and the two-column project grid reflows to a single column; overall height is essentially unchanged (12,320 -> 12,412px).
- **Headings:** NBA All-Star Weekend Data Visualisation / #TransitVizThursdays | Innovative Transit Dataviz / Coral Cities: Updated Workflow 2023 / XMEN Map Pin-Table / MTB DataViz & Analytics / Fractal Cities / Make sense of it all: Mapping Movement / The Global Tanaka Project / 2022 Wrapped / The BODS Bus Trilogy / 2021 Wrapped / Miniature Worlds / City Domes / Window Cities / Commuter Flowers
- **Weight:** None requests; hosts: mapzilla.co.uk, static1.squarespace.com, assets.squarespace.com, definitions.sqspcdn.com, use.typekit.net, fonts.googleapis.com
- **Extracted:** 2026-07-08 · Playwright MCP, 1440x900 fullPage + 390x844 mobile probe; logged_out: true.

## Related sites
- [[gaspardhedde.fr]] — shared: portfolio, minimal, experimental, design, light
- [[jasonyuan.design]] — shared: portfolio, minimal, experimental, design
- [[asekachov.com]] — shared: portfolio, minimal, design, light
- [[backgrounds.supply]] — shared: minimal, experimental, art, design
- [[christophlocher.com]] — shared: portfolio, minimal, design, light
- [[daryl.cv]] — shared: portfolio, minimal, design, light
