---
url: https://templatoria.com/
domain: templatoria.com
title: "Templatoria — Handcrafted Framer Templates Ready to Launch"
category: design
extracted_at: 2026-07-08
tags:
  - category/design
  - aesthetic/minimal
  - aesthetic/light
  - pattern/framer-template
  - pattern/marketplace
  - pattern/minimalist
  - pattern/monochrome
  - pattern/product-cards
  - pattern/pricing-tiers
  - pattern/light-grey
  - pattern/inter
  - pattern/mono-labels
  - tech/framer
  - tech/datafast-analytics
  - tech/google-tag-manager
  - tech/unpkg-css
  - color/light
  - color/monochrome
  - font/inter
  - font/inter-display
  - font/aspekta-variable
---
# Templatoria — Handcrafted Framer Templates Ready to Launch
> Handcrafted, launch-ready Framer templates designed for fast setup, easy customization, and real-world websites.  ·  [templatoria.com](https://templatoria.com/)

![templatoria.com](../../screenshots/templatoriacom.png)

## What it is
A Framer-template marketplace whose h1 pitch is simply 'Handcrafted, launch-ready Framer templates' and whose meta description reads 'Handcrafted, launch-ready Framer templates designed for fast setup, easy customization, and real-world websites.' It sells a curated set of ~9 templates; the Möbius® template the tweet's author (Anton Drukarov) is promoting is one of them.

## What it shows
A hero of stacked template preview cards, then 'Featured templates.' — ClearPath, Möbius®, Firma and more, each ~$129 with 'More Info' and 'Live Preview' buttons — a pull-quote ('A great template should match the quality of real client work and adapt easily beyond its original niche.'), a 'From idea to live site. Fast.' three-step flow (Choose a template / Customize everything / Publish and go live) around a ring of colourful template thumbnails, a 'Flexible pricing.' block (Single $129 / Double $179 / All-Access Bundle $279), a 'What customers say.' testimonial row, a 'Let's clear things up!' FAQ and a dark footer (templatoria@gmail.com, Templates (9), Pricing, Blog, Support, Terms, Privacy).

## How it works
Built entirely on Framer: the framework global is exposed and every asset is served from framerusercontent.com / events.framer.com, with stylesheet(s) pulled from unpkg.com. Analytics run through Datafast (datafa.st) and Google Tag Manager. It is a light, mostly-vector page — 8 <img>, 71 inline <svg>, 0 canvas/video and 1 <iframe> — over a long 11,033px scroll.

## How it's designed
Deliberately near-monochrome so the colourful template thumbnails pop. getComputedStyle reports a light-grey body background rgb(242,242,242) with black body text and an h1 rendered near-black rgb(37,37,37); CTAs are solid black pills. Type pairs Inter and Inter Display (loaded 400/700) as the workhorse with an Aspekta Variable display face (loaded), and Fragment Mono is declared for the small mono labels though it reports unloaded on the homepage. No meaningful :root colour custom properties are exposed (only a --one-if-corner-shape-supported flag), so colours are read from the rendered page.

## Design data
- **Palette:** Light-grey canvas (#f2f2f2) with near-black text (#252525 / #000) and solid-black pill CTAs; saturation comes only from the colourful template thumbnails.
- **Palette tokens:** body background: rgb(242, 242, 242) (rendered), body text: rgb(0, 0, 0) (rendered), h1: rgb(37, 37, 37) (rendered)
- **Fonts:** Inter + Inter Display (loaded 400/700) for UI and display, Aspekta Variable (loaded) as a display face; Fragment Mono declared for mono labels but reporting unloaded on the homepage.
- **Fonts loaded:** Inter 400, Inter 700, Inter Display 700, Aspekta Variable 400, Aspekta Variable 1000
- **Tech stack:** Framer, Datafast Analytics, Google Tag Manager, unpkg (CSS)
- **Media mix:** img 8 · svg 71 · iframe 1
- **Page height:** 11033px (single-screen: False)
- **Responsive:** At 390x844 the desktop nav collapses and the multi-column template/pricing grid reflows to a single stacked column (scrollHeight 11,033 -> 12,544px).
- **Headings:** Handcrafted, launch-ready Framer templates / Featured templates. / From idea to live site. Fast. / Flexible pricing. / What customers say. / Let's clear things up!
- **Weight:** None requests; hosts: templatoria.com, framerusercontent.com, events.framer.com, datafa.st, www.googletagmanager.com, unpkg.com
- **Extracted:** 2026-07-08 · Playwright MCP, 1440x900 fullPage + 390x844 mobile probe; logged_out: true. A scroll-triggered newsletter popup was hidden via the DOM before the full-page capture.

## Related sites
[[asekachov.com]] [[daviskeene.com]] [[designengineer.tools]] [[drafts9.com]] [[hiivearts.com]] [[humanoid-index.com]]

## Tags
#category/design #aesthetic/minimal #aesthetic/light #pattern/framer-template #pattern/marketplace #pattern/minimalist #pattern/monochrome #pattern/product-cards #pattern/pricing-tiers #pattern/light-grey #pattern/inter #pattern/mono-labels #tech/framer #tech/datafast-analytics #tech/google-tag-manager #tech/unpkg-css #color/light #color/monochrome #font/inter #font/inter-display #font/aspekta-variable
