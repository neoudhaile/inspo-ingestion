---
url: https://www.ryancarson.com/
domain: ryancarson.com
title: "Ryan Carson, Founder with 20 years of experience building companies."
vertical: portfolio
mode: light
vibe: [minimal]
topics: [startups]
extracted_at: 2026-06-06
tags:
  - vertical/portfolio
  - vibe/minimal
  - topic/startups
  - mode/light
---
# Ryan Carson, Founder with 20 years of experience building companies.
> Founder, CEO and Developer with 25 years experience building developer communities and startups.  ·  [ryancarson.com](https://www.ryancarson.com/)

![ryancarson.com](../../screenshots/ryancarsoncom.png)

**Vertical:** #vertical/portfolio  ·  **Vibe:** #vibe/minimal  ·  **Topics:** #topic/startups  ·  **Mode:** #mode/light

## What it is
The personal site of serial founder Ryan Carson (DropSend, Carsonified, Treehouse). The hero <h1> reads 'Founder, CEO and Developer with 25 years experience building developer communities and startups.'

## What it shows
A clean résumé-style homepage: a circular avatar and bio, a three-up row of past ventures (DropSend, Carsonified, Treehouse), a strip of media/talk thumbnails, then a reverse-chronological feed of recent posts — currently AI-agent how-tos ('Code Factory', 'set up a team of agents in OpenClaw', 'agent that learns and ships while you sleep') and a newsletter sign-up.

## How it works
A static, content-first page built with Tailwind CSS; no SPA framework global is exposed (__NEXT__/__NUXT__/Vue/Svelte all absent), so it reads as a static export. The only third-party script is Google Tag Manager.

## How it's designed
Minimal editorial layout on an off-white rgb(250,250,250) canvas with black body text and near-black rgb(39,39,42) headings; the only CSS custom properties present are Tailwind's own utility vars plus a few avatar/header layout vars (--header-height:180px, sticky header). No webfont is downloaded at all — document.fonts is empty, so it renders entirely in the system ui-sans-serif stack. Accent restraint, generous whitespace, a single small avatar as the only ornament.

## Design data
- **Palette:** Off-white #fafafa background, black body text, near-black #27272a headings — essentially monochrome
- **Palette tokens:** body bg: rgb(250,250,250) (rendered), body text: rgb(0,0,0) (rendered), h1: rgb(39,39,42) (rendered), button bg: rgba(255,255,255,0.9) (rendered)
- **Fonts:** System fonts only (ui-sans-serif / system-ui) — no webfont payload
- **Fonts loaded:** system only (no webfont)
- **Tech stack:** Tailwind CSS, Google Tag Manager
- **Keywords:** minimalist, personal, portfolio, editorial, system-fonts, tailwind
- **Media mix:** img 9 · svg 12
- **Page height:** 2789px (single-screen: False)
- **Responsive:** At 390×844 the layout collapses to a single column and the page grows from ~2,790px to ~3,755px; nav remains.
- **Headings:** Founder, CEO and Developer with 25 years experience building developer communities and startups. / DropSend / Carsonified / Treehouse / Code Factory: How to setup your repo so your agent can auto write and review 100% of your code / How to setup a team of agents in OpenClaw - in just one command / How to setup your agent to do daily testing + file bugs / How to make your agent learn and ship while you sleep / Stay up to date
- **Weight:** None requests; hosts: www.ryancarson.com, www.googletagmanager.com
- **Extracted:** 2026-06-06 · Playwright 1440x900 + 390x844 mobile pass, logged_out: true

## Related sites
- [[axiaisacat.indiehacker.bio]] — shared: portfolio, minimal, startups, light
- [[debarghyadas.com]] — shared: portfolio, minimal, startups, light
- [[farza.com]] — shared: portfolio, minimal, startups, light
- [[julian.ai]] — shared: portfolio, minimal, startups, light
- [[shanemac.com]] — shared: portfolio, minimal, startups, light
- [[willmanidis.com]] — shared: portfolio, minimal, startups, light
