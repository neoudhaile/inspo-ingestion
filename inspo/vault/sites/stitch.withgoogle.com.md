---
url: https://stitch.withgoogle.com/
title: "Stitch - Design with AI"
category: tools-build
aesthetics: [dark]
tags: [ai-design-tool, google-labs, prompt-to-ui, templates-gallery, angular, iframe-app, dark-mode]
extracted_at: 2026-06-06
---
# Stitch - Design with AI
> Design at the speed of AI  ·  [stitch.withgoogle.com](https://stitch.withgoogle.com/)

![stitch.withgoogle.com](../../../screenshots/stitchwithgooglecom.png)

**What it is** — Stitch is Google Labs' AI design canvas that turns natural-language prompts (or wireframes/screenshots) into editable mobile and web UIs plus front-end code. Its own pitch, captured from the rendered app, reads "Design at the speed of AI — Transform ideas into UI designs for mobile and web applications", and the FAQ calls it "an AI-native software design canvas developed by Google Labs."

**What it shows** — A product landing + live entry point in one: a prompt box ("What native mobile app shall we design?") with App/Web toggles and a Gemini model picker, three playful example prompts, a templates carousel (Studio Portfolio, Auralis Dashboard, Romer Analytics, Horizon SaaS, etc.), feature cards (Easy edits, Export code, Build with Gemini, Own your design), a "Vibe design is here" section, and an FAQ that highlights Figma export and a new MCP integration.

**How it works** — The shell is an Angular app (ng-version detected) on stitch.withgoogle.com, but the entire landing/app UI is rendered inside an embedded iframe served from app-companion-430619.appspot.com (a Google App Engine host), with a gapi companion frame for Google auth. Scripts come from apis.google.com, gstatic.com and GTM; fonts load from fonts.googleapis.com.

**How it's designed** — A dark Google-Labs aesthetic: the outer shell paints a deep charcoal (rgb(25,26,31)) behind white text, and the whole experience is typed in Google Sans / Google Sans Text (loaded via Google Fonts) with Google Material Icons — an unmistakably first-party Google product look. Color/typography here are reported from the outer document; the inner pitch UI lives in a cross-origin iframe so per-element colors weren't probed.

**Palette** — Deep charcoal canvas (rgb(25,26,31)) with white text — first-party Google dark UI.
**Fonts** — Google Sans + Google Sans Text (and Google Material Icons).

## Connections
**Aesthetics:** [[aesthetics/dark|dark]]
**Patterns:** `ai-design-tool` `google-labs` `prompt-to-ui` `templates-gallery` `angular` `iframe-app` [[patterns/dark-mode|dark-mode]]
**Category:** [[categories/tools-build|tools-build]]
**Tech:** `Angular` `Google App Engine (appspot)` `Google Identity (gapi)` [[tech/google-tag-manager|Google Tag Manager]] [[tech/google-fonts|Google Fonts]]
**Colors:** [[colors/dark|dark]]
**Fonts:** [[fonts/google-sans|Google Sans]] `Google Sans Text 400/500/700` `Google Material Icons`

## Related sites
[[sites/backgrounds.supply|backgrounds.supply]] [[sites/badmarketing.com|badmarketing.com]] [[sites/davekrugman.com|davekrugman.com]] [[sites/daytona.io|daytona.io]] [[sites/ditther.com|ditther.com]]
