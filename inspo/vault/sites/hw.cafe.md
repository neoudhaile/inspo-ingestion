---
url: https://hw.cafe/
title: "Hello World Cafe — New York's First 24/7 Cafe for Builders"
category: design
aesthetics: [developer-product, dark, editorial]
tags: [terminal-aesthetic, monospace-ui, ascii-art, single-page-landing, anchor-nav, waitlist-funnel, dark-theme, serif-display-contrast, web3-walletconnect, self-hosted]
extracted_at: 2026-06-06
---
# Hello World Cafe — New York's First 24/7 Cafe for Builders
> >_ hello world  ·  [hw.cafe](https://hw.cafe/)

![hw.cafe](../../../screenshots/hwcafe.png)

**What it is** — The launch/waitlist site for Hello World Cafe (hw.cafe), pitched in the meta as "A 24/7, mostly-automated coffee shop for builders in NYC. Gigabit wifi, power at every seat, proper chairs, and a door that doesn't close." Its h1 is the literal terminal prompt ">_ hello world".

**What it shows** — A terminal-themed one-pager: a fake zsh status bar ("hwc.boot — zsh — 80x24", "$ ./status --founding", an ASCII progress bar showing founding_200 "all claimed"), then narrative sections from the h2s — "100 builders said yes in 24 hours. then it happened again." (the_signal), "the founding 200." (a member wall), "everything you need. nothing you don't." (amenities), "save your spot in line." (join), and "questions, answered." (faq). Contact is daniel@hw.cafe with X (@hw_cafe_nyc) and a github org.

**How it works** — Long single-scroll landing (~7,950px) with an anchor nav styled as file paths (// the_signal, // the_200, // amenities, // faq) jumping to in-page sections; the core CTA is "join the waitlist / save my spot". It carries a wallet-connect layer (RainbowKit CSS variables present), hinting at a token/membership or web3-gated reservation, though the founding 200 are already claimed and the funnel is now the waitlist. Self-hosted — every script and stylesheet is served from hw.cafe itself, with no third-party analytics detected.

**How it's designed** — Full developer-terminal aesthetic done with taste: an almost-black #0a0d12 background, JetBrains Mono as the body typeface, and a phosphor-green accent (#4ade80) for the primary buttons and status glyphs, with amber/gold (#e8b765 / #d8a93e) as secondary signal colors. The twist is the oversized Fraunces serif display (h1 at 92px, light weight 300) playing against the monospace UI — code-meets-editorial. A tight CSS-variable design system (--bg/--panel/--line/--ink/--body/--dim ladder) keeps the dark palette layered and intentional.

**Palette** — Near-black canvas (#0a0d12) with phosphor-green accent (#4ade80) and amber/gold secondaries (#e8b765 / #d8a93e); off-white ink (#eef2f6), muted blue-grey body text (rgb(174,185,197))
**Fonts** — JetBrains Mono (monospace) for body/UI; Fraunces (serif) for oversized display headings

## Connections
**Aesthetics:** [[aesthetics/developer-product|developer-product]] [[aesthetics/dark|dark]] [[aesthetics/editorial|editorial]]
**Patterns:** [[patterns/terminal-aesthetic|terminal-aesthetic]] [[patterns/monospace-ui|monospace-ui]] `ascii-art` `single-page-landing` `anchor-nav` `waitlist-funnel` [[patterns/dark-theme|dark-theme]] `serif-display-contrast` `web3-walletconnect` [[patterns/self-hosted|self-hosted]]
**Category:** [[categories/design|design]]
**Tech:** `self-hosted (all assets from hw.cafe)` `RainbowKit/wallet-connect` `Lightning CSS` [[tech/no-third-party-analytics-detected|no third-party analytics detected]]
**Colors:** [[colors/dark|dark]] [[colors/warm|warm]] [[colors/cool|cool]]
**Fonts:** `JetBrains Mono 400/500/700` `Fraunces 300/400`

## Related sites
[[sites/colf.dev|colf.dev]] [[sites/affiliatenetwork.com|affiliatenetwork.com]] [[sites/ashpreetbedi.com|ashpreetbedi.com]] [[sites/backdoorai.app|backdoorai.app]] [[sites/bigplayers.co|bigplayers.co]]
