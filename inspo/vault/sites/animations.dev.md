---
url: https://animations.dev/
title: "animations.dev — Emil Kowalski's interactive animations course"
category: uncategorized
aesthetics: [editorial, minimal, light]
tags: [course, editorial, minimal, inter, serif-accent, nextjs, motion, media-dense, light]
extracted_at: 2026-07-05
---
# animations.dev — Emil Kowalski's interactive animations course
> Learn the theory and practice behind great animations with this interactive learning experience.  ·  [animations.dev](https://animations.dev/)

![animations.dev](../../../screenshots/animationsdev.png)

**What it is** — animations.dev — Emil Kowalski's interactive course on crafting UI animations: 'Learn the theory and practice behind great animations with this interactive learning experience.' It's the flagship product referenced in the bookmarked tweet (the /review-animations skill is its companion); enrollment is currently closed.

**What it shows** — A long (~14,266px) course landing page. The hero h1 'How do you craft animations that feel right?' sits over a 'Notify me' CTA (enrollment closed), a 'Trusted by developers and designers at' logo wall, a 'Hey, I'm Emil' author section, a 'What you'll learn' curriculum with playfully-named interactive chapters (The Odyssey, Angry Rabbits, Ghost town, Pirates in the jungle, Lost in the mountains), 'Walkthroughs', and a 'You'll also get…' bonuses block.

**How it works** — Next.js (next/font fallbacks + hashed static assets), self-hosted with no third-party analytics in the script set. It's extremely media-dense — 143 img, 53 inline svg and 1 video — to carry the animated course previews that demonstrate the craft it teaches.

**How it's designed** — Warm, refined, light editorial. From getComputedStyle the canvas is a warm off-white (body rgb(253,253,252)) with pure-black text; the h1 renders 48px at an unusual 575 weight in Inter (variable 100–900). The type system pairs Inter (UI/headings) with a monospace and a 'serifInline' italic serif used for emphasis words — a signature Emil touch. No :root custom-property palette is exposed (tokens applied via classes), so colour claims come from getComputedStyle.

**Palette** — A warm off-white canvas (rgb(253,253,252)) with pure-black text — near-monochrome, letting the colourful animated course demos supply the colour.
**Fonts** — Inter (variable 100–900, the h1 at a 575 weight), a monospace, and a 'serifInline' italic serif for emphasis words.

## Connections
**Aesthetics:** [[aesthetics/editorial|editorial]] [[aesthetics/minimal|minimal]] [[aesthetics/light|light]]
**Patterns:** `course` [[patterns/editorial|editorial]] [[patterns/minimal|minimal]] [[patterns/inter|inter]] `serif-accent` [[patterns/nextjs|nextjs]] `motion` `media-dense` [[patterns/light|light]]
**Category:** [[categories/uncategorized|uncategorized]]
**Tech:** `Next.js (next/font)` [[tech/self-hosted|self-hosted]]
**Colors:** [[colors/light|light]] [[colors/monochrome|monochrome]] [[colors/warm|warm]]
**Fonts:** [[fonts/inter-100-900-variable|Inter 100-900 (variable)]] `mono` `serifInline`

## Related sites
[[sites/emilkowal.ski|emilkowal.ski]] [[sites/nucleoapp.com|nucleoapp.com]] [[sites/type.lol|type.lol]] [[sites/12matcha.com|12matcha.com]] [[sites/21st.dev|21st.dev]]
