---
url: https://www.hex.inc/
domain: hex.inc
title: "HEX Studio - Web, Marketing, Product & Brand Studio"
vertical: studio-agency
mode: dark
vibe: [luxury, minimal]
topics: [design, marketing]
extracted_at: 2026-07-08
tags:
  - vertical/studio-agency
  - vibe/luxury
  - vibe/minimal
  - topic/design
  - topic/marketing
  - mode/dark
---
# HEX Studio - Web, Marketing, Product & Brand Studio
> HEX is an experimental creative studio working on visually interesting identities, websites, and products. Led by Ayush Soni.  ·  [hex.inc](https://www.hex.inc/)

![hex.inc](../../screenshots/hexinc.png)

**Vertical:** #vertical/studio-agency  ·  **Vibe:** #vibe/luxury #vibe/minimal  ·  **Topics:** #topic/design #topic/marketing  ·  **Mode:** #mode/dark

## What it is
The site of HEX Studio, whose h1 reads 'HEX is a full-cycle creative studio for technology companies.' and whose meta description is 'HEX is an experimental creative studio working on visually interesting identities, websites, and products. Led by Ayush Soni.' Ayush Soni — the tweet's author — runs the studio; the tweet's 'Unsigned' brand study is a taste of the work this site collects.

## What it shows
A giant 'HEX' wordmark and hero, then a long 'select case studies:' scroll of colourful video/image reels for AI and tech startups — Composio, Inference, Detail, First Star, Founders Inc, Anthrogen, Plasticity, Sequence, Default.com, Moonlake and Tensorlake ('The Engine for Agentic Work'), alongside client logos for Grafana, exa, Framer, Replo, whop and OpenSea. Below sits a stats band (1,192,201 / 150+ / 42 / $1B+ / 1M+), a 'writings' article grid ('Process Breakdown: Plasticity Brand & Website', 'Website Design and Development for Default.com', 'Creamier Branding Process Breakdown', 'Brand Strategy & Identity: Wayfinder Ventures'), an FAQ, and a closing 'When you work with HEX, you work with the best of the best…' statement over a repeated HEX footer wordmark.

## How it works
A Webflow site (Webflow global present; markup, CSS and jQuery served from cdn.prod.website-files.com and Webflow's cloudfront JS bundle). The ~19 case-study reels stream as .mp4/.mov from Cloudflare R2 buckets (*.r2.dev) with the Vimeo player API also loaded. It is heavily instrumented: Google Tag Manager + GA4, PostHog (with session-recording, surveys and dead-click autocapture), a Meta/Facebook Pixel, Visitors.now and Google reCAPTCHA. Media mix is 86 <img>, 19 <video>, 2 <svg>, 0 canvas/iframe over a very long 14,683px scroll (~94 requests).

## How it's designed
A confident dark, near-monochrome frame that lets the colourful client reels pop. getComputedStyle reports a dark teal-green body background rgb(3,27,29) — the exposed CSS var --hex-dark-green #031b1d — with near-white body text rgb(235,235,235) (--white #ebebeb) and the h1 rendered in neon-mint rgb(33,255,188) (--hex-green #21ffbc); the primary CTA ('Get in touch') is a solid-white pill with dark-green text. The design system publishes its palette as :root vars (--hex-green #21ffbc, --hex-dark-green #031b1d, --medium-aquamarine #05d194, --hex-light-green/--white #ebebeb). Type is TWK Lausanne (loaded 300/400/500/700) as the workhorse sans; GT Alpina is declared as a serif display but reports unloaded on the homepage, and Webflow's default Open Sans / Oswald / Changa One families are declared but unloaded.

## Design data
- **Palette:** Dark teal-green canvas (--hex-dark-green #031b1d) with near-white text (#ebebeb) and a neon-mint accent (--hex-green #21ffbc); solid-white pill CTAs — saturation comes from the colourful case-study reels.
- **Palette tokens:** --hex-green: #21ffbc (var), --hex-dark-green: #031b1d (var), --medium-aquamarine: #05d194 (var), --white: #ebebeb (var), body background: rgb(3, 27, 29) (rendered), body text: rgb(235, 235, 235) (rendered), h1: rgb(33, 255, 188) (rendered), primary button bg: rgb(255, 255, 255) (rendered)
- **Fonts:** TWK Lausanne (loaded 300/400/500/700) as the workhorse sans; GT Alpina declared as a display serif but unloaded on the homepage; Webflow's Open Sans / Oswald / Changa One defaults declared but unloaded.
- **Fonts loaded:** Lausanne 300, Lausanne 400, Lausanne 500, Lausanne 700
- **Tech stack:** Webflow, jQuery, Cloudflare R2 (video), Vimeo, PostHog, Google Tag Manager / GA4, Meta Pixel, Visitors.now, reCAPTCHA
- **Keywords:** creative-studio, portfolio, dark, teal-green, neon-mint, case-study-reels, webflow, lausanne, video-heavy, monochrome-frame
- **Media mix:** img 86 · video 19 · svg 2
- **Page height:** 14683px (single-screen: False)
- **Responsive:** At 390x844 Webflow swaps in its burger nav (w-nav-button) and the case-study / stats / writings grid reflows to a single column (scrollHeight 14,683 -> 9,539px).
- **Headings:** HEX is a full-cycle creative studio for technology companies. / select case studies: / 1,192,201 / 150+ / 42 / $1B+ / 1M+ / writings / Process Breakdown: Plasticity Brand & Website / Website Design and Development for Default.com / Creamier Branding Process Breakdown / Brand Strategy & Identity: Wayfinder Ventures / When you work with HEX, you work with the best of the best. Because we care. We care about quality, we put in the effort and we move the needle forward for the people who trust us. We work on all creative projects - websites, brands, products, stores, apps, events, illustrations. And we do it for the people who value craft - the game changers and the big thinkers.
- **Links out:** [Get in touch](https://www.hex.inc/contact)
- **Weight:** 94 requests; hosts: www.hex.inc, cdn.prod.website-files.com, *.r2.dev (Cloudflare R2 video), player.vimeo.com, us-assets.i.posthog.com, www.googletagmanager.com, connect.facebook.net, cdn.visitors.now, fonts.googleapis.com, d3e54v103j8qbb.cloudfront.net, www.google.com (reCAPTCHA)
- **Extracted:** 2026-07-08 · Playwright MCP, 1440x900 fullPage + 390x844 mobile probe; logged_out: true.

## Related sites
- [[ddlabstudio.com]] — shared: studio-agency, luxury, design, marketing, dark
- [[vanschneider.com]] — shared: studio-agency, luxury, design, dark
- [[coldiq.com]] — shared: studio-agency, luxury, marketing
- [[drafts9.com]] — shared: studio-agency, minimal, design
- [[hiivearts.com]] — shared: studio-agency, minimal, marketing
- [[northgarden.com]] — shared: studio-agency, minimal, design
