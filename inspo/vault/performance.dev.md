---
url: https://performance.dev
domain: performance.dev
title: "Performance"
vertical: personal-blog
mode: light
vibe: [editorial, minimal]
topics: [engineering]
extracted_at: 2026-06-06
tags:
  - vertical/personal-blog
  - vibe/editorial
  - vibe/minimal
  - topic/engineering
  - mode/light
---
# Performance
> Essays on building fast, beautiful web apps and the craft behind them.  ·  [performance.dev](https://performance.dev)

![performance.dev](../../screenshots/performancedev.png)

**Vertical:** #vertical/personal-blog  ·  **Vibe:** #vibe/editorial #vibe/minimal  ·  **Topics:** #topic/engineering  ·  **Mode:** #mode/light

## What it is
Dennis Brotzky's personal essay blog about web performance craft — the companion site to the Fey performance thread. The meta description is the mission statement: "Essays on building fast, beautiful web apps and the craft behind them." (The page has no <h1>; the description carries the pitch.)

## What it shows
A spare, light editorial index listing essays as large rounded preview cards — currently "The Conductor Rewrite: What They Changed to Make It Fast" (Jun 1, 2026) and "How's Linear so fast? A technical breakdown" (May 3, 2026) — each card showing a styled hero graphic. A footer pitches a no-spam email subscription and credits Dennis Brotzky (linked to x.com/brotzky).

## How it works
No JS framework was detected (no Next/Nuxt/Vue/Svelte/React roots or globals) — it behaves as a static/hand-built site. The only third-party script is Cloudflare's cloudflareinsights analytics beacon; everything else, including the custom 'Performance Sans' and 'Performance Serif' webfonts, is served from performance.dev.

## How it's designed
Light, print-like editorial: an off-white canvas (rgb(252,252,252)) with near-black ink text (rgb(43,47,41)) and a single dark-navy pill CTA (bg rgb(10,13,26), white label). It rides on an unusually elaborate CSS-variable design system for such a small site: a custom serif/sans pairing, a tiny UI type scale (--fs-body 11px up to --fs-xl 14px) alongside an 18px reading size, squircle card corners (--squircle-shape superellipse(1.6), 38px radius), layered media shadows (--shadow-media), a 720px --content-width measure and glass-blur tokens. The result reads like a meticulously typeset magazine column.

## Design data
- **Palette:** Off-white paper, near-black ink, a single dark-navy pill CTA.
- **Palette tokens:** body-bg: rgb(252, 252, 252) (rendered), body-text: rgb(43, 47, 41) (rendered), button-bg: rgb(10, 13, 26) (rendered), button-text: rgb(255, 255, 255) (rendered), --content-width: 720px (var), --squircle-radius: 38px (var)
- **Fonts:** Custom 'Performance Sans' (400/600) for body/UI and 'Performance Serif' (400) for prose, with a system mono fallback; self-hosted.
- **Fonts loaded:** Performance Sans 400, Performance Sans 600, Performance Serif 400
- **Tech stack:** No JS framework detected (static/hand-built), Cloudflare (cloudflareinsights analytics), self-hosted fonts
- **Keywords:** editorial, blog-index, light-theme, squircle-cards, custom-typeface, design-tokens, minimalist, performance-craft
- **Media mix:** img 3 · svg 3
- **Page height:** 1768px (single-screen: False)
- **Responsive:** At 390x844 the single 720px content column simply narrows and the page shortens (1,768px to 1,260px); it is already single-column so there is no layout-mode change or hamburger.
- **Headings:** The Conductor Rewrite:What They Changed to Make It Fast / How's Linear so fast? A technical breakdown
- **Links out:** [Skills](https://performance.dev/skills) · [Dennis Brotzky](https://x.com/brotzky)
- **Extracted:** 2026-06-06 · Playwright Chromium, 1440x900 desktop + 390x844 mobile pass; logged_out: true

## Related sites
- [[anyblockers.com]] — shared: personal-blog, editorial, minimal, engineering, light
- [[amanml.com]] — shared: personal-blog, minimal, engineering, light
- [[emilkowal.ski]] — shared: personal-blog, minimal, engineering, light
- [[rvivek.com]] — shared: personal-blog, editorial, minimal, light
- [[21st.dev]] — shared: editorial, minimal, engineering, light
- [[animations.dev]] — shared: editorial, minimal, engineering, light
