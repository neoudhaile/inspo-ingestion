---
url: https://eko.lumaris.works/
domain: eko.lumaris.works
title: "Eko — tiny tasks done in seconds (Mac shortcut app)"
category: uncategorized
extracted_at: 2026-07-05
tags:
  - category/uncategorized
  - aesthetic/dark
  - aesthetic/editorial
  - aesthetic/developer-product
  - pattern/dark
  - pattern/serif-display
  - pattern/playfair
  - pattern/editorial
  - pattern/product-landing
  - pattern/tailwind
  - pattern/react
  - pattern/one-time-pricing
  - tech/react
  - tech/tailwind-css
  - tech/google-fonts
  - tech/posthog
  - tech/google-tag-manager
  - tech/cloudflare
  - color/dark
  - color/cool
  - font/inter
  - font/playfair-display
---
# Eko — tiny tasks done in seconds (Mac shortcut app)
> All the tiny tasks that eat your day, done in seconds.  ·  [eko.lumaris.works](https://eko.lumaris.works/)

![eko.lumaris.works](../../screenshots/ekolumarisworks.png)

## What it is
Eko is a $39 one-time Mac utility that dictates, translates, fixes and rewrites text 'in any app, from one shortcut.' It's the second site in the tweet, shared alongside Contra Labs for sharing the same classical-serif 'renaissance' aesthetic.

## What it shows
A long dark landing page: the hero 'All the tiny tasks that eat your day, done in seconds.', a problem framing ('You write for 20 hours every week.' → 'What if all of that took 2 seconds?'), a 'See Eko in action' demo video, an 'A shortcut for everything' feature block, a privacy section ('Your data, your choice'), one-time pricing ('$39 — once, forever'), an FAQ, and a closing 'Save hours every day. Never write a typo again.'

## How it works
A React single-page app (React root detected) styled with Tailwind (--tw-* utility tokens on :root) and Google-Fonts CSS. It carries one product-demo <video>, 45 inline SVG icons and 3 images, and runs a privacy-first-plus-advertising analytics stack: PostHog (us-assets.i.posthog.com), Google Tag Manager, and Cloudflare Insights.

## How it's designed
Dark, high-contrast editorial. From the DOM the body background is pure black (rgb(0,0,0)) with white text (rgb(255,255,255)). The display face is Playfair Display — the h1 renders 60px/500 in 'Playfair Display', serif — with Cormorant SC also declared for classical flourish, set against Inter (weights 200–800 loaded) for body and UI. A Didone serif on black is exactly what reads as the 'renaissance vibe.' The one non-neutral token is Tailwind's default blue focus ring (--tw-ring-color rgb(59 130 246 / .5)).

## Design data
- **Palette:** Pure-black background (rgb(0,0,0)) with white text; Tailwind default-blue focus ring (rgb(59 130 246)) as the only chromatic accent.
- **Palette tokens:** body background: rgb(0, 0, 0) (rendered), body color: rgb(255, 255, 255) (rendered), --tw-ring-color: rgb(59 130 246 / .5) (var), h1 color (light section): rgb(24, 24, 27) (rendered)
- **Fonts:** Playfair Display (Didone display serif, the 'renaissance' headline face) plus Cormorant SC declared, paired with Inter 200–800 for body and UI.
- **Fonts loaded:** Inter 200, Inter 300, Inter 400, Inter 600, Inter 800, Playfair Display 400, Playfair Display 500
- **Tech stack:** React, Tailwind CSS, Google Fonts, PostHog, Google Tag Manager, Cloudflare
- **Media mix:** img 3 · video 1 · svg 45
- **Page height:** 14787px (single-screen: False)
- **Responsive:** At 390x844 the top nav collapses behind a hamburger (Shortcuts/Pricing/FAQ links hidden), the hero h1 scales from 60px to 36px, and the page reflows to a single column (~15,860px tall).
- **Headings:** All the tiny tasks that eat your day, done in seconds. / You write for 20 hours every week. / What if all of that took 2 seconds? / See Eko in action / A shortcut for everything / Your data, your choice / $39 — once, forever / Frequently asked questions / Save hours every day. Never write a typo again.
- **Extracted:** 2026-07-05 · Playwright MCP, 1440x900 + 390x844 mobile pass, logged_out: true

## Related sites
[[21st.dev]] [[contralabs.com]] [[fantasypresidentcareer.com]] [[joonasvirtanen.com]] [[ryancarson.com]] [[sinceerly.com]]

## Tags
#category/uncategorized #aesthetic/dark #aesthetic/editorial #aesthetic/developer-product #pattern/dark #pattern/serif-display #pattern/playfair #pattern/editorial #pattern/product-landing #pattern/tailwind #pattern/react #pattern/one-time-pricing #tech/react #tech/tailwind-css #tech/google-fonts #tech/posthog #tech/google-tag-manager #tech/cloudflare #color/dark #color/cool #font/inter #font/playfair-display
