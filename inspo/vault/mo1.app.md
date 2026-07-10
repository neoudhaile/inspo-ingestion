---
url: https://mo1.app/
domain: mo1.app
title: "mo¹"
category: product
extracted_at: 2026-06-05
tags:
  - category/product
  - aesthetic/developer-product
  - aesthetic/playful
  - aesthetic/light
  - pattern/product-landing
  - pattern/single-screen
  - pattern/hero-demo-video
  - pattern/interactive-mock
  - pattern/sidebar-cta
  - pattern/playful
  - pattern/system-fonts
  - pattern/orange-highlight
  - pattern/beta
  - tech/nuxt-vue
  - tech/cloudflare-insights
  - tech/desktop-fm-analytics-e-dkp-fm
  - color/light
  - color/warm
  - font/system-fonts
---
# mo¹
> like after effects, but it's fun  ·  [mo1.app](https://mo1.app/)

![mo1.app](../../screenshots/mo1app.png)

## What it is
The landing page for mo¹ (mo1), a browser-based motion-graphics app pitched as 'like after effects, but it's fun.' It is in beta 0.1, made by xavier (jack) — the tweet's author, @KMkota0 — under the desktop.fm umbrella.

## What it shows
A hero with a live mock of the editor (a keyframe timeline, an 'add audio' CD element, a camera/transform module) and three pitch columns: 'no easings, just vibes', 'camera motion, simplified', 'crazy modules, extra delight', each with a one-line note about the philosophy. A left sidebar carries the app icon (beta 0.1), 'a new way to create epic animations', a 'learn more' link and 'try it out!' / 'log in' buttons.

## How it works
A single full-viewport screen (no scroll at desktop; scrollHeight == innerHeight == 900) with one <video> demoing the editor in motion. The primary CTA ('try it out!') opens the app; 'log in' is for returning users. Footer credits xavier (jack) / desktop.fm and links to socials.

## How it's designed
Light, Apple-ish and playful: a cream/white ground with a soft warm-peach radial gradient behind the editor mock, solid black pill buttons, and a single orange highlight (#fe9024) reserved for the punchy phrases ('but it's fun', 'just vibes', 'simplified', 'delight'). Type is SF Pro (system sans) with EB Garamond as a serif accent — and notably it ships no webfont payload at all (document.fonts is empty), leaning entirely on system fonts.

## Design data
- **Palette:** Cream/white ground with a warm peach gradient panel, black text and black pill buttons, orange highlight (#fe9024).
- **Palette tokens:** --highlight-color: #fe9024 (var), --accent: #666 (var), button background (rendered): rgb(0,0,0) (rendered), button text (rendered): rgb(255,255,255) (rendered), body text (rendered): rgb(0,0,0) (rendered)
- **Fonts:** SF Pro (system sans, primary) + EB Garamond (serif accent) — system-only, no webfont payload.
- **Fonts loaded:** system only (no webfont)
- **Tech stack:** Nuxt / Vue, Cloudflare (insights), desktop.fm analytics (e.dkp.fm)
- **Media mix:** img 7 · video 1 · svg 5
- **Page height:** 900px (single-screen: True)
- **Responsive:** At 390x844 the sidebar stacks above the hero and the three feature columns collapse into a single column; the single screen becomes scrollable (~1,744px).
- **Headings:** like after effects, but it's fun / no easings, just vibes. / camera motion, simplified. / crazy modules, extra delight.
- **Links out:** [x.com/KMkota0](https://x.com/KMkota0) · [instagram](https://www.instagram.com/kmkota0/) · [desktop.fm](https://desktop.fm/) · [email](mailto:xavier@desktop.fm) · [terms and privacy](https://mo1.app/terms-privacy)
- **Extracted:** 2026-06-05 · playwright-mcp @ 1440x900 (fullPage) + mobile 390x844

## Related sites
[[kmk0.com]] [[bird.onethreenine.net]] [[daryl.cv]] [[gatheros.co]] [[addyosmani.com]] [[akira.sachi.dev]]

## Tags
#category/product #aesthetic/developer-product #aesthetic/playful #aesthetic/light #pattern/product-landing #pattern/single-screen #pattern/hero-demo-video #pattern/interactive-mock #pattern/sidebar-cta #pattern/playful #pattern/system-fonts #pattern/orange-highlight #pattern/beta #tech/nuxt-vue #tech/cloudflare-insights #tech/desktop-fm-analytics-e-dkp-fm #color/light #color/warm #font/system-fonts
