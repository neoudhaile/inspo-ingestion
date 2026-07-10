---
url: https://www.hofai.io/
domain: hofai.io
title: "House of AI — Learn AI with projects and mentorship"
vertical: docs-resource
mode: mixed
vibe: [technical, playful]
topics: [ai, education]
extracted_at: 2026-06-06
tags:
  - vertical/docs-resource
  - vibe/technical
  - vibe/playful
  - topic/ai
  - topic/education
  - mode/mixed
---
# House of AI — Learn AI with projects and mentorship
> AI öğrenmenin en keyifli yolu. (the most enjoyable way to learn AI)  ·  [hofai.io](https://www.hofai.io/)

![hofai.io](../../screenshots/hofaiio.png)

**Vertical:** #vertical/docs-resource  ·  **Vibe:** #vibe/technical #vibe/playful  ·  **Topics:** #topic/ai #topic/education  ·  **Mode:** #mode/mixed

## What it is
House of AI (hofai.io) is a Turkish-language AI-learning platform. Its meta description pitches it plainly: “Learn Claude, ChatGPT, Gemini and modern AI tools through guided projects. Your AI mentor reviews assignments. Try 3 days free, then $14.99/mo.” It's a paid, mentor-reviewed, project-based course product — bookmarked via a Turkish thread by its maker (“digital ghost”) about spending six hours with Claude to erase a personal digital footprint.

## What it shows
A dark, single-scroll marketing page. The body renders near-black (rgb 5,5,7) with off-white text (rgb 240,240,242), but the hero sits on a light block where the h1 — “AI öğrenmenin en keyifli yolu.” — renders in dark brown (rgb 31,22,17) at 88px. Scrolling steps through the pitch via its Turkish h2s: “Üç adımda ilk ödevin.” (your first assignment in three steps), “Her büyük AI aracı için, kendi yolu.” (a path per major AI tool), “Cebinde bir özel öğretmen.” (a private tutor in your pocket), “Bir oyun gibi bağımlılık yapan öğrenme.” (game-like, addictive learning), “12 haftada sıfırdan gerçek projelere.” (zero to real projects in 12 weeks), then objection-handling, social proof, transparent pricing, FAQ and a final CTA. Light on media: 8 img, 4 svg, no video or canvas.

## How it works
A conventional SaaS landing flow on one long page (desktop scrollHeight ~10912): hero → three-step onboarding → per-tool tracks → mobile-tutor angle → gamified learning → a 12-week curriculum → testimonials → simple pricing ($14.99/mo after a 3-day free trial) → FAQ → sign-up CTA. It loads only self-hosted scripts plus Google Tag Manager — no heavy third-party stack.

## How it's designed
A warm dark theme built on Tailwind v4: the CSS exposes lab() color tokens, a full --color-* ramp (amber/cyan/purple/emerald), a --surface-lowest of #050507 and a warm-tan --sidebar-accent-foreground of #e0b88a; cards/borders use translucent white (--card #ffffff12, --border #ffffff1f). Type is Geist for headings and body (h1 88px) with Instrument Serif loaded as an editorial accent and JetBrains Mono for code. No framework global is present (__NUXT__, __NEXT_DATA__, data-v-app and a React root are all absent), so it reads as a custom SSR/static build rather than a named meta-framework.

## Design data
- **Palette:** Near-black canvas (rendered rgb 5/5/7) with off-white text (rgb 240/240/242); warm-tan accent (--sidebar-accent-foreground #e0b88a) over amber/cyan/purple/emerald token ramps; hero block flips to a light ground with dark-brown headline (rgb 31/22/17).
- **Palette tokens:** body-bg: rgb(5, 5, 7) (rendered), body-text: rgb(240, 240, 242) (rendered), h1-color: rgb(31, 22, 17) (rendered), --surface-lowest: #050507 (var), --sidebar-accent-foreground: #e0b88a (var), --card: #ffffff12 (var), --card-foreground: #f0f0f2 (var)
- **Fonts:** Geist for headings + body (h1 88px), Instrument Serif as an editorial accent, JetBrains Mono for code (all loaded).
- **Fonts loaded:** Geist 100-900, Instrument Serif 400, JetBrains Mono 400
- **Tech stack:** Tailwind v4, Google Tag Manager
- **Keywords:** product-landing, saas-pricing, dark-theme, warm-accent, gamified-learning, single-scroll, turkish, tailwind-v4, ai-education
- **Media mix:** img 8 · svg 4
- **Page height:** 10912px (single-screen: False)
- **Responsive:** At 390x844 the hero h1 drops 88px→48px and the page reflows to a single column (scrollHeight 10912→16876); no hamburger detected, the nav stays block-level.
- **Headings:** AI öğrenmenin en keyifli yolu. / Üç adımda ilk ödevin. / Her büyük AI aracı için, kendi yolu. / Cebinde bir özel öğretmen. / Bir oyun gibi bağımlılık yapan öğrenme. / 12 haftada sıfırdan gerçek projelere. / “ChatGPT aboneliğim var zaten.” / Onlar başardı. Sıra sende. / Basit fiyat. Şeffaf koşullar. / Aklındaki her şey. / AI ile yeniden başla.
- **Extracted:** 2026-06-06 · playwright-mcp @ 1440x900 (+ 390x844 mobile), logged_out: true

## Related sites
- [[heyneuma.com]] — shared: docs-resource, ai, education
- [[midu.dev]] — shared: docs-resource, playful, education
- [[walkinglabs.github.io]] — shared: docs-resource, ai, education
- [[cofounder.co]] — shared: technical, ai, mixed
- [[makingsoftware.com]] — shared: docs-resource, technical
- [[transitions.dev]] — shared: docs-resource, technical
