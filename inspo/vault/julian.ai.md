---
url: https://www.julian.ai/
domain: julian.ai
title: "Julian Alvarez"
vertical: portfolio
mode: light
vibe: [minimal, playful]
topics: [startups]
extracted_at: 2026-06-06
tags:
  - vertical/portfolio
  - vibe/minimal
  - vibe/playful
  - topic/startups
  - mode/light
---
# Julian Alvarez
> Hello Universe! ¡Hola! 👋  ·  [julian.ai](https://www.julian.ai/)

![julian.ai](../../screenshots/julianai.png)

**Vertical:** #vertical/portfolio  ·  **Vibe:** #vibe/minimal #vibe/playful  ·  **Topics:** #topic/startups  ·  **Mode:** #mode/light

## What it is
The personal portfolio of Julian Alvarez — founder/CEO of Jungle, host of the 'Inventing The Future' podcast, ex-Meta/LinkedIn/Goldman engineer. (Note: the bookmark announces his 'unbounded ∞' second-brain app, but the tweet linked only this portfolio; the app itself has no public URL yet — the matching email is infinite@julian.ai.)

## What it shows
A two-column profile page: a fixed left sidebar with a circular avatar, name, the 'INFINITE / JULIAN.AI' tagline and social icons (LinkedIn, X, Instagram, GitHub, email); a right column with a 'Hello Universe! ¡Hola! 👋' greeting, a bulleted career overview, and the 'Inventing The Future' podcast cover artwork.

## How it works
A React single-page app styled with Chakra UI (the :root carries the full --chakra-* token set). PostHog is wired in for analytics (us-assets.i.posthog.com) and fonts come from Google Fonts; routes like /story, /about, /Jungle, /podcast, /contact are client-rendered.

## How it's designed
Clean light theme — Chakra's default body bg #FFFFFF with body text rgb(26,32,44) (#1A202C). Display copy is set in the Outfit webfont (Raleway and others are also loaded), giving a friendly geometric-sans feel; Font Awesome powers the social glyphs. Sparse imagery (only 2 images, 5 SVGs) keeps it text-forward and personable.

## Design data
- **Palette:** White background, dark slate #1A202C text, blue link accents (Chakra default palette)
- **Palette tokens:** --chakra-colors-chakra-body-bg: #FFFFFF (var), --chakra-colors-chakra-body-text: #1A202C (var), --chakra-colors-blue-500 (link): #3182ce (var), body text: rgb(26,32,44) (rendered)
- **Fonts:** Outfit (400/700) for display, Raleway (400/800) loaded too — via Google Fonts
- **Fonts loaded:** Outfit 400, Outfit 700, Raleway 400, Raleway 800
- **Tech stack:** React, Chakra UI, PostHog, Google Fonts
- **Keywords:** portfolio, personal, chakra-ui, two-column, light, podcast
- **Media mix:** img 2 · svg 5
- **Page height:** 1444px (single-screen: False)
- **Responsive:** At 390×844 the sidebar/nav collapses behind a ☰ hamburger and the columns stack, taking the page from ~1,444px to ~2,642px.
- **Headings:** Julian Alvarez / Hello Universe! ¡Hola! 👋 / About
- **Links out:** [Jungle](https://www.julian.ai/Jungle) · [Inventing The Future Podcast](https://www.julian.ai/podcast) · [LinkedIn](https://www.linkedin.com/in/julianalvarez42) · [X](https://twitter.com/infinitejulian0) · [GitHub](https://github.com/julianjear) · [email](mailto:infinite@julian.ai)
- **Weight:** None requests; hosts: www.julian.ai, us-assets.i.posthog.com, fonts.googleapis.com
- **Extracted:** 2026-06-06 · Playwright 1440x900 + 390x844 mobile pass, logged_out: true

## Related sites
- [[axiaisacat.indiehacker.bio]] — shared: portfolio, minimal, startups, light
- [[debarghyadas.com]] — shared: portfolio, minimal, startups, light
- [[designrebuilds.vercel.app]] — shared: portfolio, minimal, playful, light
- [[farza.com]] — shared: portfolio, minimal, startups, light
- [[gyanl.com]] — shared: portfolio, minimal, playful, light
- [[kmk0.com]] — shared: portfolio, minimal, playful, light
