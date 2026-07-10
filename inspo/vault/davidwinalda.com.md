---
url: https://davidwinalda.com/
domain: davidwinalda.com
title: "David Winalda"
category: tools-build
extracted_at: 2026-06-06
tags:
  - category/tools-build
  - aesthetic/minimal
  - aesthetic/light
  - pattern/personal-site
  - pattern/blog
  - pattern/minimalist
  - pattern/wordpress
  - pattern/light-theme
  - pattern/typographic
  - tech/wordpress-anders-nor-n-theme
  - tech/font-awesome-5
  - tech/self-hosted-no-third-party-analytics-detected
  - color/light
  - font/archivo
  - font/font-awesome
---
# David Winalda
> Personal site & blog — Articles, Blog, Quotes, Talks and the Terra Talks podcast.  ·  [davidwinalda.com](https://davidwinalda.com/)

![davidwinalda.com](../../screenshots/davidwinaldacom.png)

## What it is
David Winalda's personal WordPress site — the homepage doubles as an 'About Me' page and is the destination 0xMarioNawfal's shadcn/Claude-Code tweet links to. The nav reveals the scope: Articles, Blog, Quotes, Talks, a 'Terra Talks – Podcast', and a 'What I've Learned and Valued' page, plus a LinkedIn link. It is a writer/builder's home base rather than a product page.

## What it shows
A clean light-on-white homepage led by the 'David Winalda' wordmark and an 'About Me' heading, with a horizontal top nav (Articles / Blog / Quotes / Talks / Terra Talks – Podcast / What I've Learned and Valued) and a search affordance. No imagery, video or SVG on the landing screen — it is essentially a typographic index page.

## How it works
A classic WordPress build on an Anders Norén theme (the footer credits andersnoren.se), with WordPress's block-editor preset CSS variables sitting in :root and all CSS/JS served from davidwinalda.com itself. Archivo is the only text webfont (400/600/700) alongside Font Awesome 5 for icons; no SSR JS framework (__NEXT_DATA__/__NUXT__/Vue/Svelte/React all absent) and no third-party analytics host detected. The page is near-static and single-screen (~980px tall, 0 images/canvas/video/svg).

## How it's designed
A minimal light theme: white body (rgb(255,255,255)) with near-black text (--wp--preset--color--black #121212, rendered rgb(18,18,18)) and a solid black button (rgb(18,18,18)) carrying white text for the primary action. Type is set entirely in Archivo over a Helvetica Neue fallback, and there is no accent color, gradient, imagery or motion — hierarchy comes purely from weight and scale.

## Design data
- **Palette:** White #fff background, near-black #121212 text, solid black buttons — no accent color
- **Palette tokens:** --wp--preset--color--black: #121212 (var), --wp--preset--color--white: #fff (var), body-background: rgb(255, 255, 255) (rendered), body-text: rgb(18, 18, 18) (rendered), button-background: rgb(18, 18, 18) (rendered), button-text: rgb(255, 255, 255) (rendered)
- **Fonts:** Archivo 400/600/700 (with Font Awesome 5 icons), Helvetica Neue fallback
- **Fonts loaded:** Archivo 400, Archivo 600, Archivo 700, Font Awesome 5
- **Tech stack:** WordPress (Anders Norén theme), Font Awesome 5, self-hosted (no third-party analytics detected)
- **Media mix:** 
- **Page height:** 980px (single-screen: True)
- **Responsive:** At 390x844 the layout reflows to a single column at the same ~977px height with no hamburger menu (nav stays block-level); body type holds at 16px.
- **Headings:** David Winalda / About Me
- **Links out:** [LinkedIn](https://linkedin.com/in/davidwinalda) · [Theme: Anders Norén](https://andersnoren.se/)
- **Extracted:** 2026-06-06 · Playwright MCP, 1440x900 + 390x844, logged_out: true

## Related sites
[[alisawuffles.github.io]] [[performance.dev]] [[richzou.com]] [[willmanidis.com]] [[amanml.com]] [[anyblockers.com]]

## Tags
#category/tools-build #aesthetic/minimal #aesthetic/light #pattern/personal-site #pattern/blog #pattern/minimalist #pattern/wordpress #pattern/light-theme #pattern/typographic #tech/wordpress-anders-nor-n-theme #tech/font-awesome-5 #tech/self-hosted-no-third-party-analytics-detected #color/light #font/archivo #font/font-awesome
