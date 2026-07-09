---
url: https://recent.design/
title: "Recent — Design Inspiration"
category: design
aesthetics: []
tags: [design-gallery, directory, tailwind-v4, oklch, squircle, masonry, live-counter, inter, mono-accent]
extracted_at: 2026-07-05
---
# Recent — Design Inspiration
> The best design inspiration on the Internet.  ·  [recent.design](https://recent.design/)

![recent.design](../../../screenshots/recentdesign.png)

**What it is** — Recent (recent.design) is Daryl Ginn's daily-updated design-inspiration gallery — 'the best design inspiration on the Internet' — spanning Websites, OG Images, App Screenshots, App Icons, plus newer Tools and Skills collections. It's the subject of the bookmarked tweet celebrating how fast it's growing.

**What it shows** — A live gallery topped by a '30 online' presence counter and a 'Last updated 9h ago' freshness stamp. There's a category filter row (All, Web, Interface, Branding, Product, Typography, Motion, Illustration, 3D, Editorial, Print…), a top nav of collection types (Design, Websites, OG Images, App Screenshots, App Icons, Tools, Skills, Info), a promoted tool card (Raycast — 'A faster command center for launching work and tools — Get 10% off'), and a 'Subscribe to the Recent digest / Stay ahead of trends' weekly-email CTA ('joining 262 people today').

**How it works** — A dense client-rendered gallery — 141 img, 42 video, 66 svg — self-hosted on recent.design. Notably it runs on Daryl's own analytics product, visitors.now (cdn.visitors.now), plus Cloudflare Insights. No Next/Nuxt/Svelte root was exposed; the styling is a large Tailwind-v4 token system (OKLCH color scales, superellipse 'squircle' corner-shape tokens, dedicated app-icon radius tokens).

**How it's designed** — A neutral, content-first shell that lets the thumbnails supply all the color. From the DOM the background is white (rgb(255,255,255)) with a near-black foreground token --color-foreground #202020 (body color oklch(0.205 0 0)). The type system is Inter (variable 100–900, the only loaded webfont) for everything, with Departure Mono declared as the mono/decimal face for the counters and metadata. An extensive OKLCH accent palette (red/orange/amber/yellow/green/sky/blue/purple/pink scales) is reserved for tag chips, and squircle corner-shapes (superellipse 1.25–1.8) plus app-icon radius tokens shape the cards.

**Palette** — White canvas with #202020 near-black foreground; a full OKLCH accent system (red/amber/green/sky/blue/purple/pink) reserved for tag chips — the gallery thumbnails provide the actual color.
**Fonts** — Inter Variable (100–900) for all text — the only loaded webfont — with Departure Mono for numeric/metadata (counters, timestamps).

## Connections
**Aesthetics:** —
**Patterns:** `design-gallery` [[patterns/directory|directory]] [[patterns/tailwind-v4|tailwind-v4]] `oklch` `squircle` `masonry` `live-counter` [[patterns/inter|inter]] [[patterns/mono-accent|mono-accent]]
**Category:** [[categories/design|design]]
**Tech:** [[tech/tailwind-css-v4|Tailwind CSS v4]] `visitors.now (analytics)` [[tech/cloudflare|Cloudflare]]
**Colors:** [[colors/warm|warm]] [[colors/cool|cool]]
**Fonts:** [[fonts/inter-100-900-variable|Inter 100-900 (variable)]]

## Related sites
[[sites/nicelydone.club|nicelydone.club]] [[sites/cofounder.co|cofounder.co]] [[sites/21st.dev|21st.dev]] [[sites/animations.dev|animations.dev]] [[sites/coolsites.ai|coolsites.ai]]
