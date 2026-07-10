---
url: https://www.drafts9.com/
domain: drafts9.com
title: "Drafts9 — Full stack design and dev partner for startups"
vertical: studio-agency
mode: light
vibe: [corporate-clean, minimal]
topics: [design, startups]
extracted_at: 2026-06-06
tags:
  - vertical/studio-agency
  - vibe/corporate-clean
  - vibe/minimal
  - topic/design
  - topic/startups
  - mode/light
---
# Drafts9 — Full stack design and dev partner for startups
> Full stack design and dev partner for startups.  ·  [drafts9.com](https://www.drafts9.com/)

![drafts9.com](../../screenshots/drafts9com.png)

**Vertical:** #vertical/studio-agency  ·  **Vibe:** #vibe/corporate-clean #vibe/minimal  ·  **Topics:** #topic/design #topic/startups  ·  **Mode:** #mode/light

## What it is
Drafts9 is the studio site of designer/developer Ahmed Hassan (@uihssn) — a 'full stack design and dev partner for startups' that ships premium websites, landing pages, brands, products, and no-code experiences on monthly plans. It's the home base behind the 'Dreamblur Gradients' background library the bookmarked tweet is promoting.

## What it shows
A long single-page pitch: a hero headline ('Full stack design and dev partner for startups.') with 'Book a call' and 'Send a message' CTAs, a horizontally-scrolling carousel of recent work (a data-workspace product UI, polished travel/nature landing pages), a 'Trusted by startups and industry leaders' logo strip, a testimonials carousel that includes short video testimonials, a 'What we're best at' capabilities section, a 'Simple monthly plans for fast-moving startups' pricing block, an FAQ ('Questions founders usually ask'), and a closing 'Let's build something cool.' contact section.

## How it works
A static, hand-built marketing page — no JS framework signature was detected (no __NEXT_DATA__, __NUXT__, or React/Vue/Svelte roots; document.scripts exposed no external hosts). Content is scroll-revealed, so most below-the-fold sections render blank in a static full-page capture until scrolled into view. Three self-hosted MP4s (video-01/02/03.mp4, served via HTTP 206 range requests) power the video testimonials, and the work showcase is a manual carousel with prev/next arrows and slide dots. Primary actions route off-site: 'Book a call' → Calendly, 'Send a message' → WhatsApp (wa.me), 'Recent work' → a Figma prototype.

## How it's designed
Unapologetically Apple-flavored. The palette is built on Apple's own system: parchment/pearl off-whites (--canvas-parchment #f5f5f7, --surface-pearl #fafafc) against near-black ink (--ink #1d1d1f) with Apple blue accents (--primary #0066cc, --primary-focus #0071e3). Despite loading Inter, Instrument Serif, Archivo Black and DM Mono from Google Fonts, the body and the 56px/600 hero headline actually render in the Apple system stack (-apple-system / SF Pro Text / SF Pro Display) — only Instrument Serif reports as loaded, so most of the declared webfont payload appears unused on the home page. Generous 80px section rhythm, a 1440px max container, pill buttons, soft product shadows (0 30px 60px -25px rgba(0,0,0,.22)) and hairline dividers complete the calm, premium, conversion-focused feel.

## Design data
- **Palette:** Apple-system neutrals — parchment #f5f5f7 / pearl #fafafc surfaces, near-black ink #1d1d1f, muted grey body #86868b — with Apple blue #0066cc/#0071e3 CTAs.
- **Palette tokens:** --primary: #0066cc (var), --primary-focus: #0071e3 (var), --canvas: #ffffff (var), --canvas-parchment: #f5f5f7 (var), --surface-pearl: #fafafc (var), --ink: #1d1d1f (var), --body-muted: #86868b (var), --hairline: #e0e0e0 (var), body color: rgb(29, 29, 31) (rendered), body background: rgb(255, 255, 255) (rendered), h1 color: rgb(29, 29, 31) (rendered), button color: rgb(0, 102, 204) (rendered)
- **Fonts:** Renders in the Apple system stack (-apple-system / SF Pro Text / SF Pro Display) for body + hero; Instrument Serif is the one webfont actually loaded; Inter, Archivo Black and DM Mono are declared via Google Fonts but report unloaded on the home page.
- **Fonts loaded:** Instrument Serif 400
- **Tech stack:** Static HTML/CSS/JS (no framework detected), Google Fonts, self-hosted MP4 video, Calendly, WhatsApp, Figma (work prototype)
- **Keywords:** apple-style, studio, agency-landing, scroll-reveal, carousel, video-testimonials, pricing-tiers, faq, system-fonts, minimalist
- **Media mix:** img 20 · video 3 · svg 22
- **Page height:** 6268px (single-screen: False)
- **Responsive:** At 390x844 the layout stacks to a single column (page grows to ~7674px), the hero h1 scales down from 56px to 40px, and the minimal nav stays inline (logo + 'Recent work', no hamburger).
- **Headings:** Full stack design and dev partner for startups. / Trusted by startups and industry leaders. / What founders say about working with us. / What we're best at. / Simple monthly plans for fast-moving startups. / Questions founders usually ask. / Let's build something cool.
- **Links out:** [Book a call](https://calendly.com/drafts9/30min) · [Send a message](https://wa.me/923057597557) · [Recent work](https://www.figma.com/proto/oe90hxHoZuLbrp1xZ5Etjq/Drafts9-Work--Landing-pages) · [Email](mailto:hello.uihssn@gmail.com)
- **Weight:** 27 requests; hosts: www.drafts9.com, fonts.googleapis.com, fonts.gstatic.com
- **Extracted:** 2026-06-06 · Playwright MCP, 1440x900 + 390x844 mobile pass, logged_out: true

## Related sites
- [[ignytlabs.com]] — shared: studio-agency, corporate-clean, design, startups, light
- [[northgarden.com]] — shared: studio-agency, minimal, design, light
- [[offthewall.studio]] — shared: studio-agency, minimal, design, light
- [[ravalabs.com]] — shared: studio-agency, minimal, design, light
- [[rotimi.design]] — shared: studio-agency, minimal, design, light
- [[varickagents.com]] — shared: studio-agency, corporate-clean, startups, light
