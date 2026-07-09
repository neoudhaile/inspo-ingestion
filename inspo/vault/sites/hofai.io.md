---
url: https://www.hofai.io/
title: "House of AI — Learn AI with projects and mentorship"
category: tutorial
aesthetics: [developer-product, dark, playful]
tags: [product-landing, saas-pricing, dark-theme, warm-accent, gamified-learning, single-scroll, turkish, tailwind-v4, ai-education]
extracted_at: 2026-06-06
---
# House of AI — Learn AI with projects and mentorship
> AI öğrenmenin en keyifli yolu. (the most enjoyable way to learn AI)  ·  [hofai.io](https://www.hofai.io/)

![hofai.io](../../../screenshots/hofaiio.png)

**What it is** — House of AI (hofai.io) is a Turkish-language AI-learning platform. Its meta description pitches it plainly: “Learn Claude, ChatGPT, Gemini and modern AI tools through guided projects. Your AI mentor reviews assignments. Try 3 days free, then $14.99/mo.” It's a paid, mentor-reviewed, project-based course product — bookmarked via a Turkish thread by its maker (“digital ghost”) about spending six hours with Claude to erase a personal digital footprint.

**What it shows** — A dark, single-scroll marketing page. The body renders near-black (rgb 5,5,7) with off-white text (rgb 240,240,242), but the hero sits on a light block where the h1 — “AI öğrenmenin en keyifli yolu.” — renders in dark brown (rgb 31,22,17) at 88px. Scrolling steps through the pitch via its Turkish h2s: “Üç adımda ilk ödevin.” (your first assignment in three steps), “Her büyük AI aracı için, kendi yolu.” (a path per major AI tool), “Cebinde bir özel öğretmen.” (a private tutor in your pocket), “Bir oyun gibi bağımlılık yapan öğrenme.” (game-like, addictive learning), “12 haftada sıfırdan gerçek projelere.” (zero to real projects in 12 weeks), then objection-handling, social proof, transparent pricing, FAQ and a final CTA. Light on media: 8 img, 4 svg, no video or canvas.

**How it works** — A conventional SaaS landing flow on one long page (desktop scrollHeight ~10912): hero → three-step onboarding → per-tool tracks → mobile-tutor angle → gamified learning → a 12-week curriculum → testimonials → simple pricing ($14.99/mo after a 3-day free trial) → FAQ → sign-up CTA. It loads only self-hosted scripts plus Google Tag Manager — no heavy third-party stack.

**How it's designed** — A warm dark theme built on Tailwind v4: the CSS exposes lab() color tokens, a full --color-* ramp (amber/cyan/purple/emerald), a --surface-lowest of #050507 and a warm-tan --sidebar-accent-foreground of #e0b88a; cards/borders use translucent white (--card #ffffff12, --border #ffffff1f). Type is Geist for headings and body (h1 88px) with Instrument Serif loaded as an editorial accent and JetBrains Mono for code. No framework global is present (__NUXT__, __NEXT_DATA__, data-v-app and a React root are all absent), so it reads as a custom SSR/static build rather than a named meta-framework.

**Palette** — Near-black canvas (rendered rgb 5/5/7) with off-white text (rgb 240/240/242); warm-tan accent (--sidebar-accent-foreground #e0b88a) over amber/cyan/purple/emerald token ramps; hero block flips to a light ground with dark-brown headline (rgb 31/22/17).
**Fonts** — Geist for headings + body (h1 88px), Instrument Serif as an editorial accent, JetBrains Mono for code (all loaded).

## Connections
**Aesthetics:** [[aesthetics/developer-product|developer-product]] [[aesthetics/dark|dark]] [[aesthetics/playful|playful]]
**Patterns:** [[patterns/product-landing|product-landing]] `saas-pricing` [[patterns/dark-theme|dark-theme]] `warm-accent` `gamified-learning` [[patterns/single-scroll|single-scroll]] `turkish` [[patterns/tailwind-v4|tailwind-v4]] `ai-education`
**Category:** [[categories/tutorial|tutorial]]
**Tech:** [[tech/tailwind-v4|Tailwind v4]] [[tech/google-tag-manager|Google Tag Manager]]
**Colors:** [[colors/dark|dark]] [[colors/warm|warm]] [[colors/cool|cool]]
**Fonts:** [[fonts/geist-100-900|Geist 100-900]] [[fonts/instrument-serif|Instrument Serif]] [[fonts/jetbrains-mono|JetBrains Mono]]

## Related sites
[[sites/cofounder.co|cofounder.co]] [[sites/printingpress.dev|printingpress.dev]] [[sites/fey.com|fey.com]] [[sites/todesktop.com|todesktop.com]] [[sites/affiliatenetwork.com|affiliatenetwork.com]]
