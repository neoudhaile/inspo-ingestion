---
url: https://animations.dev/
domain: animations.dev
title: "animations.dev — Emil Kowalski's interactive animations course"
vertical: docs-resource
mode: light
vibe: [minimal, editorial]
topics: [design, engineering]
extracted_at: 2026-07-05
tags:
  - vertical/docs-resource
  - vibe/minimal
  - vibe/editorial
  - topic/design
  - topic/engineering
  - mode/light
---
# animations.dev — Emil Kowalski's interactive animations course
> Learn the theory and practice behind great animations with this interactive learning experience.  ·  [animations.dev](https://animations.dev/)

![animations.dev](../../screenshots/animationsdev.png)

**Vertical:** #vertical/docs-resource  ·  **Vibe:** #vibe/minimal #vibe/editorial  ·  **Topics:** #topic/design #topic/engineering  ·  **Mode:** #mode/light

## What it is
animations.dev — Emil Kowalski's interactive course on crafting UI animations: 'Learn the theory and practice behind great animations with this interactive learning experience.' It's the flagship product referenced in the bookmarked tweet (the /review-animations skill is its companion); enrollment is currently closed.

## What it shows
A long (~14,266px) course landing page. The hero h1 'How do you craft animations that feel right?' sits over a 'Notify me' CTA (enrollment closed), a 'Trusted by developers and designers at' logo wall, a 'Hey, I'm Emil' author section, a 'What you'll learn' curriculum with playfully-named interactive chapters (The Odyssey, Angry Rabbits, Ghost town, Pirates in the jungle, Lost in the mountains), 'Walkthroughs', and a 'You'll also get…' bonuses block.

## How it works
Next.js (next/font fallbacks + hashed static assets), self-hosted with no third-party analytics in the script set. It's extremely media-dense — 143 img, 53 inline svg and 1 video — to carry the animated course previews that demonstrate the craft it teaches.

## How it's designed
Warm, refined, light editorial. From getComputedStyle the canvas is a warm off-white (body rgb(253,253,252)) with pure-black text; the h1 renders 48px at an unusual 575 weight in Inter (variable 100–900). The type system pairs Inter (UI/headings) with a monospace and a 'serifInline' italic serif used for emphasis words — a signature Emil touch. No :root custom-property palette is exposed (tokens applied via classes), so colour claims come from getComputedStyle.

## Design data
- **Palette:** A warm off-white canvas (rgb(253,253,252)) with pure-black text — near-monochrome, letting the colourful animated course demos supply the colour.
- **Palette tokens:** body background: rgb(253, 253, 252) (rendered), body/h1 color: rgb(0, 0, 0) (rendered)
- **Fonts:** Inter (variable 100–900, the h1 at a 575 weight), a monospace, and a 'serifInline' italic serif for emphasis words.
- **Fonts loaded:** Inter 100-900 (variable), mono 400, serifInline 400
- **Tech stack:** Next.js (next/font), self-hosted
- **Keywords:** course, editorial, minimal, inter, serif-accent, nextjs, motion, media-dense, light
- **Media mix:** img 143 · video 1 · svg 53
- **Page height:** 14266px (single-screen: False)
- **Responsive:** At 390x844 the nav collapses to a hamburger, the hero h1 scales 48 → 40px, and the page stacks to a single column (~14,266 → 15,746px).
- **Headings:** How do you craft animations that feel right? / Enrollment is closed / What if you knew exactly how to craft great animations? / The interactive learning experience where you’ll learn the theory and practice behind great animations / Trusted by developers and designers at / Hey, I’m Emil / What you’ll learn / The Oddysey / Angry Rabbits / Ghost town / Pirates in the jungle / Lost in the mountains / Walkthroughs / You’ll also get…
- **Extracted:** 2026-07-05 · Playwright MCP, 1440x900 + 390x844 mobile pass, logged_out: true

## Related sites
- [[makingsoftware.com]] — shared: docs-resource, editorial, design, engineering, light
- [[transitions.dev]] — shared: docs-resource, minimal, design, engineering, light
- [[21st.dev]] — shared: minimal, editorial, design, engineering, light
- [[interfaces.dev]] — shared: minimal, editorial, design, engineering, light
- [[sensory-ui.com]] — shared: minimal, editorial, design, engineering, light
- [[walkinglabs.github.io]] — shared: docs-resource, editorial, engineering, light
