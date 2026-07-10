---
url: https://typatone.com/
domain: typatone.com
title: "Typatone — make music while you write"
category: uncategorized
extracted_at: 2026-07-05
tags:
  - category/uncategorized
  - aesthetic/minimal
  - aesthetic/experimental
  - pattern/generative-music
  - pattern/web-audio
  - pattern/interactive
  - pattern/minimalist
  - pattern/canvas
  - pattern/typography
  - pattern/monochrome
  - pattern/soft-sans
  - tech/vanilla-js-web-audio-api
  - tech/adobe-typekit
  - tech/google-tag-manager
  - color/monochrome
  - font/proxima-nova-soft
---
# Typatone — make music while you write
> The act of writing has always been an art. Now, it can also be an act of music.  ·  [typatone.com](https://typatone.com/)

![typatone.com](../../screenshots/typatonecom.png)

## What it is
Typatone — a minimalist interactive instrument where 'each letter you type corresponds to a specific musical note,' turning writing into generative melody (by Jono Brandel with Lullatone). It's the 'turns text into a generative melody' entry from Jonas's list.

## What it shows
A near-empty off-white page with a text field; as you type, each keystroke plays a soft synth note and spawns reactive typographic/particle visuals, composing an ambient tune from your words — which you can then share or download.

## How it works
Vanilla JS plus the Web Audio API driving two <canvas> layers (2 canvas, 0 img) for the reactive visuals; Adobe Typekit (use.typekit.net) serves the type and Google Tag Manager handles analytics. A fixed single-screen experience (scrollHeight 0).

## How it's designed
Serene, Muji-like minimalism. From getComputedStyle the canvas is light grey (body rgb(239,239,239)) with black text; the 'Typatone' wordmark renders 42px in Proxima Nova Soft (proxima-nova-soft via Typekit) in soft dark-grey rgb(51,51,51). The rounded geometric sans deliberately mirrors the gentle, rounded synth tones — the page stays monochrome so the generated sound and visuals carry the piece.

## Design data
- **Palette:** A light-grey paper (rgb(239,239,239)) with near-black text and soft dark-grey headings (rgb(51,51,51)) — deliberately monochrome.
- **Palette tokens:** body background: rgb(239, 239, 239) (rendered), body text: rgb(0, 0, 0) (rendered), h1 color: rgb(51, 51, 51) (rendered)
- **Fonts:** Proxima Nova Soft (a rounded geometric sans, via Adobe Typekit) for the wordmark and UI.
- **Fonts loaded:** Proxima Nova Soft 400
- **Tech stack:** Vanilla JS + Web Audio API, Adobe Typekit, Google Tag Manager
- **Media mix:** canvas 2 · iframe 3
- **Page height:** 900px (single-screen: True)
- **Responsive:** At 390x844 it stays a single-screen instrument (scrollHeight 0) with the two canvas layers intact; the typing/visual field simply scales to the narrower width.
- **Headings:** Typatone
- **Extracted:** 2026-07-05 · Playwright MCP, 1440x900 + 390x844 mobile pass, logged_out: true

## Related sites
[[asekachov.com]] [[daviskeene.com]] [[designengineer.tools]] [[hiivearts.com]] [[humanoid-index.com]] [[nicolasbustamante.com]]

## Tags
#category/uncategorized #aesthetic/minimal #aesthetic/experimental #pattern/generative-music #pattern/web-audio #pattern/interactive #pattern/minimalist #pattern/canvas #pattern/typography #pattern/monochrome #pattern/soft-sans #tech/vanilla-js-web-audio-api #tech/adobe-typekit #tech/google-tag-manager #color/monochrome #font/proxima-nova-soft
