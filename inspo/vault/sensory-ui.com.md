---
url: https://www.sensory-ui.com/
domain: sensory-ui.com
title: "sensory-ui - Semantic Sound for React & Next.js"
vertical: tool-app
mode: light
vibe: [editorial, minimal]
topics: [engineering, design]
extracted_at: 2026-06-05
tags:
  - vertical/tool-app
  - vibe/editorial
  - vibe/minimal
  - topic/engineering
  - topic/design
  - mode/light
---
# sensory-ui - Semantic Sound for React & Next.js
> A semantic, opt-in sound layer for React and Next.js apps — meaningful audio feedback for UI, built for shadcn/ui.  ·  [sensory-ui.com](https://www.sensory-ui.com/)

![sensory-ui.com](../../screenshots/sensory-uicom.png)

**Vertical:** #vertical/tool-app  ·  **Vibe:** #vibe/editorial #vibe/minimal  ·  **Topics:** #topic/engineering #topic/design  ·  **Mode:** #mode/light

## What it is
sensory-ui, an opt-in semantic sound layer for React/Next.js apps by Satyam Vyas (github.com/SatyamVyas04/sensory-ui) — 'Your website speaks. Give it a voice.' It adds meaningful audio feedback to UI interactions with 17 sound roles across 24 components, built for shadcn/ui (v1 early preview). One of Devster's inspo-dump links.

## What it shows
A hero with a photoreal 3D render of a translucent reel-to-reel tape machine beside the headline, a shadcn install command ('npx shadcn@latest add …/sensory-ui-switch'), and a stat strip (24 components · 17 roles · 9 sound packs · ~26kb gzipped); below, a 'Showcase — Feel the difference.' carousel and editorial sections ('Sound with intention.', 'The forgotten dimension.') making the case for UI sound, citing Material Design's sound guidelines.

## How it works
A single ~4,785px page on the shadcn/ui token system; the demo components play audio on interaction (1 <video>, 73 inline <svg>, a hero-background.jpg) and the library installs via the shadcn registry CLI. Analytics are self-hosted (p.sensory-ui.com); no framework global is exposed but the Geist stack + tokens indicate a Next.js build, and a light/dark theme toggle is present.

## How it's designed
Crisp editorial light theme with a single bold accent: a white ground (--background #fff) with near-black ink (--foreground #0c0a09) and a strong signal red (--primary #e40014) that colours the 'voice.' word, the CTA and the chart ramp (#ffa3a3 → #9f0712). The 'Your website speaks…' headline is set in GeistPixelCircle (a dotted pixel display face) with Geist Sans for prose and Geist Mono for the install command.

## Design data
- **Palette:** White ground (--background #fff) with near-black ink (--foreground #0c0a09) and a single bold red accent (--primary #e40014) running through CTA, headline highlight and a red chart ramp.
- **Palette tokens:** --background: #fff (var), --foreground: #0c0a09 (var), --primary: #e40014 (var), --chart-1: #ffa3a3 (var)
- **Fonts:** GeistPixelCircle (dotted pixel display headline) + Geist Sans (prose) + Geist Mono (install command) — all three load.
- **Fonts loaded:** Geist (variable 100-900), Geist Mono (variable 100-900), GeistPixelCircle 500
- **Tech stack:** shadcn/ui tokens, Geist, self-hosted analytics (p.sensory-ui.com)
- **Keywords:** developer-tool, sound-ui, shadcn, pixel-type, editorial, light-mode, red-accent, open-source
- **Media mix:** img 8 · video 1 · svg 73
- **Page height:** 4785px (single-screen: False)
- **Responsive:** At 390x844 the hero stacks the tape-machine render above the copy, the headline drops from 60px to 36px, and the sections expand to a ~8,271px scroll; no burger nav.
- **Headings:** Your website speaks. Give it a voice. / Feel the difference. / Sound with intention. / The forgotten dimension. / Give your UI a voice.
- **Links out:** [GitHub (SatyamVyas04/sensory-ui)](https://github.com/SatyamVyas04/sensory-ui) · [Material Design — About Sound](https://m2.material.io/design/sound/about-sound.html)
- **Extracted:** 2026-06-05 · playwright-mcp @ 1440x900 (fullPage) + mobile 390x844, logged_out: true

## Related sites
- [[drawably.dev]] — shared: tool-app, minimal, engineering, design, light
- [[itshover.com]] — shared: tool-app, minimal, engineering, design, light
- [[patterncraft.fun]] — shared: tool-app, minimal, engineering, design, light
- [[serif.sh]] — shared: tool-app, editorial, minimal, design, light
- [[21st.dev]] — shared: editorial, minimal, engineering, design, light
- [[animations.dev]] — shared: editorial, minimal, engineering, design, light
