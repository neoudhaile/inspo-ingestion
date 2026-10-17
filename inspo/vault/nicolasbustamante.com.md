---
url: https://nicolasbustamante.com/
domain: nicolasbustamante.com
title: "Nicolas Bustamante — AI Entrepreneur"
vertical: personal-blog
mode: light
vibe: [minimal, technical]
topics: [ai, startups]
extracted_at: 2026-06-06
tags:
  - vertical/personal-blog
  - vibe/minimal
  - vibe/technical
  - topic/ai
  - topic/startups
  - mode/light
---
# Nicolas Bustamante — AI Entrepreneur
> AI Entrepreneur  ·  [nicolasbustamante.com](https://nicolasbustamante.com/)

![nicolasbustamante.com](../../screenshots/nicolasbustamantecom.png)

**Vertical:** #vertical/personal-blog  ·  **Vibe:** #vibe/minimal #vibe/technical  ·  **Topics:** #topic/ai #topic/startups  ·  **Mode:** #mode/light

## What it is
The minimal personal site and blog of Nicolas Bustamante, a serial founder (Doctrine; Fintool, acquired by Microsoft) who now writes prolifically about building AI agents.

## What it shows
A single narrow text column, no imagery at all. An 'About' intro, then a long 'Writings' index of agent-engineering essays ('Long Running Agent Engineering', 'Agent Memory Engineering', 'Model-Harness-Fit', 'Microsoft Has Acquired Fintool', 'Are LLMs Plateauing? No. You Are.'), and a 'Recommendations' section (Paris, San Francisco, Parenting hacks).

## How it works
A plain read-top-to-bottom homepage; everything is a text link into a blog post or a recommendation page. No animation, no media, no interactive chrome beyond the links.

## How it's designed
Ultra-minimal developer-blog aesthetic built on the Geist typeface and a shadcn/ui design-token system. It renders in light mode by default (white #fcfcfc ground, black text) while carrying a full dark theme in CSS variables (--background #0a0a0a / --foreground #fafafa). Zero images (img:0) — the content is the design.

## Design data
- **Palette:** Renders light by default — near-white ground (rgb(252,252,252)) with black text; a complete dark theme is defined in tokens (#0a0a0a ground / #fafafa text), with a coral destructive (#ff6568) and a blue (#1447e6) accent.
- **Palette tokens:** --background: #0a0a0a (var), --foreground: #fafafa (var), --primary: #e5e5e5 (var), --muted-foreground: #a1a1a1 (var), --destructive: #ff6568 (var), --sidebar-primary: #1447e6 (var), body-bg-rendered: rgb(252, 252, 252) (rendered), body-text-rendered: rgb(0, 0, 0) (rendered)
- **Fonts:** Geist (body/UI) + Geist Mono
- **Fonts loaded:** Geist 100-900, Geist Mono 100-900
- **Tech stack:** Next.js (Geist font), shadcn/ui, self-hosted
- **Keywords:** minimalist, text-first, personal-homepage, blog-index, shadcn, geist, dark-mode-ready, single-column, monochrome
- **Media mix:** svg 2
- **Page height:** 1198px (single-screen: False)
- **Responsive:** Already a single narrow column; at 390px it simply reflows taller (~1,198 → ~1,475px) with no horizontal scroll.
- **Headings:** About / Writings / Recommendations
- **Links out:** [Doctrine](https://doctrine.com/) · [Fintool](https://fintool.com/)
- **Extracted:** 2026-06-06 · playwright-mcp @ 1440x900 (+390x844 mobile), logged_out: true

## Related sites
- [[amanml.com]] — shared: personal-blog, minimal, ai, light
- [[emilkowal.ski]] — shared: personal-blog, minimal, ai, light
- [[richzou.com]] — shared: personal-blog, minimal, startups, light
- [[ashpreetbedi.com]] — shared: personal-blog, technical, ai
- [[backdoorai.app]] — shared: minimal, ai, startups, light
- [[canivibecodeit.com]] — shared: technical, ai, startups, light
