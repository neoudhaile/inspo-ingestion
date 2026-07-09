---
url: https://www.thinkwithmark.com/
title: "The Smart Bookmark for Physical Books | Mark II"
category: product
aesthetics: [developer-product, luxury, editorial]
tags: [product-landing, scrollytelling, video-per-section, lifestyle-photography, warm-sepia, editorial-serif, email-capture-modal, press-logos, shopify-hydrogen, hardware-product]
extracted_at: 2026-06-06
---
# The Smart Bookmark for Physical Books | Mark II
> Bookmarks, reinvented.  ·  [thinkwithmark.com](https://www.thinkwithmark.com/)

![thinkwithmark.com](../../../screenshots/thinkwithmarkcom.png)

**What it is** — The product site for Mark II, a $159 AI “smart bookmark” — a physical bookmark-plus-scanner for paper books. Per the meta description it lets you “capture quotes and voice notes as you read” and “revisit them all in the Mark app,” under the hero line “Bookmarks, reinvented.” It's the Mark II launch (a $1M-funded follow-up to the earlier $129 Mark 1) by thinkwithmark, sold through a Shopify storefront.

**What it shows** — A long, cinematic product page built around video. The dark sepia hero shows the device resting in an open book beside “Bookmarks, reinvented” and a buy/learn CTA (plus a “Watch keynote” link to YouTube). Scrolling reveals chaptered sections its headings name — “An extension to your books,” “Do more with your notes,” “Quality you can feel,” and “Connect your knowledge / Migrate all your notes with a click of a button” — interleaving lifestyle photography of people reading with product/demo videos (8 <video>, 51 <img>). Press logos (Tom's Hardware, Gizmodo) lend credibility.

**How it works** — It reads as a scrollytelling product tour: section after section pairs a claim with motion (the 8 inline videos demo scanning a quote, recording a voice note, and the companion app). A newsletter/email-capture modal overlays the page on load (an .email-popup-backdrop that intercepts clicks until dismissed). Navigation is a slim top bar (How it works / Pricing / Blog / FAQ / Login) feeding a Shopify checkout, with the “Migrate all your notes with a click” section pitching import from other note apps. Outbound press and a keynote video reinforce the launch.

**How it's designed** — A warm, premium hardware aesthetic: a sepia/brown photographic hero with white headline text (h1 rendered rgb 255,255,255) giving way to an off-white body with deep near-black teal text (rendered rgb 13,27,30). The type is editorial-meets-techy — a 62px Copernicus serif for the big headings against Geist for UI/body (both genuinely loaded; Inter sits in the fallback stack). It's a Shopify build on the Hydrogen/Oxygen headless stack (assets served from cdn.shopify.com/oxygen-v2, favicon included), instrumented with Microsoft Clarity, Meta Pixel and Google Tag Manager. The craft signal is the video-per-section storytelling and large-format photography rather than UI chrome (only 6 svg). Exact section background colors are image/section-level rather than CSS tokens (:root exposes no custom props), so the sepia is asserted from the photography, not a DOM value.

**Palette** — Sepia/brown photographic hero with white headline text (rendered #fff); off-white body with deep near-black-teal text (rendered rgb 13/27/30). Section backgrounds are imagery, not CSS tokens.
**Fonts** — Copernicus serif for headings (62px), Geist for body/UI (both loaded); Inter in the fallback stack.

## Connections
**Aesthetics:** [[aesthetics/developer-product|developer-product]] [[aesthetics/luxury|luxury]] [[aesthetics/editorial|editorial]]
**Patterns:** [[patterns/product-landing|product-landing]] `scrollytelling` `video-per-section` `lifestyle-photography` `warm-sepia` [[patterns/editorial-serif|editorial-serif]] `email-capture-modal` `press-logos` `shopify-hydrogen` `hardware-product`
**Category:** [[categories/product|product]]
**Tech:** `Shopify (Hydrogen / Oxygen)` [[tech/microsoft-clarity|Microsoft Clarity]] [[tech/meta-pixel|Meta Pixel]] [[tech/google-tag-manager|Google Tag Manager]] [[tech/jsdelivr|jsDelivr]]
**Colors:** [[colors/cool|cool]]
**Fonts:** `Copernicus` [[fonts/geist|Geist]] `Geist 700/800`

## Related sites
[[sites/printingpress.dev|printingpress.dev]] [[sites/12matcha.com|12matcha.com]] [[sites/cofounder.co|cofounder.co]] [[sites/eko.lumaris.works|eko.lumaris.works]] [[sites/fantasypresidentcareer.com|fantasypresidentcareer.com]]
