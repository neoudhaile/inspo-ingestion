---
url: https://bird.onethreenine.net
title: "apartment birds"
category: uncategorized
aesthetics: []
tags: [single-screen, generative, live-data, collage, watercolor, system-fonts, iot, birdwatching]
extracted_at: 2026-06-06
---
# apartment birds
> A tiny microphone on my apartment balcony listens around the clock — realtime bird recognition via Cornell's BirdNET. NVIDIA ShadowPlay, but for birdsong.  ·  [bird.onethreenine.net](https://bird.onethreenine.net)

![bird.onethreenine.net](../../../screenshots/birdonethreeninenet.png)

**What it is** — The live front-end of Teddy Warner's 'Avian Visitors' project — a balcony microphone running Cornell's BirdNET that recognises passing birds in realtime and assembles them into a collage. The companion writeup lives at theodore.net/projects/AvianVisitors/ and the code at github.com/Twarner491/AvianVisitors.

**What it shows** — A single-screen 'apartment birds / HEARD RECENTLY' collage of watercolor bird illustrations whose prominence tracks how often each species was heard (e.g. 'House Sparrow — 1,121 calls today'), with a 1H / 12H / 24H / 7D / ALL time-range filter and COLLAGE / STATS / ATLAS tabs. Species are listed by common and Latin name (House Sparrow / Passer domesticus, House Finch, Hooded Oriole, Western Kingbird, Mourning Dove, Bullock's Oriole, American Crow…).

**How it works** — A vanilla-JS single-screen app (no framework global), served behind Cloudflare. The tab row swaps between the collage, a STATS view and an ATLAS, the time pills rescope the feed, and a 'menu' offers a password-gated tools panel ('enter password to unlock tools'). Data comes from the BirdNET pipeline running on the author's hardware.

**How it's designed** — A warm paper-and-ink scheme defined entirely in CSS variables — --paper #fcfcfb, --ink #1a1612, soft --ink-soft #908576 and a brown --accent #4a3f31 — with layered inset/raised box-shadow tokens for a tactile, letterpressed feel. Type is system-only: a serif display stack (ui-serif / Iowan Old Style / Bookman) for the 40px bold h1 and ui-monospace for the small 10px labels, with no webfont payload at all (document.fonts is empty). The 29 hand-painted watercolor bird illustrations are the entire visual identity.

**Palette** — Warm paper (#fcfcfb) with near-black ink (#1a1612) and a brown accent (#4a3f31)
**Fonts** — System only — serif display (Iowan Old Style) + ui-monospace labels; no webfonts loaded

## Connections
**Aesthetics:** —
**Patterns:** [[patterns/single-screen|single-screen]] [[patterns/generative|generative]] `live-data` `collage` `watercolor` [[patterns/system-fonts|system-fonts]] `iot` `birdwatching`
**Category:** [[categories/uncategorized|uncategorized]]
**Tech:** `Vanilla JS (no framework)` [[tech/cloudflare|Cloudflare]] `BirdNET (Cornell)`
**Colors:** [[colors/warm|warm]]
**Fonts:** [[fonts/system-fonts|system-fonts]]

## Related sites
[[sites/daryl.cv|daryl.cv]] [[sites/killedbyopenai.com|killedbyopenai.com]] [[sites/kmk0.com|kmk0.com]] [[sites/mo1.app|mo1.app]] [[sites/addyosmani.com|addyosmani.com]]
