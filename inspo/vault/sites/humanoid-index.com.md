---
url: https://humanoid-index.com/
title: "Humanoid Index — a comprehensive visual index of humanoid robots"
category: uncategorized
aesthetics: [minimal]
tags: [index, directory, robotics, minimalist, monochrome, geist, nextjs, design-system, spec-sheet, comparison]
extracted_at: 2026-07-05
---
# Humanoid Index — a comprehensive visual index of humanoid robots
> A comprehensive visual index of humanoid robots.  ·  [humanoid-index.com](https://humanoid-index.com/)

![humanoid-index.com](../../../screenshots/humanoid-indexcom.png)

**What it is** — Humanoid Index — 'a comprehensive visual index of humanoid robots.' It's the 'visual index of humanoid robots' from Jonas's list: a catalogue comparing the current generation of humanoid robots.

**What it shows** — A gallery/index of humanoid robots — Memo, Oli, K2, Domo / Domo Plus, Tesla Optimus Gen 2, Boston Dynamics' Electric Atlas, 1X Neo, Figure 02, Sanctuary Phoenix, Apptronik Apollo, Unitree G1 / H1, Astribot S1, Tiangong and Menteebot — each with a photo and a spec blurb ('Memo is built for everyday housework, from tidying surfaces to moving…'), plus a Compare tool.

**How it works** — A Next.js app (Geist typeface via next/font, next-font fallbacks and hashed static assets) self-hosted with Plausible analytics. It's media-forward — 32 robot images, 26 svg icons and 2 canvases (spec/compare visuals) — and runs a little taller than one screen (1150px).

**How it's designed** — Restrained, spec-sheet minimalism built on a proper neutral design system read from :root: a white canvas (body rgb(255,255,255)) with a full grayscale ramp (--color-neutral-50 #fafafa → --color-neutral-900 #171717), four whisper-tinted surfaces (warm #fafaf8, cool #f8fafa, cream #faf9f8, blush #faf8f9) and a near-black accent (--color-accent #171717); body text is neutral-700 rgb(64,64,64). Type is Geist Sans (variable 100–900) with tight negative tracking (down to -0.04em) — clean, technical, Vercel-adjacent.

**Palette** — White with a full neutral-gray ramp (#fafafa → #171717) and four whisper-tinted surfaces (warm/cool/cream/blush); a near-black #171717 accent — monochrome so the robot photography pops.
**Fonts** — Geist Sans (variable 100–900) throughout — no serif — with tight negative tracking tokens.

## Connections
**Aesthetics:** [[aesthetics/minimal|minimal]]
**Patterns:** `index` [[patterns/directory|directory]] `robotics` [[patterns/minimalist|minimalist]] [[patterns/monochrome|monochrome]] [[patterns/geist|geist]] [[patterns/nextjs|nextjs]] [[patterns/design-system|design-system]] `spec-sheet` `comparison`
**Category:** [[categories/uncategorized|uncategorized]]
**Tech:** `Next.js (Geist / next-font)` [[tech/plausible|Plausible]]
**Colors:** [[colors/monochrome|monochrome]] [[colors/warm|warm]]
**Fonts:** `Geist Sans 100-900 (variable)`

## Related sites
[[sites/designengineer.tools|designengineer.tools]] [[sites/designtools.fyi|designtools.fyi]] [[sites/nicolasbustamante.com|nicolasbustamante.com]] [[sites/noahzender.com|noahzender.com]] [[sites/northgarden.com|northgarden.com]]
