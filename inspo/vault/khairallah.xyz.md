---
url: https://khairallah.xyz/
domain: khairallah.xyz
title: "Khairallah AL-Awady"
vertical: portfolio
mode: dark
vibe: [minimal, technical]
topics: [engineering]
extracted_at: 2026-06-06
tags:
  - vertical/portfolio
  - vibe/minimal
  - vibe/technical
  - topic/engineering
  - mode/dark
---
# Khairallah AL-Awady
> Hi, I'm Khairallah. I've been building software and digital products for years across blockchain, web3, and AI.  ·  [khairallah.xyz](https://khairallah.xyz/)

![khairallah.xyz](../../screenshots/khairallahxyz.png)

**Vertical:** #vertical/portfolio  ·  **Vibe:** #vibe/minimal #vibe/technical  ·  **Topics:** #topic/engineering  ·  **Mode:** #mode/dark

## What it is
A single-page personal site / résumé for Khairallah AL-Awady, a blockchain/web3/AI developer (founder of web3arabs.com), built as a quiet text-first identity card rather than a marketing page.

## What it shows
An anime-style avatar and a short intro bio at top, a top-right link cluster (github, x, articles, linkedin, email), then two link-dense columns: 'Clients and employers' (Starknet, EigenCloud, Web3Arabs, PWR Labs, QuickNode, QuillAudits, Nahmii, Livepeer, WeaveDB) and 'Current tech interests' (a reading-list of repos and docs — Maestro, EigenCloud, deer-flow, GitNexus, Starknet, OpenClaw, stwo, Aave, btczee, React Native, Bun, Anthropic).

## How it works
A fully self-hosted static page — every script and stylesheet comes from khairallah.xyz itself, with no analytics, no framework runtime (no Next/Nuxt/Vue/Svelte globals) and only a single image and one inline SVG. The whole thing fits in ~2k px on desktop.

## How it's designed
Terminal-minimalist: a flat dark-gray rgb(33,33,33) canvas with light-gray rgb(217,217,217) text, set entirely in JetBrains Mono (400 the only loaded weight). The stylesheet is a Tailwind build (token vars like --background, --foreground, --muted-foreground, --radius, --font-mono-stack present as HSL custom properties); links sit in near-white rgb(235,235,234) with no decorative color, keeping everything monochrome and document-like.

## Design data
- **Palette:** Dark-gray #212121 (rendered rgb(33,33,33)) background, light-gray text, near-white links — fully monochrome
- **Palette tokens:** body background: rgb(33, 33, 33) (rendered), body text: rgb(217, 217, 217) (rendered), link/accent: rgb(235, 235, 234) (rendered), --background: 0 0% 13% (var), --foreground: 0 0% 85% (var), --muted-foreground: 0 0% 55% (var), --radius: .5rem (var)
- **Fonts:** JetBrains Mono 400 (mono stack); no other webfont loaded
- **Fonts loaded:** JetBrains Mono 400
- **Tech stack:** Tailwind CSS, self-hosted static, no analytics
- **Keywords:** minimalist, monospace, dark-mode, personal-card, tailwind, link-list, web3
- **Media mix:** img 1 · svg 1
- **Page height:** 2022px (single-screen: False)
- **Responsive:** At 390×844 the two columns reflow into a single stacked column and the page grows to ~3k px; layout is otherwise unchanged.
- **Headings:** Clients and employers / Current tech interests
- **Links out:** [github](https://github.com/KhairallahA) · [x](https://x.com/eng_khairallah1) · [linkedin](https://linkedin.com/in/khairallah-w3a) · [email](mailto:khairallah@web3arabs.com)
- **Extracted:** 2026-06-06 · Playwright Chromium @ 1440×900 + 390×844 mobile pass; logged_out: true

## Related sites
- [[lab01.dev]] — shared: portfolio, minimal, technical, engineering, dark
- [[siddz.com]] — shared: portfolio, minimal, technical, engineering
- [[spyrosigma.in]] — shared: portfolio, minimal, technical, engineering
- [[nyk.dev]] — shared: portfolio, technical, engineering, dark
- [[objectives.md]] — shared: portfolio, minimal, technical, dark
- [[addyosmani.com]] — shared: portfolio, minimal, engineering
