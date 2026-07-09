---
url: https://www.bigplayers.co/subscribe
title: "Subscribe | Big Players"
category: product
aesthetics: [dark]
tags: [newsletter, subscribe-page, beehiiv, dark-theme, email-capture, template]
extracted_at: 2026-06-06
---
# Subscribe | Big Players
> Steal billion-dollar growth strategies from the world's top companies.  ·  [bigplayers.co](https://www.bigplayers.co/subscribe)

![bigplayers.co](../../../screenshots/bigplayersco.png)

**What it is** — The beehiiv subscribe page for 'Big Players,' a weekly growth-marketing newsletter — the meta description pitches it as 'Steal billion-dollar growth strategies from the world's top companies. Get data-driven tactics, AI tools, and proven playbooks delivered weekly to scale your business faster.' Matthew Berman's tweet about his free OpenClaw 'Meta Ads Kit' funnels readers here to subscribe.

**What it shows** — A dark, centered email-capture page headed simply 'Big Players,' with an email field and a magenta subscribe button set against the publication's brand thumbnail — the standard beehiiv hosted subscribe layout, no marketing long-form below it.

**How it works** — Hosted entirely on beehiiv — the favicon, og:image and footer (Report abuse / Privacy / Terms) all resolve to beehiiv, and styling is driven by beehiiv's '--wt-*' theme tokens rather than a custom framework (no Next/Nuxt/Vue/Svelte/React global). The page carries a heavy marketing/measurement stack: Google Tag Manager, the Meta/Facebook pixel (connect.facebook.net), PerimeterX bot defense (client.px-cloud.net), Birdie (app.birdie.so) and Cloudflare Insights. Notably no webfont is actually downloaded — the configured header/body fonts fall back to system Helvetica.

**How it's designed** — A dark charcoal canvas (--wt-background-color #292d2e) with off-white text (--wt-text-on-background-color #f9fafb) and a single hot-magenta brand accent (--wt-primary-color #ec00fb, rendered rgb(236,0,251)) on the subscribe button, with corners rounded at --wt-border-radius 8px. Type is plain system Helvetica (the beehiiv default header stack names 'Helvetica Neue Condensed Black' but no webfont loads), so the magenta CTA and the brand thumbnail do all the visual work.

**Palette** — Charcoal #292d2e background, off-white #f9fafb text, hot-magenta #ec00fb CTA
**Fonts** — System Helvetica only — no webfont payload (beehiiv defaults)

## Connections
**Aesthetics:** [[aesthetics/dark|dark]]
**Patterns:** [[patterns/newsletter|newsletter]] `subscribe-page` `beehiiv` [[patterns/dark-theme|dark-theme]] [[patterns/email-capture|email-capture]] `template`
**Category:** [[categories/product|product]]
**Tech:** `beehiiv` [[tech/google-tag-manager|Google Tag Manager]] [[tech/meta-pixel|Meta Pixel]] `PerimeterX` `Birdie` [[tech/cloudflare-insights|Cloudflare Insights]]
**Colors:** [[colors/dark|dark]]
**Fonts:** [[fonts/system-fonts|system-fonts]]

## Related sites
[[sites/letters.thedankoe.com|letters.thedankoe.com]] [[sites/systematiclongshort.com|systematiclongshort.com]] [[sites/theprohuman.ai|theprohuman.ai]] [[sites/affiliatenetwork.com|affiliatenetwork.com]] [[sites/ashpreetbedi.com|ashpreetbedi.com]]
