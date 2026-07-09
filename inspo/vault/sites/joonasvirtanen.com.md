---
url: https://www.joonasvirtanen.com/
title: "Joonas Virtanen - Portfolio"
category: design
aesthetics: [portfolio, light, editorial, minimal]
tags: [portfolio, light-mode, editorial, serif-display, whitespace, video-led, webflow, single-page-scroll]
extracted_at: 2026-06-05
---
# Joonas Virtanen - Portfolio
> Portfolio of a Finnish experience designer & creative director currently living in NYC.  ·  [joonasvirtanen.com](https://www.joonasvirtanen.com/)

![joonasvirtanen.com](../../../screenshots/joonasvirtanencom.png)

**What it is** — The personal portfolio of Joonas Virtanen, a Finnish product designer & creative director living in NYC (h1: 'Moi! I'm Joonas Virtanen, a Finnish product designer & creative director currently living in NYC.'). The tweet showcases a generative weather toy — a site that 'picks the closest Rothko for how the weather feels outside your window' — and its t.co link resolves to this domain, so the homepage is the captured destination; the Rothko piece itself isn't surfaced as a separate nav link (a 'Playground' section holds his side projects).

**What it shows** — A near-empty, mostly-white editorial homepage where a single centered serif paragraph introduces him, followed by a long list of case studies (Wealthsimple rebrand, an instant-payments app, a Sundance documentary action hub, a 'sight simulator', blind street-art project, fwd.us) that load as autoplaying project videos on scroll, and a closing 'say hi' block linking out to Instagram, LinkedIn, Dribbble, Twitter, Vimeo and Medium.

**How it works** — A long single scroll (~8,723px) built in Webflow; the work grid is video-led (7 inline <video> plus 5 iframes) with project clips served from a DigitalOcean Spaces CDN and assets from Webflow's website-files CDN. No analytics host is exposed. Content is anchored (#work, #about, #contact) off a thin top nav.

**How it's designed** — Quiet, type-first gallery aesthetic: a white ground (rgb(255,255,255)) with near-black text (rgb(18,18,18)) and an enormous amount of negative space, so the centered Canela serif hero (65px) carries the whole page. A single firebrick red (--firebrick #c72e2e) is the only declared accent. Body copy is set in Post Grotesk; the declared family list also names PP Neue Montreal and Romie, but only Canela and Post Grotesk Light actually load as webfonts.

**Palette** — White ground (rgb(255,255,255)) with near-black text (rgb(18,18,18)); a single firebrick-red accent (--firebrick #c72e2e), otherwise monochrome and whitespace-led.
**Fonts** — Canela (serif display, the centered hero) + Post Grotesk (body sans); PP Neue Montreal and Romie are declared but unused — only Canela 300 and Post Grotesk Light 300 actually load.

## Connections
**Aesthetics:** [[aesthetics/portfolio|portfolio]] [[aesthetics/light|light]] [[aesthetics/editorial|editorial]] [[aesthetics/minimal|minimal]]
**Patterns:** [[patterns/portfolio|portfolio]] [[patterns/light-mode|light-mode]] [[patterns/editorial|editorial]] [[patterns/serif-display|serif-display]] `whitespace` `video-led` [[patterns/webflow|webflow]] `single-page-scroll`
**Category:** [[categories/design|design]]
**Tech:** [[tech/webflow|Webflow]] `DigitalOcean Spaces (video CDN)` [[tech/no-analytics-detected|no analytics detected]]
**Colors:** [[colors/light|light]] [[colors/monochrome|monochrome]]
**Fonts:** `Canela` `Post Grotesk Light`

## Related sites
[[sites/siddz.com|siddz.com]] [[sites/asekachov.com|asekachov.com]] [[sites/christophlocher.com|christophlocher.com]] [[sites/claude.com|claude.com]] [[sites/contralabs.com|contralabs.com]]
