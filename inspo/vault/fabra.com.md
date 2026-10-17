---
url: https://www.fabra.com/
domain: fabra.com
title: "Fabra - Turn Ideas into Real Products"
vertical: startup-product
mode: light
vibe: [editorial, corporate-clean]
topics: [fashion, design]
extracted_at: 2026-10-17
tags:
  - vertical/startup-product
  - vibe/editorial
  - vibe/corporate-clean
  - topic/fashion
  - topic/design
  - mode/light
---
# Fabra - Turn Ideas into Real Products
> Your product design studio  ·  [fabra.com](https://www.fabra.com/)

![fabra.com](../../screenshots/fabracom.png)

**Vertical:** #vertical/startup-product  ·  **Vibe:** #vibe/editorial #vibe/corporate-clean  ·  **Topics:** #topic/fashion #topic/design  ·  **Mode:** #mode/light

## What it is
A browser-based 3D apparel design platform: design garments in 3D, pull from thousands of assets, and generate production-ready tech packs.

## What it shows
The h1 reads 'YOUR PRODUCT DESIGN STUDIO'. Below it: category entry points (Streetwear, Merch, Sportswear, Athleisure, Swimwear, Kidswear, Sleepwear, Women's/Men's RTW, Denim), feature sections (Design Editor, Pattern Editing, Range Plan, Tech Pack), an AI generation block ('Your ideas, generated'), inspiration browsing, 'The Fabra Report' and the team.

## How it works
Navigation is organised by garment category (/category/*) and feature (/features/*). The long marketing scroll (13049px) walks from 'Pick a starting point' through editor features to community and a report/blog section. Segment and Amplitude events fire to events.fabra.com.

## How it's designed
All-caps display headings in Signs with GT America (and GT America Condensed) for supporting text; the page is black type on a white canvas (html and body backgrounds are transparent, h1 rgb(0,0,0)). No CSS custom properties are declared on :root. Image-heavy: 208 img and 187 svg elements, much of it product and garment imagery.

## Design data
- **Palette:** Black on white; color comes from garment imagery rather than UI tokens
- **Palette tokens:** body text: rgb(0, 0, 0) (rendered), h1: rgb(0, 0, 0) (rendered), canvas: transparent over white (rendered)
- **Fonts:** Signs (display, all-caps), GT America and GT America Condensed (body/labels)
- **Fonts loaded:** Signs 400, Signs 500, GT America 400, GT America 500, GT America Condensed 500
- **Tech stack:** Segment, Amplitude, Google Tag Manager, Facebook Pixel
- **Keywords:** category-grid, all-caps-display, feature-sections, product-imagery, tech-pack
- **Media mix:** img 208 · svg 187
- **Page height:** 13049px (single-screen: False)
- **Responsive:** At 390px the h1 shrinks from 56px to 40px, the header links disappear behind a menu button, no horizontal overflow (scrollWidth 390), and page height is 12375px.
- **Headings:** YOUR PRODUCT DESIGN STUDIO / PICK A STARTING POINT / JOIN THE DESIGNERS ALREADY ON FABRA / PRO FOUNDATIONS, YOUR VISION / DESIGN EDITOR / PATTERN EDITING / RANGE PLAN / TECH PACK / EVERYTHING YOU NEED TO START / YOUR IDEAS, GENERATED / FIND YOUR CATEGORY / BROWSE YOUR NEXT INSPIRATION / THE FABRA REPORT
- **Links out:** [Design Editor](https://www.fabra.com/features/design-editor) · [Pattern Editing](https://www.fabra.com/features/pattern-editing) · [Streetwear](https://www.fabra.com/category/streetwear)
- **Weight:** None requests; hosts: connect.facebook.net, events.fabra.com, cdn.segment.com, www.googletagmanager.com, cdn.amplitude.com
- **Extracted:** 2026-10-17 · Playwright MCP, fullPage 1440x900 + 390x844 mobile text pass, DOM probe; logged_out: true

## Related sites
- [[creao.ai]] — shared: startup-product, editorial, corporate-clean, light
- [[gatheros.co]] — shared: startup-product, corporate-clean, design, light
- [[cavalry.studio]] — shared: startup-product, corporate-clean, design
- [[www.unicorn.studio]] — shared: startup-product, corporate-clean, design
- [[bigideasdb.com]] — shared: startup-product, corporate-clean, light
- [[contralabs.com]] — shared: startup-product, editorial, light
