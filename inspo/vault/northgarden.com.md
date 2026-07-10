---
url: https://www.northgarden.com/about
domain: northgarden.com
title: "About — NorthGarden"
category: design
extracted_at: 2026-06-06
tags:
  - category/design
  - aesthetic/portfolio
  - aesthetic/minimal
  - aesthetic/experimental
  - pattern/studio-portfolio
  - pattern/minimalist
  - pattern/monochrome
  - pattern/threejs-canvas
  - pattern/webgl-wordmark
  - pattern/grotesk-mono-pairing
  - pattern/single-page
  - pattern/self-hosted
  - pattern/nextjs
  - pattern/tailwind
  - tech/next-js-app-router-hashed-opengraph-image-favicon-routes
  - tech/three-js-r180-animated-wordmark-canvas
  - tech/tailwind-css
  - tech/self-hosted-assets-all-from-northgarden-com
  - tech/no-third-party-analytics-detected
  - color/monochrome
  - font/ft-system-grotesk-400-600
  - font/ft-system-mono
---
# About — NorthGarden
> NorthGarden is a design and development studio that specializes in creating digital products, websites, and interactive experiences used by millions around the world.  ·  [northgarden.com](https://www.northgarden.com/about)

![northgarden.com](../../screenshots/northgardencom.png)

## What it is
The About page of NorthGarden (northgarden.com), a self-described "design and development studio creating digital products, websites, and interactive experiences for industry-leading artists, brands, and studios." The wordmark itself is the hero: an animated Three.js (r180) canvas renders a black ink-brush garden scene with the letters of "NorthGarden" set into it.

## What it shows
A minimalist black-on-white studio page. A file-path-style top nav (N logo, WORK / ABOUT / CONTACT in monospace) sits above the illustrated wordmark, followed by a two-paragraph statement of purpose ("...used by millions around the world" / "Our work brings together thoughtful design, precise engineering, and creative technology..."), then the h2 sections "Trusted by" (client logos) and "What we build". A full-bleed contact CTA anchors the foot, with Instagram, X (@northgardenstu) and LinkedIn (@northgardenstudio) as the outbound links.

## How it works
A short single-scroll page (~2,850px). The signature element is a WebGL canvas (data-engine="three.js r180") animating the ink-garden wordmark; the rest is static editorial layout. Everything is self-hosted — every script and stylesheet is served from northgarden.com, with no third-party analytics detected. The hashed /opengraph-image.png and /favicon.ico routes point to a Next.js App Router build, styled with Tailwind utility classes (font-grotesk, font-mono, text-neutral-*).

## How it's designed
Pure monochrome restraint: a #fff background and #000 foreground driven by two CSS variables (--background / --foreground), with neutral greys (text-neutral-500) for the muted nav. Type does the work — the bespoke FT System Grotesk carries the headline copy while FT System Mono (300) handles the nav and labels, a grotesk/mono pairing that reads like a design tool's own UI. The hand-drawn Three.js garden is the only ornament, and the only color, in an otherwise pristine black-and-white frame.

## Design data
- **Palette:** Pure black ink (#000) on white (#fff), with neutral mid-greys for secondary nav text; the only imagery is a black ink-brush garden illustration
- **Palette tokens:** --background: #fff (var), --foreground: #000 (var), body-color: rgb(0, 0, 0) (rendered), body-bg: rgb(255, 255, 255) (rendered), nav-muted: rgb(115, 115, 115) (rendered)
- **Fonts:** FT System Grotesk (400/600) for headings and body; FT System Mono (300) for nav and labels — both self-hosted webfonts
- **Fonts loaded:** FT System Grotesk 400/600, FT System Mono 300
- **Tech stack:** Next.js (App Router — hashed /opengraph-image + /favicon routes), Three.js r180 (animated wordmark canvas), Tailwind CSS, self-hosted assets (all from northgarden.com), no third-party analytics detected
- **Media mix:** img 2 · canvas 1 · svg 8
- **Page height:** 2847px (single-screen: False)
- **Responsive:** At 390x844 the page reflows to a single column (~3,017px tall) with the intro paragraph at ~24px; the WORK/ABOUT/CONTACT nav stays inline rather than collapsing to a hamburger.
- **Headings:** Trusted by / What we build
- **Links out:** [instagram](https://instagram.com/northgardenstudio) · [twitter / x](https://x.com/northgardenstu) · [linkedin](https://linkedin.com/company/northgardenstudio)
- **Weight:** None requests; hosts: www.northgarden.com
- **Extracted:** 2026-06-06 · Playwright MCP, 1440x900 + 390x844 mobile pass, logged_out: true

## Related sites
[[designengineer.tools]] [[humanoid-index.com]] [[asekachov.com]] [[ashpreetbedi.com]] [[christophlocher.com]] [[daviskeene.com]]

## Tags
#category/design #aesthetic/portfolio #aesthetic/minimal #aesthetic/experimental #pattern/studio-portfolio #pattern/minimalist #pattern/monochrome #pattern/threejs-canvas #pattern/webgl-wordmark #pattern/grotesk-mono-pairing #pattern/single-page #pattern/self-hosted #pattern/nextjs #pattern/tailwind #tech/next-js-app-router-hashed-opengraph-image-favicon-routes #tech/three-js-r180-animated-wordmark-canvas #tech/tailwind-css #tech/self-hosted-assets-all-from-northgarden-com #tech/no-third-party-analytics-detected #color/monochrome #font/ft-system-grotesk-400-600 #font/ft-system-mono
