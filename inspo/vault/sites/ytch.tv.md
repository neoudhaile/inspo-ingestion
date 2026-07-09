---
url: https://ytch.tv/
title: "YTCH"
category: uncategorized
aesthetics: [retro, developer-product, dark]
tags: [web-toy, retro-tv, crt-aesthetic, channel-zapping, youtube-iframe-api, skeuomorphic-remote, keyboard-driven, single-screen, monospace, dark-mode]
extracted_at: 2026-06-06
---
# YTCH
> If Youtube had actual channels.  ·  [ytch.tv](https://ytch.tv/)

![ytch.tv](../../../screenshots/ytchxyz.png)

**What it is** — A playful web toy that reimagines YouTube as broadcast television. Instead of an algorithmic feed you 'tune' to numbered channels (CH 01, CH 02…) of curated videos and flip between them with an on-screen remote — the whole conceit, per the meta description, is 'If Youtube had actual channels.' Reached via ytch.xyz, which redirects to ytch.tv.

**What it shows** — A single full-black screen. Centered is a video frame currently playing a YouTube clip ('Why is Gen Z so Poor?'); a glowing green monospace 'CH 01' channel readout sits top-left like a cable-box overlay. Bottom-right is a skeuomorphic remote control with a 0–9 numeric keypad and power/record-style buttons. Small chrome at the bottom reads 'COPY URL', 'More videos', and a YouTube logo.

**How it works** — One fixed, non-scrolling screen (exactly 900px, no body scroll). The clip is an embedded YouTube IFrame-API player (script host www.youtube.com, the page's single iframe); the number keys / remote keypad switch channels, and 'COPY URL' shares the current channel. Google Tag Manager and the Cloudflare insights beacon are the only other scripts.

**How it's designed** — A pure retro-terminal aesthetic. Black ground (rgb(0,0,0)) with IBM Plex Mono (500 and 700, loaded from Google Fonts) for everything, and the channel readout in a vivid CRT green (rgb(0,255,34)) that deliberately evokes an old cable box / tuner display; the 'COPY URL' label is plain white. No SVG and no canvas — the UI is built from 14 raster sprites (the remote, buttons) plus the one video iframe. It's deliberately minimal, single-screen and keyboard-driven, all atmosphere and interaction rather than content layout.

**Palette** — Black ground (#000), vivid CRT green channel readout (rgb(0,255,34)), white secondary text — high-contrast retro tuner look.
**Fonts** — IBM Plex Mono (500 & 700), loaded via Google Fonts.

## Connections
**Aesthetics:** [[aesthetics/retro|retro]] [[aesthetics/developer-product|developer-product]] [[aesthetics/dark|dark]]
**Patterns:** `web-toy` `retro-tv` `crt-aesthetic` `channel-zapping` `youtube-iframe-api` `skeuomorphic-remote` `keyboard-driven` [[patterns/single-screen|single-screen]] [[patterns/monospace|monospace]] [[patterns/dark-mode|dark-mode]]
**Category:** [[categories/uncategorized|uncategorized]]
**Tech:** `YouTube IFrame API` [[tech/google-tag-manager|Google Tag Manager]] [[tech/cloudflare-insights|Cloudflare (insights)]]
**Colors:** [[colors/dark|dark]] [[colors/cool|cool]]
**Fonts:** [[fonts/ibm-plex-mono|IBM Plex Mono]]

## Related sites
[[sites/akira.sachi.dev|akira.sachi.dev]] [[sites/davekrugman.com|davekrugman.com]] [[sites/khairallah.xyz|khairallah.xyz]] [[sites/killedbyopenai.com|killedbyopenai.com]] [[sites/axiaisacat.indiehacker.bio|axiaisacat.indiehacker.bio]]
