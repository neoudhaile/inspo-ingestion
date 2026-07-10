---
url: https://objectives.md/
domain: objectives.md
title: "Andrew Jiang"
category: product
extracted_at: 2026-06-06
tags:
  - category/product
  - aesthetic/dark
  - aesthetic/minimal
  - aesthetic/developer-product
  - aesthetic/portfolio
  - pattern/dark
  - pattern/markdown
  - pattern/developer
  - pattern/terminal-window
  - pattern/minimalist
  - pattern/monospace
  - pattern/portfolio
  - tech/next-js
  - tech/inter-jetbrains-mono-next-font
  - color/dark
  - color/cool
  - font/inter-100-900
  - font/jetbrains-mono-100-800
---
# Andrew Jiang
> # Objectives  ·  [objectives.md](https://objectives.md/)

![objectives.md](../../screenshots/objectivesmd.png)

## What it is
The personal site of builder/investor Andrew Jiang (YC alum, GP at Curated), and the page the 'Palantir for Family Trips' tweet links to. It styles his whole résumé as a raw Markdown document — the <h1> is literally '# Objectives'.

## What it shows
A single dark 'editor window' (with macOS traffic-light dots and an 'objectives.md' filename) rendering a Markdown CV: ## About (name + bio), ## Work (LockIn, Curated), ## Projects (Gifted.art, BotPreview, Paper Pong, LockIn Pitch, CV Studio), and ## Open Source — where 'Palantir for Family Trips' links out to its GitHub repo. Section markers like '## WORK' are shown verbatim as the design motif.

## How it works
A self-hosted Next.js page (og image served from the /opengraph-image route convention; Inter Fallback / JetBrains Mono Fallback names are next/font's generated fallbacks). All scripts and styles come from objectives.md itself; project names are plain outbound <a> links.

## How it's designed
Dev-tool aesthetic driven by explicit CSS vars: near-black --bg #030303 with a slightly lighter --window #0a0a0a card, off-white --text-primary #f5f5f5, muted --text-secondary #a0a0a0, a green --accent #22c55e and blue --link #3b82f6, hairline --border #1a1a1a. Body copy is Inter, with JetBrains Mono for the monospaced 'filename' and markdown-syntax accents — leaning into the 'a life as a .md file' concept. Image-free (0 imgs, 4 SVGs for the social icons).

## Design data
- **Palette:** Near-black #030303 canvas, off-white #f5f5f5 text, green #22c55e accent, blue #3b82f6 links
- **Palette tokens:** --bg: #030303 (var), --window: #0a0a0a (var), --text-primary: #f5f5f5 (var), --text-secondary: #a0a0a0 (var), --accent: #22c55e (var), --link: #3b82f6 (var), --border: #1a1a1a (var)
- **Fonts:** Inter for prose, JetBrains Mono for code/markdown syntax — self-hosted via next/font
- **Fonts loaded:** Inter 100-900, JetBrains Mono 100-800
- **Tech stack:** Next.js, Inter + JetBrains Mono (next/font)
- **Media mix:** svg 4
- **Page height:** 1052px (single-screen: False)
- **Responsive:** At 390×844 the window/list reflows to a single narrow column, growing from ~1,052px to ~1,455px.
- **Headings:** # Objectives / ## About / ## Work / ## Projects / ## Open Source
- **Links out:** [Palantir for Family Trips](https://github.com/andrewjiang/palantir-for-family-trips) · [LockIn](https://www.heylockin.com/) · [Curated](https://curated.xyz/) · [Gifted.art](https://gifted.art/) · [X](https://x.com/andrewjiang) · [GitHub](https://github.com/andrewjiang)
- **Weight:** None requests; hosts: objectives.md
- **Extracted:** 2026-06-06 · Playwright 1440x900 + 390x844 mobile pass, logged_out: true

## Related sites
[[siddz.com]] [[lab01.dev]] [[ankit-rai.com]] [[asekachov.com]] [[christophlocher.com]] [[hex.inc]]

## Tags
#category/product #aesthetic/dark #aesthetic/minimal #aesthetic/developer-product #aesthetic/portfolio #pattern/dark #pattern/markdown #pattern/developer #pattern/terminal-window #pattern/minimalist #pattern/monospace #pattern/portfolio #tech/next-js #tech/inter-jetbrains-mono-next-font #color/dark #color/cool #font/inter-100-900 #font/jetbrains-mono-100-800
