---
url: https://addyosmani.com/
title: "Addy Osmani"
category: personal
aesthetics: [portfolio, dark, light]
tags: [personal-hub, portfolio, author-site, books-grid, case-study-logos, light-dark-bands, oversized-display-type, system-fonts, section-index, static-page, link-rich]
extracted_at: 2026-06-05
---
# Addy Osmani
> Addy Osmani is a Software Engineer at Google working on Google Cloud and Gemini.  ·  [addyosmani.com](https://addyosmani.com/)

![addyosmani.com](../../../screenshots/addyosmanicom.png)

**What it is** — The personal homepage and link hub of Addy Osmani — a software engineer at Google (working on Google Cloud and Gemini, long known for Chrome/web performance) and a prolific author. The only h1 is simply his name, “Addy Osmani”; rather than a marketing landing page it is a dense, sectioned index of everything he makes: books, articles, talks and videos.

**What it shows** — It opens on a black hero band with a live-stage photo of Addy, his name set huge, a short bio and social links. Below, on a white ground, run titled sections: a Books grid of cover thumbnails (JS Design Patterns, Learning Patterns, Image Optimization, Success at Scale and other Smashing Magazine titles); a Case Studies row of company logos (eBay, Netflix, Tinder, Pinterest, Treebo, YouTube, Adobe, Twitter); a black “Featured AI articles” band of article cards (The Factory Model, Stop Using Just for READMEs, Claude Code Swarms, Agentic Engineering, Self-Improving Coding Agents); Featured thoughts cards; a row of contact/section cards (Personal projects, Open source, Premium, Talks, Blog); a Featured Videos and Shorts thumbnail grid; and a My Network footer. It is image-heavy (68 <img>, no inline SVG).

**How it works** — A static, scroll-driven single page (~6988px tall on desktop). There are no interactive widgets — navigation is scroll plus outbound links, each card linking to its book, article, video or external profile, with a newsletter/contact path via his Substack and socials. No client-side framework is present (no Nuxt/Next/React/Svelte/Gatsby globals) — a classic statically-generated site; Google Tag Manager + Google Analytics are the only third-party scripts and images are served from Cloudinary.

**How it's designed** — Monochrome and editorial: alternating light and dark bands — a white content ground bookended by a pure-black hero and a black “Featured AI articles” section (rendered backgrounds rgb(0,0,0)). The display name is set in Inter at weight 900 and 96px, white on black; everything else falls back to the system Helvetica Neue stack — only Inter 900 is actually loaded as a webfont (an 'icons' icon-font is declared but unloaded), so there is essentially no body webfont payload. Links on the dark hero are a light blue-grey (rgb(217,227,234)). The full-color company logos in the Case Studies row supply the only saturated color against the otherwise black-and-white scheme; hierarchy comes from the oversized name and tidy card grids rather than decorative type.

**Palette** — Monochrome — white content ground, pure-black hero and AI-articles bands (rgb 0/0/0), black body text; light blue-grey links on dark (rgb 217/227/234); full-color company logos as the only accents.
**Fonts** — Inter 900 for the oversized display name; system Helvetica Neue stack for body/UI (no body webfont); an 'icons' icon-font declared but unloaded.

## Connections
**Aesthetics:** [[aesthetics/portfolio|portfolio]] [[aesthetics/dark|dark]] [[aesthetics/light|light]]
**Patterns:** `personal-hub` [[patterns/portfolio|portfolio]] `author-site` `books-grid` `case-study-logos` `light-dark-bands` `oversized-display-type` [[patterns/system-fonts|system-fonts]] `section-index` `static-page` `link-rich`
**Category:** [[categories/personal|personal]]
**Tech:** `Static site (no JS framework)` [[tech/google-tag-manager|Google Tag Manager]] [[tech/google-analytics|Google Analytics]] `Cloudinary` [[tech/self-hosted|self-hosted]]
**Colors:** [[colors/dark|dark]] [[colors/light|light]] [[colors/monochrome|monochrome]] [[colors/cool|cool]]
**Fonts:** [[fonts/inter|Inter]]

## Related sites
[[sites/debarghyadas.com|debarghyadas.com]] [[sites/kmk0.com|kmk0.com]] [[sites/ryancarson.com|ryancarson.com]] [[sites/ankit-rai.com|ankit-rai.com]] [[sites/asekachov.com|asekachov.com]]
