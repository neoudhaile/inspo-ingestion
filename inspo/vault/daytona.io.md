---
url: https://www.daytona.io/
domain: daytona.io
title: "Daytona - Secure Infrastructure for Running AI-Generated Code"
category: personal
extracted_at: 2026-06-06
tags:
  - category/personal
  - aesthetic/dark
  - aesthetic/developer-product
  - pattern/dark-mode
  - pattern/developer-tool
  - pattern/framer
  - pattern/terminal-aesthetic
  - pattern/long-scroll-landing
  - pattern/code-accent-green
  - tech/framer
  - tech/google-tag-manager
  - tech/zeroclick-ai
  - color/dark
  - color/cool
  - font/inter-variable
  - font/inter
  - font/berkeley-mono-regular
  - font/ibm-plex-mono
---
# Daytona - Secure Infrastructure for Running AI-Generated Code
> Run AI Code on Daytona  ·  [daytona.io](https://www.daytona.io/)

![daytona.io](../../screenshots/daytonaio.png)

## What it is
Daytona is a developer-infrastructure product that gives AI agents secure, disposable sandboxes to execute the code they generate. The hero pitch is literally its own <h1>: "Run AI Code on Daytona", and the meta description sells the headline numbers — 90ms environment creation, stateful operations, and enterprise-grade security.

## What it shows
A long (11.5k px) marketing landing page: a dark hero with the run-AI-code promise, then stacked sections of product capabilities, code/terminal mockups, logos and stats, leading toward sign-up CTAs. There's a single embedded iframe and heavy use of inline SVG (226) and product imagery (97 images) to illustrate the sandbox/infra story.

## How it works
It's a Framer-built static marketing site (assets served from framerusercontent.com, framer events script present). No app framework like Next/Nuxt — the page is Framer's renderer. GTM and a zeroclick.ai script handle analytics/attribution.

## How it's designed
A near-black developer aesthetic: page background is rgb(10,10,10) with white headings, accented by a terminal green (#2ecc71) reserved for code text and a blue (#0080ff / #59acff) for interactive accents — all read from the site's own design tokens. Type is set in Inter Variable for UI with Berkeley Mono and IBM Plex Mono for code, reinforcing the infra/terminal feel. Letter-spacing is tightened (-0.02em) for a dense, technical headline look.

## Design data
- **Palette:** Near-black canvas (#0a0a0a) + white text, terminal-green (#2ecc71) code accent, electric blue (#0080ff/#59acff) interactive accent.
- **Palette tokens:** --token (near-black bg): #0a0a0a (var), --token (surface): #161616 (var), --token (green accent): #2ecc71 (var), --token (blue accent): #0080ff (var), --token (blue accent light): #59acff (var), body_bg (rendered): rgb(10, 10, 10) (rendered), h1_color (rendered): rgb(255, 255, 255) (rendered)
- **Fonts:** Inter Variable (UI) + Berkeley Mono & IBM Plex Mono (code).
- **Fonts loaded:** Inter Variable 400, Inter 400, Inter 700, Inter 500, Inter 600, Berkeley Mono Regular 400, IBM Plex Mono 400
- **Tech stack:** Framer, Google Tag Manager, zeroclick.ai
- **Media mix:** img 97 · svg 226 · iframe 1
- **Page height:** 11486px (single-screen: False)
- **Responsive:** At 390px the layout stacks into a single column (scrollHeight grows from ~11.5k to ~19k px); the header nav stays flex with no hamburger toggle.
- **Headings:** Run AI Code on Daytona
- **Extracted:** 2026-06-06 · Playwright 1440x900 + 390x844, logged_out: true

## Related sites
[[backgrounds.supply]] [[crustdata.com]] [[affiliatenetwork.com]] [[akira.sachi.dev]] [[ankit-rai.com]] [[asekachov.com]]

## Tags
#category/personal #aesthetic/dark #aesthetic/developer-product #pattern/dark-mode #pattern/developer-tool #pattern/framer #pattern/terminal-aesthetic #pattern/long-scroll-landing #pattern/code-accent-green #tech/framer #tech/google-tag-manager #tech/zeroclick-ai #color/dark #color/cool #font/inter-variable #font/inter #font/berkeley-mono-regular #font/ibm-plex-mono
