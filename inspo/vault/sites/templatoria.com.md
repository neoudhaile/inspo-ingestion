---
url: https://templatoria.com/
title: "Templatoria — Handcrafted Framer Templates Ready to Launch"
category: design
aesthetics: [minimal, light]
tags: [framer-template, marketplace, minimalist, monochrome, product-cards, pricing-tiers, light-grey, inter, mono-labels]
extracted_at: 2026-07-08
---
# Templatoria — Handcrafted Framer Templates Ready to Launch
> Handcrafted, launch-ready Framer templates designed for fast setup, easy customization, and real-world websites.  ·  [templatoria.com](https://templatoria.com/)

![templatoria.com](../../../screenshots/templatoriacom.png)

**What it is** — A Framer-template marketplace whose h1 pitch is simply 'Handcrafted, launch-ready Framer templates' and whose meta description reads 'Handcrafted, launch-ready Framer templates designed for fast setup, easy customization, and real-world websites.' It sells a curated set of ~9 templates; the Möbius® template the tweet's author (Anton Drukarov) is promoting is one of them.

**What it shows** — A hero of stacked template preview cards, then 'Featured templates.' — ClearPath, Möbius®, Firma and more, each ~$129 with 'More Info' and 'Live Preview' buttons — a pull-quote ('A great template should match the quality of real client work and adapt easily beyond its original niche.'), a 'From idea to live site. Fast.' three-step flow (Choose a template / Customize everything / Publish and go live) around a ring of colourful template thumbnails, a 'Flexible pricing.' block (Single $129 / Double $179 / All-Access Bundle $279), a 'What customers say.' testimonial row, a 'Let's clear things up!' FAQ and a dark footer (templatoria@gmail.com, Templates (9), Pricing, Blog, Support, Terms, Privacy).

**How it works** — Built entirely on Framer: the framework global is exposed and every asset is served from framerusercontent.com / events.framer.com, with stylesheet(s) pulled from unpkg.com. Analytics run through Datafast (datafa.st) and Google Tag Manager. It is a light, mostly-vector page — 8 <img>, 71 inline <svg>, 0 canvas/video and 1 <iframe> — over a long 11,033px scroll.

**How it's designed** — Deliberately near-monochrome so the colourful template thumbnails pop. getComputedStyle reports a light-grey body background rgb(242,242,242) with black body text and an h1 rendered near-black rgb(37,37,37); CTAs are solid black pills. Type pairs Inter and Inter Display (loaded 400/700) as the workhorse with an Aspekta Variable display face (loaded), and Fragment Mono is declared for the small mono labels though it reports unloaded on the homepage. No meaningful :root colour custom properties are exposed (only a --one-if-corner-shape-supported flag), so colours are read from the rendered page.

**Palette** — Light-grey canvas (#f2f2f2) with near-black text (#252525 / #000) and solid-black pill CTAs; saturation comes only from the colourful template thumbnails.
**Fonts** — Inter + Inter Display (loaded 400/700) for UI and display, Aspekta Variable (loaded) as a display face; Fragment Mono declared for mono labels but reporting unloaded on the homepage.

## Connections
**Aesthetics:** [[aesthetics/minimal|minimal]] [[aesthetics/light|light]]
**Patterns:** `framer-template` [[patterns/marketplace|marketplace]] [[patterns/minimalist|minimalist]] [[patterns/monochrome|monochrome]] `product-cards` `pricing-tiers` `light-grey` [[patterns/inter|inter]] [[patterns/mono-labels|mono-labels]]
**Category:** [[categories/design|design]]
**Tech:** [[tech/framer|Framer]] `Datafast Analytics` [[tech/google-tag-manager|Google Tag Manager]] [[tech/unpkg-css|unpkg (CSS)]]
**Colors:** [[colors/light|light]] [[colors/monochrome|monochrome]]
**Fonts:** [[fonts/inter|Inter]] [[fonts/inter-display|Inter Display]] `Aspekta Variable`

## Related sites
[[sites/asekachov.com|asekachov.com]] [[sites/daviskeene.com|daviskeene.com]] [[sites/designengineer.tools|designengineer.tools]] [[sites/drafts9.com|drafts9.com]] [[sites/hiivearts.com|hiivearts.com]]
