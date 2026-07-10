---
url: https://www.gatheros.co/
domain: gatheros.co
title: "GatherOS"
vertical: startup-product
mode: light
vibe: [corporate-clean, minimal]
topics: [design, productivity]
extracted_at: 2026-06-06
tags:
  - vertical/startup-product
  - vibe/corporate-clean
  - vibe/minimal
  - topic/design
  - topic/productivity
  - mode/light
---
# GatherOS
> The Mac app for design inspiration. Capture, organize, and find every reference without leaving your desktop.  ·  [gatheros.co](https://www.gatheros.co/)

![gatheros.co](../../screenshots/gatherosco.png)

**Vertical:** #vertical/startup-product  ·  **Vibe:** #vibe/corporate-clean #vibe/minimal  ·  **Topics:** #topic/design #topic/productivity  ·  **Mode:** #mode/light

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
- **Keywords:** product-landing, single-screen, app-preview, webflow, light-mode, mac-app
- **Media mix:** img 29 · svg 12
- **Page height:** 900px (single-screen: True)
- **Responsive:** At 390x844 the single-screen desktop layout stacks into one column and scrollHeight grows to ~2,450px; the hero copy and app preview reflow vertically (no hamburger menu detected).
- **Headings:** The Mac app for design inspiration.
- **Extracted:** 2026-06-06 · playwright-mcp @ 1440x900 (+ 390x844 mobile pass), logged_out: true

## Related sites
- [[flowstate.com]] — shared: startup-product, corporate-clean, minimal, productivity
- [[apps.ankiweb.net]] — shared: startup-product, minimal, productivity, light
- [[mo1.app]] — shared: startup-product, minimal, design, light
- [[simple.ink]] — shared: startup-product, corporate-clean, productivity, light
- [[vercel.com]] — shared: startup-product, corporate-clean, minimal, light
- [[drafts9.com]] — shared: corporate-clean, minimal, design, light
