---
url: https://www.shanemac.com/
title: "Shane Mac"
category: personal
aesthetics: [minimal]
tags: [personal-landing, minimalist, single-screen, webflow, signature-logo, text-nav, centered]
extracted_at: 2026-06-06
---
# Shane Mac
> Hi, I'm Shane Mac.  ·  [shanemac.com](https://www.shanemac.com/)

![shanemac.com](../../../screenshots/shanemaccom.png)

**What it is** — The personal landing page of Shane Mac, a founder & CEO who — per the site's own meta description — is 'building XMTP, a decentralized messaging protocol.' It is a single-screen Webflow page that acts as a hub linking out to his About, Writing, and News. Notably it does NOT link the @openclaw agent product the tweet is about, so the showcased product has no resolvable site.

**What it shows** — A centered hand-drawn 'SM' signature mark, the H1 'Hi, I'm Shane Mac.', a three-item text nav (About, Writing, News), and a pair of small email and Twitter icons — nothing else.

**How it works** — A pure static Webflow page with no JS framework; jQuery (from googleapis) and Google Tag Manager are the only scripts, fonts come from Google Fonts and assets from a Webflow Cloudfront CDN. Everything fits one viewport (scrollHeight 900px == innerHeight), and each nav item routes to a subpage.

**How it's designed** — Minimal, white-canvas, document-like. White background (rgb(255,255,255)), near-black ink (rgb(26,27,31)), and Montserrat (plus Montserrat Alternates) loaded across the full 100-900 weight range; the H1 is a 30px bold Montserrat. The only imagery is the signature mark and two social glyphs — there is no accent color at all, and links simply inherit the near-black ink. CSS exposes just two custom props, --white and --black.

**Palette** — White canvas, near-black text and links, no accent color.
**Fonts** — Montserrat (and Montserrat Alternates) self-loaded via Google Fonts across weights 100-900; H1 in 30px Montserrat.

## Connections
**Aesthetics:** [[aesthetics/minimal|minimal]]
**Patterns:** `personal-landing` [[patterns/minimalist|minimalist]] [[patterns/single-screen|single-screen]] [[patterns/webflow|webflow]] `signature-logo` `text-nav` `centered`
**Category:** [[categories/personal|personal]]
**Tech:** [[tech/webflow|Webflow]] [[tech/google-tag-manager|Google Tag Manager]] [[tech/google-fonts|Google Fonts]] `jQuery (googleapis)` `Cloudfront CDN`
**Colors:** [[colors/neutral|neutral]]
**Fonts:** `Montserrat 100-900` `Montserrat Alternates 300-800`

## Related sites
[[sites/axiaisacat.indiehacker.bio|axiaisacat.indiehacker.bio]] [[sites/conigma.com|conigma.com]] [[sites/daryl.cv|daryl.cv]] [[sites/daviskeene.com|daviskeene.com]] [[sites/farza.com|farza.com]]
