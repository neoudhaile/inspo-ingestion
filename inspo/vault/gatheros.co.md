---
url: https://www.gatheros.co/
domain: gatheros.co
title: "GatherOS"
category: product
extracted_at: 2026-06-06
tags:
  - category/product
  - aesthetic/developer-product
  - aesthetic/light
  - pattern/product-landing
  - pattern/single-screen
  - pattern/app-preview
  - pattern/webflow
  - pattern/light-mode
  - pattern/mac-app
  - tech/webflow
  - tech/jquery
  - tech/cloudfront
  - tech/google-fonts
  - color/light
  - color/warm
  - font/geist
---
# GatherOS
> The Mac app for design inspiration. Capture, organize, and find every reference without leaving your desktop.  ·  [gatheros.co](https://www.gatheros.co/)

![gatheros.co](../../screenshots/gatherosco.png)

## What it is
The marketing landing page for GatherOS, a native macOS app (currently in beta) for collecting design inspiration, built by Brett of Designjoy. The single-line pitch is the real on-page h1: 'The Mac app for design inspiration.' — capture, organize and find every reference image or website without leaving your desktop.

## What it shows
A compact, single-screen pitch: the hero headline plus a polished preview of the app's own UI — a light, flat interface (its own CSS exposes a cream design-token system, --m-content-bg #FAFAF9, --m-text-primary #000) showing a saved reference with an auto-extracted palette, editable metadata and an AI 'Image Prompt'. The page leans on product screenshots (29 images) to sell the capture-and-organize workflow seen in the launch video.

## How it works
A standard Webflow one-pager: at 1440 it fits in a single viewport (scrollHeight 900), so the whole pitch is above the fold with a download/try CTA; on smaller screens it unfolds into a taller scrolling column. Interaction is minimal — it's a marketing page pointing to the downloadable Mac app, not the app itself.

## How it's designed
Light, calm and product-forward: a near-white body (rgb(246,246,246)) with pure-black text, so the colorful app screenshots carry the energy. Typography pairs Geist for UI/body copy with a 'Fg Culturetrial' display face for headlines (h1 38px, Geist). It's a Webflow build — the tell-tale webflow-icons font, jQuery and Webflow's CDN (d3e54v103j8qbb.cloudfront.net) — with fonts served from Google Fonts.

## Design data
- **Palette:** Warm off-white / near-white surfaces (#FAFAF9 app chrome, body rgb(246,246,246)), pure-black text (#000), muted grey for secondary text.
- **Palette tokens:** --m-content-bg (app surface): #FAFAF9 (var), --m-text-primary: #000 (var), --m-text-secondary: rgba(0,0,0,0.55) (var), --m-hover-bg: #EAEAEA (var), body background: rgb(246,246,246) (rendered), h1 color: rgb(0,0,0) (rendered)
- **Fonts:** Geist (UI/body), Fg Culturetrial (display headlines)
- **Fonts loaded:** Geist 400, Geist 500, Geist 600
- **Tech stack:** Webflow, jQuery, Cloudfront, Google Fonts
- **Media mix:** img 29 · svg 12
- **Page height:** 900px (single-screen: True)
- **Responsive:** At 390x844 the single-screen desktop layout stacks into one column and scrollHeight grows to ~2,450px; the hero copy and app preview reflow vertically (no hamburger menu detected).
- **Headings:** The Mac app for design inspiration.
- **Extracted:** 2026-06-06 · playwright-mcp @ 1440x900 (+ 390x844 mobile pass), logged_out: true

## Related sites
[[akira.sachi.dev]] [[conigma.com]] [[joonasvirtanen.com]] [[mo1.app]] [[shanemac.com]] [[anyblockers.com]]

## Tags
#category/product #aesthetic/developer-product #aesthetic/light #pattern/product-landing #pattern/single-screen #pattern/app-preview #pattern/webflow #pattern/light-mode #pattern/mac-app #tech/webflow #tech/jquery #tech/cloudfront #tech/google-fonts #color/light #color/warm #font/geist
