---
url: https://akira.sachi.dev/
domain: akira.sachi.dev
title: "Akira | Modern Next.js Starter"
vertical: tool-app
mode: light
vibe: [technical, minimal]
topics: [engineering]
extracted_at: 2026-06-05
tags:
  - vertical/tool-app
  - vibe/technical
  - vibe/minimal
  - topic/engineering
  - mode/light
---
# Akira | Modern Next.js Starter
> A modern starter with Next.js, Tailwind, ShadCN/ui, Motion, Drizzle, Postgres, Auth, Dodo Payments, and Resend.  ·  [akira.sachi.dev](https://akira.sachi.dev/)

![akira.sachi.dev](../../screenshots/akirasachidev.png)

**Vertical:** #vertical/tool-app  ·  **Vibe:** #vibe/technical #vibe/minimal  ·  **Topics:** #topic/engineering  ·  **Mode:** #mode/light

## What it is
The landing page for Akira, a modern open-source Next.js starter kit by Sachi Goyal (h1: 'Akira'; github.com/sachigoyal/akira) — 'A modern starter with Next.js, Tailwind, ShadCN/ui, Motion, Drizzle, Postgres, Auth, Dodo Payments, Resend.' One of the sites in Devster's inspo dump.

## What it shows
A blueprint-style one-screen marketing page: a left column with a 'Ship right away' pill, the Akira wordmark, Github + 'Get Akira' buttons and a 4x3 grid of stack logos (Next.js, Motion, TypeScript, Tailwind, Drizzle, Neon, Better Auth, Dodo, Resend, shadcn/ui); a right column of feature cards — 'Secure by default.' (auth), 'Get paid globally.' (payments) and 'Query anything.' with a faux database schema table.

## How it works
A single full-height screen (~900px, scroll-snapped) with hatched 'engineering drawing' margins framing the content; built on shadcn/ui's token system and Motion for animation (no framework global is exposed in the DOM, but the Geist stack and tokens point to a Next.js build). Logos are 33 inline SVGs and there are zero raster images; a light/dark theme toggle sits in the footer.

## How it's designed
Technical, mono, near-monochrome: a white ground (--background #fff) with near-black ink (--foreground #0a0a0a) and a dark neutral primary (--primary #171717) for the filled button. The whole page leans into a developer-blueprint look — the 'Akira' headline is set in GeistPixelSquare (a pixel/dot display face) and section labels in Geist Mono, with Geist Sans for prose. A shadcn chart palette (--chart-1 #f05100, --chart-2 #009588…) is defined but the visible UI stays grayscale.

## Design data
- **Palette:** White ground (--background #fff) with near-black ink (--foreground #0a0a0a) and a dark neutral primary (--primary #171717); essentially monochrome blueprint, accent colors defined in tokens but unused on screen.
- **Palette tokens:** --background: #fff (var), --foreground: #0a0a0a (var), --primary: #171717 (var), --destructive: #e40014 (var)
- **Fonts:** GeistPixelSquare (pixel display headline) + Geist Mono (labels/code) + Geist Sans (body) — Geist and Geist Mono variable plus GeistPixelSquare 500 actually load.
- **Fonts loaded:** Geist (variable 100-900), Geist Mono (variable 100-900), GeistPixelSquare 500
- **Tech stack:** Next.js (Geist stack + shadcn tokens; no framework global exposed), shadcn/ui, Motion, no analytics detected
- **Keywords:** developer-tool, boilerplate, blueprint, single-screen, monospace, pixel-type, shadcn, light-mode
- **Media mix:** svg 33
- **Page height:** 900px (single-screen: True)
- **Responsive:** At 390x844 the two-column blueprint collapses to a single column and the wordmark drops from 60px to 36px while the page stays roughly single-screen (scrollHeight ~844px).
- **Headings:** Akira / Secure bydefault. / Get paidglobally. / Query anything.
- **Links out:** [Github (sachigoyal/akira)](https://github.com/sachigoyal/akira) · [Get Akira](https://akira.sachi.dev/signin) · [sachi (author)](https://sachi.dev/)
- **Extracted:** 2026-06-05 · playwright-mcp @ 1440x900 (fullPage) + mobile 390x844, logged_out: true

## Related sites
- [[itshover.com]] — shared: tool-app, technical, minimal, engineering, light
- [[colf.dev]] — shared: tool-app, technical, engineering, light
- [[drawably.dev]] — shared: tool-app, minimal, engineering, light
- [[humanatlas.quest]] — shared: tool-app, technical, minimal, light
- [[patterncraft.fun]] — shared: tool-app, minimal, engineering, light
- [[sensory-ui.com]] — shared: tool-app, minimal, engineering, light
