---
url: https://canivibecodeit.com/
domain: canivibecodeit.com
title: "Can I Vibecode It? · what AI can rebuild, what survives"
vertical: directory-gallery
mode: light
vibe: [technical, playful]
topics: [ai, startups]
extracted_at: 2026-09-22
tags:
  - vertical/directory-gallery
  - vibe/technical
  - vibe/playful
  - topic/ai
  - topic/startups
  - mode/light
---
# Can I Vibecode It? · what AI can rebuild, what survives
> The live scoreboard of what AI can and can't replace, and which moats actually hold.  ·  [canivibecodeit.com](https://canivibecodeit.com/)

![canivibecodeit.com](../../screenshots/canivibecodeitcom.png)

**Vertical:** #vertical/directory-gallery  ·  **Vibe:** #vibe/technical #vibe/playful  ·  **Topics:** #topic/ai #topic/startups  ·  **Mode:** #mode/light

## What it is
canivibecodeit.com ("Can I Vibecode It?") is a live scoreboard site tracking which paid SaaS products AI coding agents can plausibly replace, per its own meta description: "The live scoreboard of what AI can and can't replace, and which moats actually hold. Honest verdicts on 1093 apps, the exact prompt to run, free."

## What it shows
A hero headlined "Can I vibecode ___?" sits above quick category chips (design, audio & video, website builders, scheduling, finance & accounting) and a scrolling ticker tallying "$2,295/mo" in SaaS bills already replaced, then the page drops into "The Death List" — a sortable, filterable leaderboard of 1,093+ apps (Granola, Wispr Flow, SuperX, Sleek, ...) each with a category, price, a YES/KINDA/NOT REALLY verdict badge, and a "replaced it" vote count, framed by small sponsor cards down each rail.

## How it works
Built on Astro (astro-transition-scope markers on the html element; no Vue/Nuxt/Next globals present) with Cloudflare Insights for analytics. The entire leaderboard renders as one continuous scroll — 66,871px tall on desktop — rather than paginating, and theming runs through a `data-theme` attribute on `<html>` (defaulted to the visitor's light preference here) with a full parallel dark palette defined in the same CSS custom properties.

## How it's designed
Terminal/stock-ticker aesthetic: a variable JetBrains Mono face carries the data-dense ticker and list rows while Space Grotesk Variable handles display headlines, and a green/amber/red verdict system (`--primary` #0b7c39 for YES, `--kinda-bg` #f5b300 for KINDA, `--no-bg` #e03131 for NOT REALLY) stands in for a stock up/down convention rather than a conventional brand palette.

## Design data
- **Palette:** Light-mode ground #f7f8f9 with white #ffffff card surfaces and ink text #15181d; verdict badges in green #0b7c39 (yes), amber #f5b300 (kinda), and red #e03131 (not really). A full dark theme (#0b0d0b ground, #33e667 accent) is defined in the same tokens but isn't the default here.
- **Palette tokens:** --bg: #f7f8f9 (var), --surface: #ffffff (var), --border: #d8dbe1 (var), --fg: #15181d (var), --muted: #5b6370 (var), --primary (yes): #0b7c39 (var), --kinda-bg (kinda): #f5b300 (var), --no-bg (not really): #e03131 (var), body background (rendered): rgb(247, 248, 249) (rendered), body text (rendered): rgb(21, 24, 29) (rendered)
- **Fonts:** Space Grotesk Variable (weight range 300–700, loaded) for display type; JetBrains Mono Variable (100–800, loaded) for the ticker and list data.
- **Fonts loaded:** Space Grotesk Variable 300-700, JetBrains Mono Variable 100-800
- **Tech stack:** Astro, Cloudflare Insights, Cloudflare (self-hosted assets)
- **Keywords:** leaderboard/scoreboard, verdict badges, ticker marquee, directory of apps, light/dark theme tokens, Astro
- **Media mix:** img 1119 · canvas 1 · svg 1102
- **Page height:** 66871px (single-screen: False)
- **Responsive:** At 390x844 the leaderboard just narrows into a single-column list — scrollHeight grows from 66,871px to 82,502px as the same rows stack taller rather than the layout restructuring.
- **Headings:** Can I vibecode ___? / The Death List / Every week, more subscriptions die. / Sign in
- **Extracted:** 2026-09-22 · desktop 1440x900, mobile 390x844 (layout check only); logged_out: true

## Related sites
- [[coolsites.ai]] — shared: directory-gallery, playful, ai, light
- [[b150.ai]] — shared: playful, ai, startups, light
- [[killedbyopenai.com]] — shared: directory-gallery, technical, ai
- [[motionsites.ai]] — shared: directory-gallery, technical, ai
- [[nicolasbustamante.com]] — shared: technical, ai, startups, light
- [[sceneai.art]] — shared: directory-gallery, technical, ai
