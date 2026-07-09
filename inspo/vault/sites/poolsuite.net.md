---
url: https://poolsuite.net/
title: "Now Playing on Poolsuite ☼: Poolsuite ON AIR"
category: favorites
aesthetics: [retro, playful]
tags: [web-radio, retro-desktop-os, vaporwave, pixel-fonts, single-screen, skeuomorphic, summer-aesthetic, vue]
extracted_at: 2026-06-06
---
# Now Playing on Poolsuite ☼: Poolsuite ON AIR
> The ultra-summer internet radio station, playing an infinity pool of summer sounds 24/7. Swimwear optional. Formerly Poolside FM.  ·  [poolsuite.net](https://poolsuite.net/)

![poolsuite.net](../../../screenshots/poolsuitenet.png)

**What it is** — Poolsuite (formerly Poolside FM) is an 'ultra-summer' internet radio station wrapped in a faux vintage-computer desktop. There's no <h1> — the conceit is the interface itself: a pastel retro operating system you 'boot into' to listen to a 24/7 stream of summer/yacht-rock sounds, with the meta description bragging 'an infinity pool of summer sounds 24/7. Swimwear optional.' The audience is the nostalgia-web / vaporwave crowd and the brand has since spun into a lifestyle label (Vacation, Inc. sunscreen, membership perks).

**What it shows** — A single, fixed, non-scrolling screen (exactly 900px tall, no body scroll) styled as a 1990s desktop dated 'SAT 6 JUN 1997'. Centered is a media player window — 'Poolsuite: ON AIR' currently spinning 'Po-one - Steady Glide' — surrounded by draggable app windows and desktop icons: Newsroom, Guestbook, Mixtapes, Members, Events, Vacation Inc, Member Perks, Profile, Settings, 'Submit a track', 'Become a member', plus a little 'HayesJarvis.mpeg' video thumbnail and an Instagram panel.

**How it works** — A Vue single-page app (the root carries data-v-app) rendering a windowed desktop metaphor on one fixed screen. Audio/video is handled through an embedded YouTube IFrame-API player (the page's single iframe, script host www.youtube.com). Plausible handles privacy-friendly analytics and a Facebook pixel (connect.facebook.net) covers marketing; the page also bundles a WalletConnect / Web3Modal stack (hundreds of --apkt-* / --w3m-* CSS tokens) for its members/crypto-tinged features.

**How it's designed** — Full pixel-art nostalgia. The loaded faces are bitmap/retro display fonts — Pixolde (400 & 700) does most of the work, alongside ChiKareGo2, Ishmeria and Everyday — so every label looks like old system chrome (the global default stack is otherwise ui-sans-serif). The palette is declared in CSS vars as soft poolside pastels: --primary #f7d5d5 (rose), --secondary #faf1e8 (cream), --tertiary #faf5c6 (pale lemon), --button #f6d6d5 and a mint --secondary-button #afe5dd; rendered, the html sits on cream rgb(249,239,228) and the body on rose rgb(246,213,213). It's image-dense (125 imgs, 33 inline SVGs) to sell the skeuomorphic desktop.

**Palette** — Poolside pastels — rose #f7d5d5, cream #faf1e8, pale-lemon #faf5c6, mint #afe5dd — on cream/rose grounds (html rgb(249,239,228), body rgb(246,213,213)).
**Fonts** — Pixel/bitmap display faces — Pixolde (400 & 700) plus ChiKareGo2, Ishmeria and Everyday — self-hosted from poolsuite.net.

## Connections
**Aesthetics:** [[aesthetics/retro|retro]] [[aesthetics/playful|playful]]
**Patterns:** `web-radio` `retro-desktop-os` `vaporwave` `pixel-fonts` [[patterns/single-screen|single-screen]] `skeuomorphic` `summer-aesthetic` `vue`
**Category:** [[categories/favorites|favorites]]
**Tech:** `Vue` `YouTube IFrame API` [[tech/plausible|Plausible]] [[tech/facebook-pixel|Facebook Pixel]] `WalletConnect / Web3Modal`
**Colors:** [[colors/warm|warm]] [[colors/cool|cool]]
**Fonts:** `Pixolde` `ChiKareGo2` `Ishmeria` `Everyday`

## Related sites
[[sites/akira.sachi.dev|akira.sachi.dev]] [[sites/axiaisacat.indiehacker.bio|axiaisacat.indiehacker.bio]] [[sites/bird.onethreenine.net|bird.onethreenine.net]] [[sites/cafe.endofday.studio|cafe.endofday.studio]] [[sites/chusmargallo.space|chusmargallo.space]]
