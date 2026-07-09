---
url: https://transitions.dev/
title: "Transitions.dev — Essential transitions for web apps"
category: uncategorized
aesthetics: [light, developer-product, minimal]
tags: [copy-paste, ui-transitions, micro-interactions, interactive-demos, css-variables, light-mode, developer-tool, minimal]
extracted_at: 2026-06-05
---
# Transitions.dev — Essential transitions for web apps
> Collection of the most essential transitions for web apps that you can just copy and paste into any project.  ·  [transitions.dev](https://transitions.dev/)

![transitions.dev](../../../screenshots/transitionsdev.png)

**What it is** — A free copy-paste library of essential UI transitions for web apps by Jakub Antalik (@jakubantalik) — the site the tweet is actually showcasing. The h1 is simply 'Transitions'.

**What it shows** — A grid of interactive demos where each card runs a live micro-interaction — modals, dropdowns, sliding panels, an error shake, skeleton shimmer, staggered list reveals, tab switches — that you can copy as CSS. Roughly 18 named recipes are encoded directly in the stylesheet (--p1 … --p18). It also promotes Emil Kowalski's animations.dev course.

**How it works** — A single light page (~2,764px) of self-contained demos. Each transition is parameterized by a block of CSS custom properties (--p1-* … --p18-*: durations, cubic-bezier eases, distances, blur, bounce) so the exact values are readable and copyable. It is deliberately lightweight — GoatCounter analytics (gc.zgo.at), Google Fonts, and no JS framework.

**How it's designed** — Clean, near-white editorial UI (--bg #fdfdfd, --text #0d0d0d) sitting on a soft grey card/stage system (--card-bg #ffffff, --stage-bg #f9f9f9, --chip-bg #f4f4f4), with Inter for UI text and Roboto Mono (--font-mono) for the code and labels. Fifty inline SVG icons label the demos. The chrome is intentionally quiet so the motion is the content; the only saturated colour is an error-red (#e23014) reserved for the shake/error demo.

**Palette** — Near-white ground (--bg #fdfdfd), near-black text (--text #0d0d0d), soft grey cards/chips (#f9f9f9 / #f4f4f4); monochrome by design, with an error-red (#e23014) reserved for the shake demo.
**Fonts** — Inter (UI sans) + Roboto Mono (code/labels), both loaded from Google Fonts.

## Connections
**Aesthetics:** [[aesthetics/light|light]] [[aesthetics/developer-product|developer-product]] [[aesthetics/minimal|minimal]]
**Patterns:** `copy-paste` `ui-transitions` `micro-interactions` `interactive-demos` `css-variables` [[patterns/light-mode|light-mode]] [[patterns/developer-tool|developer-tool]] [[patterns/minimal|minimal]]
**Category:** [[categories/uncategorized|uncategorized]]
**Tech:** `vanilla (no JS framework)` `GoatCounter` [[tech/google-fonts|Google Fonts]]
**Colors:** [[colors/light|light]] [[colors/monochrome|monochrome]]
**Fonts:** [[fonts/inter|Inter]] [[fonts/roboto-mono|Roboto Mono]]

## Related sites
[[sites/patterncraft.fun|patterncraft.fun]] [[sites/akira.sachi.dev|akira.sachi.dev]] [[sites/sensory-ui.com|sensory-ui.com]] [[sites/animations.dev|animations.dev]] [[sites/anyblockers.com|anyblockers.com]]
