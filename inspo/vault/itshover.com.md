---
url: https://www.itshover.com/
domain: itshover.com
title: "Its Hover"
category: uncategorized
extracted_at: 2026-06-05
tags:
  - category/uncategorized
  - aesthetic/developer-product
  - pattern/icon-library
  - pattern/animated-icons
  - pattern/open-source
  - pattern/monospace
  - pattern/react
  - pattern/shadcn
  - pattern/terracotta
  - pattern/developer-tool
  - tech/shadcn-ui-tokens
  - tech/motion
  - tech/umami-analytics
  - tech/geist-mono
  - color/cool
  - font/geist-mono-variable-100-900
---
# Its Hover
> Animated icons that move with intent.  ·  [itshover.com](https://www.itshover.com/)

![itshover.com](../../screenshots/itshovercom.png)

## What it is
Its Hover, an open-source library of animated icons by Abhijit (@abhijitwt; github.com/itshover/itshover) — 'editable react components with motion baked in' that work with Next.js, shadcn and modern design systems (h1s: 'itshover' / 'icons that move with intent'). One of Devster's inspo-dump links.

## What it shows
A hero where large grey line-icon glyphs (thumbs-up, stacked layers, paper plane, ghost, terminal prompt) float around the headline and animate on hover, with an 'OPEN SOURCE' pill, 'Browse Icons' / 'Sponsor' CTAs, a GitHub star count and a ⌘K search; below it, feature sections (open source, customize), a 'backed by' / 'loved by creators' block and a closing 'Ready to Bring your icons to life?' CTA. A crypto contract address is shown under the hero.

## How it works
A single ~4,723px page built on the shadcn/ui token system; the icons are React components animated with Motion (52 inline <svg> plus 2 demo <video>). It uses Umami for analytics (cloud.umami.is), a light/dark theme toggle, and installs via the standard shadcn registry flow. No framework global is exposed but the Geist stack + tokens indicate a Next.js build.

## How it's designed
Warm monospace developer aesthetic: a white ground (--background #fff) with near-black ink (--foreground #111827), a terracotta/burnt-orange primary (--primary #d87943) and a muted teal secondary (--secondary #527575) — the orange highlights the 'intent' word and the primary CTA. Type is mono-forward: Geist Mono is the UI sans (--font-sans) with JetBrains Mono as --font-mono, and a soft shadow scale keeps cards flat and light.

## Design data
- **Palette:** White ground (--background #fff) with near-black ink (--foreground #111827); a terracotta primary (--primary #d87943) and muted teal secondary (--secondary #527575) as the accent pair.
- **Palette tokens:** --background: #fff (var), --foreground: #111827 (var), --primary: #d87943 (var), --secondary: #527575 (var)
- **Fonts:** Geist Mono (the loaded UI face, set as --font-sans) with JetBrains Mono declared as --font-mono; the Geist Sans variants are declared but stay unloaded on the home view.
- **Fonts loaded:** Geist Mono (variable 100-900)
- **Tech stack:** shadcn/ui tokens, Motion, Umami (analytics), Geist Mono
- **Media mix:** img 4 · video 2 · svg 52
- **Page height:** 4723px (single-screen: False)
- **Responsive:** At 390x844 the floating hero glyphs reflow and the page grows to a ~6,745px scroll while the mono headline stays at 24px; the header has no burger.
- **Headings:** itshover / icons that move with intent / features / backed by / loved by creators / Ready to Bring your icons to life?
- **Links out:** [GitHub (itshover/itshover)](https://github.com/itshover/itshover) · [Browse Icons](https://www.itshover.com/icons) · [Abhijit (@abhijitwt)](https://x.com/abhijitwt)
- **Extracted:** 2026-06-05 · playwright-mcp @ 1440x900 (fullPage) + mobile 390x844, logged_out: true

## Related sites
[[akira.sachi.dev]] [[patterncraft.fun]] [[sensory-ui.com]] [[printingpress.dev]] [[21st.dev]] [[davekrugman.com]]

## Tags
#category/uncategorized #aesthetic/developer-product #pattern/icon-library #pattern/animated-icons #pattern/open-source #pattern/monospace #pattern/react #pattern/shadcn #pattern/terracotta #pattern/developer-tool #tech/shadcn-ui-tokens #tech/motion #tech/umami-analytics #tech/geist-mono #color/cool #font/geist-mono-variable-100-900
