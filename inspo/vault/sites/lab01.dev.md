---
url: https://lab01.dev/
title: "Lab01 - Sebastiano Guerriero's portfolio"
category: design
aesthetics: [portfolio, dark, developer-product, minimal]
tags: [experiments-lab, portfolio, dark, monospace, geist-mono, iframe-demos, ui-experiments, minimal]
extracted_at: 2026-07-08
---
# Lab01 - Sebastiano Guerriero's portfolio
> Lab01 by Sebastiano Guerriero — a portfolio/lab of live front-end UI experiments (derived from the h1; the page ships no meta description).  ·  [lab01.dev](https://lab01.dev/)

![lab01.dev](../../../screenshots/lab01dev.png)

**What it is** — Sebastiano Guerriero's experiments lab and the home of the tweet's demo. The h1 reads 'Lab01 by Sebastiano Guerriero'; the page ships no meta description. It is a running index of numbered front-end UI experiments (the drag-to-collapse sidebar is one of them).

**What it shows** — A dark, terminal-flavoured single page listing 'UI Experiment #01' through '#12' (plus a 'The Founder Package' section), each mounted as a live embedded demo via <iframe> (9 iframes), with a few inline SVG marks (15) and images (3).

**How it works** — A static, framework-less site served from lab01.dev (no __NEXT_DATA__/React/Nuxt/Svelte globals present), instrumented lightly with Umami (cloud.umami.is) and Cloudflare Web Analytics. Each experiment is isolated in its own iframe so the interactions run independently.

**How it's designed** — A monochrome dark 'lab' aesthetic driven by a single monospace typeface. getComputedStyle reports a near-black body background rgb(10,10,10) with off-white text (white at 80% opacity), and the whole page — h1 included — set in the variable 'Geist Mono' (100–900). Interactive buttons are dark-grey chips rgb(38,38,38). No :root colour tokens are published; the palette is essentially black / off-white / grey.

**Palette** — Near-black canvas rgb(10,10,10) with off-white text (white @ 80%) and dark-grey button chips rgb(38,38,38) — a strict monochrome lab look.
**Fonts** — One typeface everywhere: the variable monospace 'Geist Mono' (100–900), including headings.

## Connections
**Aesthetics:** [[aesthetics/portfolio|portfolio]] [[aesthetics/dark|dark]] [[aesthetics/developer-product|developer-product]] [[aesthetics/minimal|minimal]]
**Patterns:** `experiments-lab` [[patterns/portfolio|portfolio]] [[patterns/dark|dark]] [[patterns/monospace|monospace]] `geist-mono` `iframe-demos` `ui-experiments` [[patterns/minimal|minimal]]
**Category:** [[categories/design|design]]
**Tech:** `Static site (no meta-framework global)` `Umami analytics` `Cloudflare (Web Analytics + CDN)`
**Colors:** [[colors/dark|dark]] [[colors/monochrome|monochrome]]
**Fonts:** [[fonts/geist-mono-variable-100-900|Geist Mono (variable 100-900)]]

## Related sites
[[sites/objectives.md|objectives.md]] [[sites/ankit-rai.com|ankit-rai.com]] [[sites/hex.inc|hex.inc]] [[sites/jasonyuan.design|jasonyuan.design]] [[sites/killedbyopenai.com|killedbyopenai.com]]
