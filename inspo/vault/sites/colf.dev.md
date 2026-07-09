---
url: https://colf.dev/
title: "Colf"
category: uncategorized
aesthetics: [light, developer-product, playful]
tags: [light-mode, monospace-ui, pixel-font, terminal-aesthetic, leaderboard, data-table, gamified, tool-app, tailwind]
extracted_at: 2026-06-05
---
# Colf
> Prompt solutions to algorithmic problems with the fewest tokens.  ·  [colf.dev](https://colf.dev/)

![colf.dev](../../../screenshots/colfdev.png)

**What it is** — A browser game from Eric Zakariasson (who works on Cursor) that mashes up LeetCode, code golf and prompting: "Colf is like combining leetcode, code golf and prompting. Your task is to prompt your way to the shortest solution to a given set of code challenges." You don't write the code — you write the prompt that makes a model emit it, and the fewer tokens you spend (prompt + output) the higher you rank.

**What it shows** — A light, single-column page. Up top the title "Colf" and the one-line pitch sit above a two-pane challenge card (a Prompt box on the left holding a sample task — "Reverse string using split/reverse/join; name function rev(s)." — and a Code/output pane on the right) with Input / Output / Tries counters (13 / 17 / 38) and a "Start challenge" button. Below it the whole rest of the page is a "Leaderboard" — a Top 100 table of ranked players with avatars and columns for challenges solved, input/output token counts and totals.

**How it works** — It's a real tool, not a marketing page: pick a challenge, type a prompt, the model returns code, and you're scored on total tokens used. A persistent top nav (Home / Challenges / Leaderboard / Profile) plus a Twitter/Cursor footer frame the experience. The long leaderboard is the main draw below the fold — a live ranking that turns prompt-efficiency into a competitive sport.

**How it's designed** — Confident retro-terminal look done in a light theme: white background (#fff), near-black text (#171717), tidy neutral-gray Tailwind scale, and a single blue focus ring (#3b82f6). The signature move is typography — the entire UI is set in DepartureMono, a pixel/typewriter monospace, which makes a dense data table and a code game read as one coherent "terminal" artifact. Tailwind v4 tokens (oklch color scale) drive the spacing and color system.

**Palette** — White bg (#fff), near-black text (#171717), neutral Tailwind grays, muted accent (#f3f4f6), blue focus ring (#3b82f6), light border (#d4d4d4).
**Fonts** — DepartureMono (pixel monospace) for everything; Arial/Helvetica fallback.

## Connections
**Aesthetics:** [[aesthetics/light|light]] [[aesthetics/developer-product|developer-product]] [[aesthetics/playful|playful]]
**Patterns:** [[patterns/light-mode|light-mode]] [[patterns/monospace-ui|monospace-ui]] `pixel-font` [[patterns/terminal-aesthetic|terminal-aesthetic]] `leaderboard` `data-table` `gamified` `tool-app` [[patterns/tailwind|tailwind]]
**Category:** [[categories/uncategorized|uncategorized]]
**Tech:** `Next.js (inferred from /opengraph-image route)` [[tech/tailwind-css-v4|Tailwind CSS v4]] `DepartureMono (self-hosted)`
**Colors:** [[colors/light|light]] [[colors/cool|cool]]
**Fonts:** `DepartureMono`

## Related sites
[[sites/ditther.com|ditther.com]] [[sites/hw.cafe|hw.cafe]] [[sites/akira.sachi.dev|akira.sachi.dev]] [[sites/anyblockers.com|anyblockers.com]] [[sites/ashpreetbedi.com|ashpreetbedi.com]]
