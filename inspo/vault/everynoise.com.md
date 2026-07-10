---
url: https://everynoise.com/
domain: everynoise.com
title: "Every Noise at Once"
vertical: tool-app
mode: light
vibe: [technical]
topics: [music]
extracted_at: 2026-06-06
tags:
  - vertical/tool-app
  - vibe/technical
  - topic/music
  - mode/light
---
# Every Noise at Once
> An algorithmically-generated, readability-adjusted scatter-plot of the musical genre-space.  ·  [everynoise.com](https://everynoise.com/)

![everynoise.com](../../screenshots/everynoisecom.png)

**Vertical:** #vertical/tool-app  ·  **Vibe:** #vibe/technical  ·  **Topics:** #topic/music  ·  **Mode:** #mode/light

## What it is
Glenn McDonald's Every Noise at Once (everynoise.com) — in the page's own words, "a long-running attempt at an algorithmically-generated, readability-adjusted scatter-plot of the musical genre-space, based on data tracked and analyzed for 6,291 genre-shaped distinctions at Spotify through 2023-11-19." The copy is now past-tense: the project was frozen after the author's Spotify data access ended, so the map is a preserved snapshot.

## What it shows
A single enormous canvas (~24,700px tall) packed with ~6,291 clickable genre names — pop, rap, rock, urbano latino, reggaeton, k-pop, corridos tumbados — laid out as a dense word-cloud/scatter-plot. Position encodes sound (down = more organic/acoustic, up = more mechanical/electric; left = denser & atmospheric, right = spikier & bouncier), color encodes the genre's timbral character, and font size encodes popularity. Clicking a genre name plays an audio sample of it; the » arrow beside each opens that genre's own sub-map (engenremap-pop.html, etc.). A slim top nav offers scan / list / playlist / book / more, linking out to the 'Sounds of Spotify' playlists.

## How it works
Old-school static HTML and vanilla JavaScript — no framework (__NUXT__/__NEXT_DATA__/React/jQuery all absent), no CSS custom properties, no webfont payload. Each genre is an absolutely-positioned text node with an inline onclick handler; the whole ~1,618px-wide grid is one giant pre-rendered layout (~12,589 interactive nodes counting every tile and its » preview link). Audio plays via embedded Spotify previews. It is deliberately lo-fi infrastructure carrying an extraordinarily information-dense visualization.

## How it's designed
Function over decoration: a plain white background with each genre label colored by its own algorithmically-assigned hue (warm golds and ochres over the pop/rap/rock cluster, blues and greens elsewhere), so the palette IS the data rather than a brand choice. Everything is set in Gill Sans (GillSansRegular with Gill Sans MT / Trebuchet fallbacks), the only typeface on the page. There is no chrome, no card, no grid lines — just thousands of clickable colored words floating in space, with a giant faint blue "YOU HAVE NOT YET HEARD" easter-egg watermark behind the cloud.

## Design data
- **Palette:** White canvas with per-genre algorithmic label colors (data-driven, no fixed brand palette) — warm golds/ochres rgb(173,137,7)/rgb(189,144,2) over the pop/rap/rock cluster, plus a faint blue rgb(34,88,165) watermark
- **Palette tokens:** body-bg: rgb(255, 255, 255) (rendered), body-color: rgb(0, 0, 0) (rendered), genre-pop-color: rgb(173, 137, 7) (rendered), genre-rap-color: rgb(167, 138, 3) (rendered), watermark-blue: rgb(34, 88, 165) (rendered)
- **Fonts:** Gill Sans only (GillSansRegular, with Gill Sans MT / Gill Sans / Trebuchet MS fallbacks) — no webfont loaded, system/local font
- **Fonts loaded:** system only (no webfont)
- **Tech stack:** static HTML + vanilla JavaScript, no framework (no React/Vue/Next/Nuxt/jQuery detected), inline onclick handlers, embedded Spotify audio previews, no webfonts, no CSS variables
- **Keywords:** data-visualization, scatter-plot, word-cloud, music-map, interactive-audio, information-dense, static-html, no-framework, color-encodes-data, archived
- **Media mix:** img 5 · iframe 1
- **Page height:** 24729px (single-screen: False)
- **Responsive:** Not responsive: the map keeps its fixed ~1,618px-wide absolutely-positioned layout at 390x844, overflowing the viewport horizontally so mobile users must pinch-zoom and pan rather than getting a reflowed column.
- **Links out:** [list (1-D genre list)](https://everynoise.com/everynoise1d.html) · [playlist (Sounds of Spotify)](https://open.spotify.com/user/thesoundsofspotify/playlist/69fEt9DN5r4JQATi52sRtq) · [@EveryNoise / glenn mcdonald](https://everynoise.com/#updates)
- **Weight:** None requests; hosts: everynoise.com
- **Extracted:** 2026-06-06 · Playwright MCP, 1440x900 + 390x844 mobile pass, logged_out: true

## Related sites
- [[akira.sachi.dev]] — shared: tool-app, technical, light
- [[colf.dev]] — shared: tool-app, technical, light
- [[itshover.com]] — shared: tool-app, technical, light
- [[spacetypegenerator.com]] — shared: tool-app, technical, light
- [[cafe.endofday.studio]] — shared: tool-app, music
- [[ditther.com]] — shared: tool-app, technical
