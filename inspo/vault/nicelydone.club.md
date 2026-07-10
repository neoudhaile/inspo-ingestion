---
url: https://nicelydone.club/
domain: nicelydone.club
title: "Nicelydone — web apps design inspiration (UX & UI)"
vertical: directory-gallery
mode: light
vibe: [minimal, corporate-clean]
topics: [design]
extracted_at: 2026-07-05
tags:
  - vertical/directory-gallery
  - vibe/minimal
  - vibe/corporate-clean
  - topic/design
  - mode/light
---
# Nicelydone — web apps design inspiration (UX & UI)
> Ship faster with proven UX flows from the world's best apps.  ·  [nicelydone.club](https://nicelydone.club/)

![nicelydone.club](../../screenshots/nicelydoneclub.png)

**Vertical:** #vertical/directory-gallery  ·  **Vibe:** #vibe/minimal #vibe/corporate-clean  ·  **Topics:** #topic/design  ·  **Mode:** #mode/light

## What it is
Nicelydone — 'Web apps design inspiration (UX & UI)': a searchable library of 237,100+ real UI screenshots from 500+ SaaS apps (pricing pages, onboarding flows, settings screens…), 'searchable like Google, draggable into Figma.' It's a product of Bertrand Bruandet's Forwards Labs and one of the two design directories his '10 great websites' tweet points to.

## What it shows
A long marketing landing page (~6,356px). The hero h1 'Ship faster with proven UX flows from the world's best apps' sits over sections 'Sound familiar?', 'Research in seconds, not hours', 'The old way vs. your new workflow', 'What designers are saying', 'Built for teams that actually ship' and 'The largest library of real SaaS UI', plus an MCP integration, Pricing and a Stripe-backed 'Try it free' CTA.

## How it works
A Nuxt UI / Tailwind-v4 token system (--ui-* and --container tokens on :root; the runtime global wasn't exposed) with assets served from Bertrand's own coquelicot.forwardslabs.com. The commerce/growth stack is Stripe (js.stripe.com), a Tolt affiliate script (cdn.tolt.io), PostHog analytics (eu-assets.i.posthog.com), Cloudflare Insights and jsDelivr. 18 img, 2 iframe.

## How it's designed
A clean, near-monochrome SaaS-marketing look. From :root the canvas is white (--ui-bg = var(--color-white)) with a natural-gray text ramp (body/h1 rgb(49,49,48) ≈ naturalgray-900, muted UI text rgb(78,80,96)) and a hairline border (--color-border #1c1d2226); status colours are defined in OKLCH (success/info/warning/error). The display face is 'Klaus' (a warm, characterful sans at weight 600–700; the h1 is 52.8px) set against a system-ui body stack.

## Design data
- **Palette:** White with a natural-gray text ramp (near-black rgb(49,49,48) headings, rgb(78,80,96) UI text), a #1c1d2226 hairline border and OKLCH status colours — restrained so the app screenshots pop.
- **Palette tokens:** --color-border: #1c1d2226 (var), --ui-success: oklch(75.687% .19947 129.548) (var), --ui-info: oklch(67.748% .15628 247.903) (var), body color: rgb(49, 49, 48) (rendered), button text: rgb(78, 80, 96) (rendered), body background: rgb(255, 255, 255) (rendered)
- **Fonts:** 'Klaus' (a display sans, 600–700) for headings, with a system-ui stack for body.
- **Fonts loaded:** Klaus 600
- **Tech stack:** Nuxt UI / Tailwind v4, Stripe, PostHog, Tolt (affiliate), Cloudflare
- **Keywords:** directory, saas-ui, design-inspiration, search-tool, nuxt-ui, tailwind-v4, oklch, monochrome, marketing-landing
- **Media mix:** img 18 · svg 2 · iframe 2
- **Page height:** 6356px (single-screen: False)
- **Responsive:** At 390x844 the marketing sections reflow to a single column (the page grows ~6,356 → 8,421px); the top nav condenses inline rather than collapsing to a hamburger.
- **Headings:** Ship faster with proven UX flows from the world's best apps / Sound familiar? / Research in seconds, not hours / The old way vs. your new workflow / What designers are saying / Built for teams that actually ship / The largest library of real SaaS UI
- **Links out:** [Try it free](https://nicelydone.club/) · [Pricing](https://nicelydone.club/)
- **Weight:** None requests; hosts: coquelicot.forwardslabs.com, js.stripe.com, cdn.tolt.io, eu-assets.i.posthog.com, static.cloudflareinsights.com, cdn.jsdelivr.net
- **Extracted:** 2026-07-05 · Playwright MCP, 1440x900 + 390x844 mobile pass, logged_out: true

## Related sites
- [[21st.dev]] — shared: directory-gallery, minimal, design, light
- [[designengineer.tools]] — shared: directory-gallery, minimal, design, light
- [[designtools.fyi]] — shared: directory-gallery, minimal, design, light
- [[maxibestof.one]] — shared: directory-gallery, minimal, design, light
- [[recent.design]] — shared: directory-gallery, minimal, design, light
- [[type.lol]] — shared: directory-gallery, minimal, design, light
