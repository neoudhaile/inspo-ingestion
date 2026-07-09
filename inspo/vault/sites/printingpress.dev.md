---
url: https://printingpress.dev/
title: "Printing Press — agent-native CLIs from a single prompt"
category: tutorial
aesthetics: [developer-product, editorial]
tags: [product-landing, developer-tool, open-source, warm-cream, editorial-serif, serif-mono-pairing, single-scroll, agents, mcp, tailwind-v4]
extracted_at: 2026-06-06
---
# Printing Press — agent-native CLIs from a single prompt
> Welcome to the Printing Press. Print an agent-native CLI for any API, app, or site — from a single prompt.  ·  [printingpress.dev](https://printingpress.dev/)

![printingpress.dev](../../../screenshots/printingpressdev.png)

**What it is** — Printing Press (printingpress.dev) is the landing page for an open-source project by Matt Van Horn (@mvanhorn) and Trevin Chow (@trevin). The pitch, per its meta: “From an API spec, a website with no public API, or a community fan project — one command prints a Go CLI, a Claude Code skill, an OpenClaw skill, and an MCP server. Muscle memory for agents.” It fronts two GitHub repos — cli-printing-press (PressCLI, ★2.9k) and printing-press-library (Public Library, ★1.4k) — and is the subject of Garry Tan's tweet (“My OpenClaw/Hermes Agent setup just got way smarter”).

**What it shows** — A warm cream page (rendered/var background rgb 244,239,230) led by a Newsreader serif h1 at 60px in near-black ink (rgb 27,24,22): “Welcome to the Printing Press. Print an agent-native CLI for any API, app, or site — from a single prompt. Or install one the community already made.” Two section heads carry the concept: “Every API has a secret identity.” and “The Library.” It's deliberately text/diagram-forward — just 1 img and 30 svg — and even links a live claude.ai/share conversation as a worked example.

**How it works** — A compact single-scroll explainer (~7487px) that routes to the two GitHub repos and a public Library of community-made CLIs, plus an “Open conversation →” link to a Claude transcript. It's self-hosted with no third-party analytics scripts detected — a lean, developer-audience page.

**How it's designed** — An editorial, literary “printing press” aesthetic on warm cream #f4efe6 (var --color-ink-black #1b1816, --color-ink-mute #5a524a for body). The type pairing is the whole idea: Newsreader serif for headlines (60px h1) against Geist sans for body and Geist Mono for the CLI/code snippets — print-meets-terminal. It's a Tailwind v4 build (lab() tokens, lightningcss; purple/pink accent ramps via --color-purple-500/--color-pink-500 and a green --color-ink-green #1f6b3a). The /opengraph-image and /icon.svg metadata routes point to a Next.js app-router setup on Vercel (no __NEXT_DATA__ exposed, so inferred).

**Palette** — Warm cream #f4efe6 (var bg rgb 244/239/230) with near-black ink (rendered rgb 27/24/22, var --color-ink-black #1b1816) and muted-brown body (--color-ink-mute #5a524a); purple/pink token ramps plus a green --color-ink-green #1f6b3a.
**Fonts** — Newsreader serif for headlines (h1 60px), Geist sans for body, Geist Mono for CLI/code (all loaded).

## Connections
**Aesthetics:** [[aesthetics/developer-product|developer-product]] [[aesthetics/editorial|editorial]]
**Patterns:** [[patterns/product-landing|product-landing]] [[patterns/developer-tool|developer-tool]] [[patterns/open-source|open-source]] `warm-cream` [[patterns/editorial-serif|editorial-serif]] `serif-mono-pairing` [[patterns/single-scroll|single-scroll]] `agents` `mcp` [[patterns/tailwind-v4|tailwind-v4]]
**Category:** [[categories/tutorial|tutorial]]
**Tech:** `Next.js (App Router)` [[tech/tailwind-v4|Tailwind v4]] [[tech/vercel|Vercel]]
**Colors:** [[colors/warm|warm]] [[colors/cool|cool]]
**Fonts:** [[fonts/newsreader|Newsreader]] [[fonts/geist|Geist]] [[fonts/geist-mono|Geist Mono]]

## Related sites
[[sites/cofounder.co|cofounder.co]] [[sites/hofai.io|hofai.io]] [[sites/todesktop.com|todesktop.com]] [[sites/itshover.com|itshover.com]] [[sites/patterncraft.fun|patterncraft.fun]]
