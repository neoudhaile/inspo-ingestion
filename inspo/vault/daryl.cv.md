---
url: https://daryl.cv/
domain: daryl.cv
title: "Daryl Ginn — designer & developer"
vertical: portfolio
mode: light
vibe: [brutalist, minimal]
topics: [design]
extracted_at: 2026-07-05
tags:
  - vertical/portfolio
  - vibe/brutalist
  - vibe/minimal
  - topic/design
  - mode/light
---
# Daryl Ginn — designer & developer
> A self-taught designer and developer from Australia.  ·  [daryl.cv](https://daryl.cv/)

![daryl.cv](../../screenshots/darylcv.png)

**Vertical:** #vertical/portfolio  ·  **Vibe:** #vibe/brutalist #vibe/minimal  ·  **Topics:** #topic/design  ·  **Mode:** #mode/light

## What it is
daryl.cv is the personal index of Daryl Ginn — the tweet's author — 'a self-taught designer and developer' with ~20 years in the industry. It's the author-portfolio hub that lists the products and studios he's launched, of which Recent.design is the current one.

## What it shows
A single-screen text page: a trilingual greeting ('Hi, hola, こんにちは'), a short bio, and a chronological list of his ventures — System (system.studio, a brand design studio launching 2026), Visitors (visitors.now, a 'privacy friendly, revenue-first web analytics platform', 2025), Endless (endless.design, a design agency, 2023), and Godly (godly.website) — plus a Contact line. An 'Updated 23 March 2026' stamp sits under his name.

## How it works
Intentionally minimal — a hand-built single HTML screen (scrollHeight equals innerHeight at 900px), with zero images/svg/canvas/video, no CSS custom properties, and no webfonts at all. The only third-party script is his own visitors.now analytics (cdn.visitors.now).

## How it's designed
Radical restraint, used as a designer's flex. From the DOM the page uses the system-ui font stack only — document.fonts is completely empty, so there's no webfont payload — with body and h1 at a uniform 14px in near-black (rgb(0,0,0)) on default white, and classic default-blue hyperlinks (rgb(0,0,238)). The whole thing reads like a plain-text résumé: deliberately anti-design.

## Design data
- **Palette:** Black text (rgb(0,0,0)) on default white, with browser-default-blue hyperlinks (rgb(0,0,238)) — no custom palette.
- **Palette tokens:** body color: rgb(0, 0, 0) (rendered), link color: rgb(0, 0, 238) (rendered)
- **Fonts:** System fonts only (system-ui / -apple-system) — no webfont payload; document.fonts is empty.
- **Fonts loaded:** system only (no webfont)
- **Tech stack:** Static HTML/CSS, visitors.now (analytics)
- **Keywords:** minimalist, text-only, system-fonts, single-screen, personal-index, anti-design
- **Media mix:** 
- **Page height:** 900px (single-screen: True)
- **Responsive:** At 390x844 it stays a single screen (844px); the content just reflows to a narrower column at the same 14px text size.
- **Headings:** Daryl Ginn / Hi, hola, こんにちは / System (soon) / Visitors / Endless / Godly / Contact
- **Links out:** [System](https://system.studio/) · [Visitors](https://visitors.now/) · [Endless](https://endless.design/) · [Godly](https://godly.website/) · [@darylginn](https://x.com/darylginn)
- **Extracted:** 2026-07-05 · Playwright MCP, 1440x900 + 390x844 mobile pass, logged_out: true

## Related sites
- [[arneshbanerjee.github.io]] — shared: portfolio, brutalist, minimal, light
- [[asekachov.com]] — shared: portfolio, minimal, design, light
- [[christophlocher.com]] — shared: portfolio, minimal, design, light
- [[designrebuilds.vercel.app]] — shared: portfolio, minimal, design, light
- [[gaspardhedde.fr]] — shared: portfolio, minimal, design, light
- [[joonasvirtanen.com]] — shared: portfolio, minimal, design, light
