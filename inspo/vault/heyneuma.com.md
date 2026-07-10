---
url: https://heyneuma.com/
domain: heyneuma.com
title: "Neuma — 'Build your ideas by talking to AI' (a Claude Code personal-AI course)"
vertical: docs-resource
mode: light
vibe: [organic-warm]
topics: [ai, education]
extracted_at: 2026-07-08
tags:
  - vertical/docs-resource
  - vibe/organic-warm
  - topic/ai
  - topic/education
  - mode/light
---
# Neuma — 'Build your ideas by talking to AI' (a Claude Code personal-AI course)
> Build your ideas by talking to AI.  ·  [heyneuma.com](https://heyneuma.com/)

![heyneuma.com](../../screenshots/heyneumacom.png)

**Vertical:** #vertical/docs-resource  ·  **Vibe:** #vibe/organic-warm  ·  **Topics:** #topic/ai #topic/education  ·  **Mode:** #mode/light

## What it is
'Neuma' (heyneuma.com) — a hands-on course whose meta description reads 'A hands-on course on building personal AI systems with Claude Code. No programming background required. A framework for people who think.' It is priced $129 (a Stripe checkout link), authored by Kris Puckett (whose bio/testimonial closes the page) and cross-links his 'Epilogue — Ambient Reading' iOS app. IMPORTANT CAVEAT: this URL appears in the tweet's export metadata (all_urls) but its content is unrelated to Jason Yuan's post about Dot — treat the association as an artifact of link harvesting, not an endorsed subject site. It is included here because it was captured and is a useful reference in its own right.

## What it shows
A warm, paper-toned course landing page. The hero pairs 'Build your ideas / by talking to AI.' with a terracotta 'Enroll · $129' button and a 'See What You Build' link over a stat row (20 modules, 200+ builders, 90-day guarantee). Sections that follow: 'Watch. Build. Keep.', 'Your first build: a personal OS', 'Not a prompt course. A way of building.', '20 modules. Your first build. Then anything you want.', 'Learn to build anything. Keep everything.', a 'Common questions' FAQ and a closing 'Kris Puckett' author block.

## How it works
Self-hosted — every script and stylesheet is served from heyneuma.com, with no app-framework global (not Next / Nuxt / Vue / Svelte); the CSS shows Tailwind's --tw-* tokens and lab()-based neutral scale, so it is most likely a Tailwind + Vite build. Media-light: 1 <img>, 33 inline <svg>, 0 canvas/video/iframe, over a tall 10,617px page. Outbound CTAs go to a Stripe checkout and the Apple App Store (Epilogue).

## How it's designed
A warm 'paper' aesthetic driven by an explicit token system. :root defines --bg #fdf6f0 (warm cream), --text-primary #2a1a14 (cocoa ink), --accent #c4725c (terracotta) and --accent-bright #a85840, plus a soft mesh-gradient set (--mesh-c1 #f0d0c0, --mesh-c2 #f0c8d0, --mesh-c3 #d8c0e0, --mesh-c4 #f5eae0) and a faint grain/noise layer (--noise-opacity .02, --grain-blend multiply). getComputedStyle confirms body renders at rgb(253,246,240) with rgb(42,26,20) text and the h1 at 64px/800. Type (document.fonts): Geist Sans + Geist Mono are loaded, and a family of 'Geist Pixel' display faces (Square / Grid / Circle / Triangle / Line) is declared but reports unloaded.

## Design data
- **Palette:** Warm cream paper (#fdf6f0) with cocoa ink (#2a1a14) and a terracotta accent (#c4725c); soft pink/lavender mesh-gradient tints plus a faint grain overlay.
- **Palette tokens:** --bg: #fdf6f0 (var), --text-primary: #2a1a14 (var), --accent: #c4725c (var), --accent-bright: #a85840 (var), --mesh-c3: #d8c0e0 (var), body background: rgb(253, 246, 240) (rendered), body text: rgb(42, 26, 20) (rendered)
- **Fonts:** Geist Sans + Geist Mono (both loaded); a set of 'Geist Pixel' display faces (Square/Grid/Circle/Triangle/Line) declared but unloaded.
- **Fonts loaded:** Geist Sans, Geist Mono
- **Tech stack:** Self-hosted (no framework global; Tailwind CSS tokens present), Stripe (checkout)
- **Keywords:** course-landing, warm, cream, terracotta, paper, mesh-gradient, grain, geist, tailwind, personal-ai, claude-code
- **Media mix:** img 1 · svg 33
- **Page height:** 10617px (single-screen: False)
- **Responsive:** At 390x844 the hero and CTA stack vertically and the multi-column testimonial/module grids reflow to a single column; the tall scroll-triggered body stays a long single-column read.
- **Headings:** Build your ideas by talking to AI. / Watch. Build. Keep. / Your first build: a personal OS / Not a prompt course. A way of building. / 20 modules. Your first build. Then anything you want. / Learn to build anything. Keep everything. / Common questions / Kris Puckett
- **Links out:** [Enroll · $129 (Stripe)](https://buy.stripe.com/28E9AS2LOfTZemAdi42cg03) · [Epilogue — Ambient Reading (iOS)](https://apps.apple.com/us/app/epilogue-ambient-reading/id6751764862)
- **Extracted:** 2026-07-08 · Playwright MCP, 1440x900 fullPage + 390x844 mobile probe; logged_out: true. NOTE: the fullPage capture painted mostly the hero — the lower scroll-triggered sections did not render in the static full-page shot.

## Related sites
- [[walkinglabs.github.io]] — shared: docs-resource, organic-warm, ai, education, light
- [[hofai.io]] — shared: docs-resource, ai, education
- [[midu.dev]] — shared: docs-resource, education, light
- [[alisawuffles.github.io]] — shared: ai, education, light
- [[backdoorai.app]] — shared: organic-warm, ai, light
- [[coolsites.ai]] — shared: organic-warm, ai, light
