---
url: https://nucleoapp.com/
title: "Nucleo – The Ultimate Icon Bundle"
category: uncategorized
aesthetics: [developer-product, light]
tags: [product-landing, icon-library, light, design-system, design-tokens, inter, ppnikkeimaru, jquery, bootstrapped]
extracted_at: 2026-07-08
---
# Nucleo – The Ultimate Icon Bundle
> Explore the Nucleo icons, 40000+ icons for UIs, presentations, and print projects. Download instantly or use them via our web and native apps.  ·  [nucleoapp.com](https://nucleoapp.com/)

![nucleoapp.com](../../../screenshots/nucleoappcom.png)

**What it is** — Nucleo, Sebastiano Guerriero's icon product (linked alongside the Lab01 demo). The h1 is 'The ultimate icon bundle' and the meta description reads 'Explore the Nucleo icons, 40000+ icons for UIs, presentations, and print projects. Download instantly or use them via our web and native apps.'

**What it shows** — A polished light product landing page — hero, a 'See in action' demo, an 'And yes, there's an app!' section and an 'Independent + Bootstrapped' note — with 27 <img> and 27 inline <svg> (the icons themselves) over a ~6,600px scroll.

**How it works** — A static site served from nucleoapp.com with jQuery present (no React/Next/Vue global), Google Fonts, and light instrumentation via Umami (cloud.umami.is) and Cloudflare Web Analytics. It publishes an unusually complete design-token system as :root custom properties.

**How it's designed** — A refined near-white product system built on an explicit token scale. getComputedStyle reports a body background rgb(250,250,250) with slate-grey body text rgb(63,67,70) and near-black headings rgb(27,32,35); the h1 renders at 76px in 'PPNikkeiMaru' (the --font-heading token), while body copy is variable 'Inter' (--font-body). The primary CTA is a white pill (button bg rgb(255,255,255), text rgb(27,32,35)). The :root exposes a full design system — fluid spacing (--space-4xs … --space-4xl via clamp()), a type scale (--text-2xs … --text-5xl), layered shadow tokens built on HSL black/white channels, radius tokens and named easing curves (--ease-out-back cubic-bezier(0.34,1.56,0.64,1)).

**Palette** — Near-white canvas (#fafafa / rgb 250,250,250) with slate-grey body text (rgb 63,67,70), near-black headings (rgb 27,32,35) and white pill CTAs.
**Fonts** — Variable 'Inter' (100–900) for UI/body via --font-body, paired with 'PPNikkeiMaru' (loaded 600) for headings via --font-heading.

## Connections
**Aesthetics:** [[aesthetics/developer-product|developer-product]] [[aesthetics/light|light]]
**Patterns:** [[patterns/product-landing|product-landing]] `icon-library` [[patterns/light|light]] [[patterns/design-system|design-system]] [[patterns/design-tokens|design-tokens]] [[patterns/inter|inter]] `ppnikkeimaru` `jquery` `bootstrapped`
**Category:** [[categories/uncategorized|uncategorized]]
**Tech:** `Static site + jQuery` `Umami analytics` `Cloudflare (Web Analytics + CDN)` [[tech/google-fonts|Google Fonts]]
**Colors:** [[colors/light|light]]
**Fonts:** `Inter (variable 100-900)` `PPNikkeiMaru`

## Related sites
[[sites/animations.dev|animations.dev]] [[sites/vercel.com|vercel.com]] [[sites/21st.dev|21st.dev]] [[sites/b150.ai|b150.ai]] [[sites/cofounder.co|cofounder.co]]
