---
url: https://www.simple.ink/
domain: simple.ink
title: "Notion Website Maker: Create A Free Website Built In Notion"
vertical: startup-product
mode: light
vibe: [corporate-clean, playful]
topics: [productivity]
extracted_at: 2026-06-06
tags:
  - vertical/startup-product
  - vibe/corporate-clean
  - vibe/playful
  - topic/productivity
  - mode/light
---
# Notion Website Maker: Create A Free Website Built In Notion
> Turn your Notion page into your website in 1 minute — free, no-code, no credit card.  ·  [simple.ink](https://www.simple.ink/)

![simple.ink](../../screenshots/simpleink.png)

**Vertical:** #vertical/startup-product  ·  **Vibe:** #vibe/corporate-clean #vibe/playful  ·  **Topics:** #topic/productivity  ·  **Mode:** #mode/light

## What it is
A no-code SaaS that turns any Notion page into a live, custom-domain website in one click. The pitch is right there in the hero — 'Build a website with Notion' — and it's freemium with no credit card to start. The audience is Notion power-users who already keep their content in Notion and want it published as a real site (portfolios, help centers, job boards, landing pages) without touching code.

## What it shows
A long (~15.5k px) marketing landing page. It opens on a hero with a browser-frame product mockup, then walks through 'Your Notion Website in 1 Minute' and 'Hassle-Free Notion Websites' value sections, a wall of real customer sites (Kylar San Juan's portfolio, a 'Jobs @ Handle' board, a 'LiveTechHelper' help center, several personal portfolios) shown in embeds, testimonials, and a deep SEO/CMS FAQ ('Can you use Notion as a CMS?', 'Is Notion SEO friendly?') before a final 'Start building your Notion website for free' CTA.

## How it works
A conventional scrolling marketing page driven by repeated 'Start free' / 'Build a website' CTAs. Five iframes embed live example Notion sites inline. A Hellobar promo strip rides the top ('Welcome back 🤗'), a Zendesk widget offers chat, and FirstPromoter runs affiliate/referral tracking — the funnel machinery of a self-serve SaaS. On mobile the nav collapses behind a hamburger.

## How it's designed
Built on Webflow (all assets served from cdn.prod.website-files.com, a single Webflow stylesheet). Notably it ships no brand webfont at all — the only loaded face is 'webflow-icons', so every word renders in the native system-ui stack; the big h1 is system-ui 54px/800 in near-black (#222) on white. Personality comes from a friendly multi-accent brand palette declared in CSS vars — two blues (#0f93ff, #1a61fb), a UI purple (#7970ff), a green (#2eb67c), a peach (#ff8f7d) and a yellow (#ffe871) — used across icons, the browser mockups and section accents. Heavy on imagery (56 imgs, 80 inline SVGs) and product embeds rather than illustration.

## Design data
- **Palette:** White ground, near-black text (#222); friendly multi-accent brand set — blue #0f93ff/#1a61fb, purple #7970ff, green #2eb67c, peach #ff8f7d, yellow #ffe871.
- **Palette tokens:** --black: #222 (var), --blue-main-1: #0f93ff (var), --blue: #1a61fb (var), --ui-purple: #7970ff (var), --green-ui: #2eb67c (var), --peach: #ff8f7d (var), --yellow-ui: #ffe871 (var), body-bg: rgb(255, 255, 255) (rendered), body-text: rgb(34, 34, 34) (rendered)
- **Fonts:** System UI stack only — no brand webfont payload (only a 'webflow-icons' icon font loads).
- **Fonts loaded:** system only (no webfont)
- **Tech stack:** Webflow, Google Analytics, Google Tag Manager, FirstPromoter, Hellobar, Zendesk, Cloudfront
- **Keywords:** saas-landing, webflow, product-mockup-hero, social-proof-wall, live-embeds, seo-faq, freemium, hellobar-promo, system-fonts
- **Media mix:** img 56 · svg 80 · iframe 5
- **Page height:** 15515px (single-screen: False)
- **Responsive:** At 390px the page reflows to a single column, grows to ~21.6k px, and the top nav collapses behind a hamburger menu.
- **Headings:** Build a website with Notion / Your Notion Website in 1 Minute / Hassle-Free Notion Websites with Simple.ink / Turn Your Notion Page into a Website / Explore Simple.ink's top features / Thousands of people trust us with their website: see for yourself why / What Our Users are Saying: / Frequently asked questions about Notion-powered websites / Can you use Notion as a CMS? / Is Notion SEO friendly? / Start building your Notion website for free
- **Extracted:** 2026-06-06 · playwright-mcp @ 1440x900 + 390x844 mobile; logged_out: true

## Related sites
- [[gatheros.co]] — shared: startup-product, corporate-clean, productivity, light
- [[linkeddit.com]] — shared: startup-product, corporate-clean, playful, light
- [[photon.codes]] — shared: startup-product, corporate-clean, playful, light
- [[shipper.now]] — shared: startup-product, corporate-clean, playful, light
- [[flowstate.com]] — shared: startup-product, corporate-clean, productivity
- [[apps.ankiweb.net]] — shared: startup-product, productivity, light
