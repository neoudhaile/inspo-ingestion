---
url: https://the-cafelist.com/nyc/
domain: the-cafelist.com
title: "NYC Cafe List"
vertical: directory-gallery
mode: light
vibe: [organic-warm, editorial]
topics: [food-drink, travel-places]
extracted_at: 2026-06-05
tags:
  - vertical/directory-gallery
  - vibe/organic-warm
  - vibe/editorial
  - topic/food-drink
  - topic/travel-places
  - mode/light
---
# NYC Cafe List
> A hand-curated guide to work-friendly coffee shops, across cities.  ·  [the-cafelist.com](https://the-cafelist.com/nyc/)

![the-cafelist.com](../../screenshots/thecafelistcom.png)

**Vertical:** #vertical/directory-gallery  ·  **Vibe:** #vibe/organic-warm #vibe/editorial  ·  **Topics:** #topic/food-drink #topic/travel-places  ·  **Mode:** #mode/light

## What it is
A hand-curated, Beli-style directory of work-friendly NYC coffee shops (the nyccafelist.com bookmark redirects here to the-cafelist.com/nyc/). The site's own pitch in the meta is 'A hand-curated guide to work-friendly coffee shops, across cities,' and the page's single h1 is simply 'NYC Cafes.'

## What it shows
A two-pane app: a left scroll column of ranked cafes — each row with a name, neighborhood, a numeric score chip, and a thumbnail (e.g. Amaà Vidà 7.5, La Tazza D'Oro 7.4, Le Club Café 9.3, Stripes Wine Bar & Café) — beside a right-hand interactive map of Manhattan/Brooklyn dense with green location pins.

## How it works
It behaves like a ranked map-directory rather than a scrolling page: the body fits the viewport (scrollHeight equals innerHeight at 1440x900) and the cafe list scrolls internally while the map stays pinned. Header controls cover search, sort/filter, and a 'Submit' (cafe nomination) CTA; rows pair with map pins so picking a cafe locates it.

## How it's designed
Warm 'paper café' aesthetic rendered in a light theme — an off-white canvas (rgb 247,246,243) with espresso-brown ink (rgb 41,36,31) and a terracotta accent (--primary hsl 12 55% 58%) used for scores and the focus ring. Typography mixes a DM Serif Display masthead, DM Sans body, and IBM Plex Mono for the tabular score numerals (the CSS even sets tabular-nums); a Caveat handwriting face is defined in the stack but was not loaded. Built as a React single-page app styled with Tailwind and shadcn/sonner toasts; 157 inline SVGs (pin and UI icons) and 136 images (cafe thumbnails) carry the visual density.

## Design data
- **Palette:** Warm paper off-white (rgb 247,246,243) with espresso-brown ink (rgb 41,36,31) and a terracotta score/accent (hsl 12 55% 58%).
- **Palette tokens:** --background: 30 12% 9% (var), --foreground: 36 22% 90% (var), --primary: 12 55% 58% (var), --accent: 12 55% 58% (var), --open-status: 142 50% 48% (var), --warm: 36 30% 50% (var), body background: rgb(247, 246, 243) (rendered), body text: rgb(41, 36, 31) (rendered), link/button text: rgb(124, 116, 106) (rendered)
- **Fonts:** DM Sans body, DM Serif Display headings, IBM Plex Mono numerals (Caveat handwriting accent defined but not loaded).
- **Fonts loaded:** DM Sans 400, DM Serif Display 400, IBM Plex Mono 400, IBM Plex Mono 500, IBM Plex Mono 600
- **Tech stack:** React, Tailwind CSS, shadcn/sonner toasts, Google Tag Manager, self-hosted
- **Keywords:** list-plus-map, two-pane, leaderboard-ranking, interactive-map, filter-chips, curated-directory, score-chips
- **Media mix:** img 136 · svg 157
- **Page height:** 900px (single-screen: True)
- **Responsive:** At 390px the two-pane layout collapses to a single full-height list view with a 'Full map' toggle button; filter chips (Open / Rating / Filter) and a 'Nominate' CTA remain.
- **Headings:** NYC Cafes
- **Extracted:** 2026-06-05 · Playwright MCP — 1440x900 fullPage + DOM probe + 390x844 mobile pass, logged_out: true

## Related sites
- [[21st.dev]] — shared: directory-gallery, editorial, light
- [[are.na]] — shared: directory-gallery, editorial, light
- [[coolsites.ai]] — shared: directory-gallery, organic-warm, light
- [[designtools.fyi]] — shared: directory-gallery, editorial, light
- [[type.lol]] — shared: directory-gallery, editorial, light
- [[typo.love]] — shared: directory-gallery, organic-warm, light
