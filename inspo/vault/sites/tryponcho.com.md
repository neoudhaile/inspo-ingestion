---
url: https://tryponcho.com/
title: "Poncho — 'AI agents with 3000+ tools': a dark, pay-per-use agent workspace"
category: product
aesthetics: [dark]
tags: [ai-agent, app-shell, dark, charcoal, cyan-accent, shadcn, tailwind, marketplace, pay-per-use, sidebar, geist]
extracted_at: 2026-07-08
---
# Poncho — 'AI agents with 3000+ tools': a dark, pay-per-use agent workspace
> Access 3000+ tools from one account with Poncho. Find data at machine speed, automate work, and skip setup, subscriptions, and API keys.  ·  [tryponcho.com](https://tryponcho.com/)

![tryponcho.com](../../../screenshots/tryponchocom.png)

**What it is** — The product itself, not a marketing splash: tryponcho.com loads straight into Poncho's logged-out app shell. The page title is 'Poncho - AI agents with 3000+ tools' and its meta description is 'Access 3000+ tools from one account with Poncho. Find data at machine speed, automate work, and skip setup, subscriptions, and API keys.' The link shafu shared (link.tryponcho.com/shafu0x) is a Dub-tracked referral that redirects to tryponcho.com/redeem/shafu0x; the subject site is the Poncho app.

**What it shows** — A dark charcoal workspace with a left sidebar (Poncho logo, New Chat, Search, Marketplace, Balance, Artifacts, Templates, Help & Resources, and a 'Poncho / Sign in to start free' footer). The main column headlines 'Put Poncho to Work' with a cyan 'Get Started' button and a large 'What do you need done?' chat input (cyan focus ring). Below it a 'Marketplace' rail ('Use thousands of pay-per-use services - no subscriptions required') with category chips (Creative Production, Data Analytics, GTM, Local Lead Machine, Public Equity Investing, Sales, Social Media Intel), a 'Popular Tasks' list (Audit content performance, Shape positioning routes, 'Agencies: Businesses Paying for Ads on a Broken Site', Build an analytical report, Earnings Deep-Dive) and a 'Services' section (e.g. 'StableEnrich - Pay-per-request access to Apollo, Clado, Exa, Firecrawl, Google Maps, Serper, and Whitepages APIs. No auth, no subscriptions.').

**How it works** — A React-style single-page app built on shadcn/ui + Tailwind: :root carries the full shadcn token set in oklch (--background, --foreground, --card, --primary, --ring, --sidebar-*, --chart-*). Auth is Privy (a large --privy-* token block is injected), payments are Stripe (js.stripe.com), links are tracked via Dub (www.dubcdn.com - matching the dub_id on the shared redeem URL), and analytics via Google Tag Manager; the app talks to its own backend at barn.tryponcho.com. No public framework global (__NEXT_DATA__ etc.) is exposed. Media: 14 <img>, 33 <svg>, 4 <iframe> (auth/payment embeds), 0 canvas/video; KaTeX fonts are declared (for math in chat answers) but unloaded.

**How it's designed** — A restrained, developer-tool dark UI where a single cyan accent does the pointing. getComputedStyle/CSS vars report a warm charcoal canvas --background oklch(26.79% .0036 106.643) with near-white --foreground oklch(92% .0041 91.45); the interactive accent --primary/--ring is a cyan oklch(62.67% .1089 211.73) (the Get Started button and input focus ring), while the Poncho brand mark uses a red --brand oklch(63.68% .2078 25.3313). Type is Geist Variable (loaded) with Geist Mono Variable declared; corners are soft (--radius .5rem) and shadows are subtle - a clean shadcn baseline dressed in warm-grey + cyan.

**Palette** — Warm charcoal canvas (oklch 26.79% ~= near-black grey) with near-white text, a single cyan primary/focus accent (oklch 62.67% .1089 211.73) and a red brand mark (oklch 63.68% .2078 25.3313).
**Fonts** — Geist Variable (loaded, 100-900) for UI; Geist Mono Variable declared but unloaded; a full KaTeX family declared (math rendering) but unloaded. No other webfont payload.

## Connections
**Aesthetics:** [[aesthetics/dark|dark]]
**Patterns:** `ai-agent` `app-shell` [[patterns/dark|dark]] `charcoal` `cyan-accent` [[patterns/shadcn|shadcn]] [[patterns/tailwind|tailwind]] [[patterns/marketplace|marketplace]] `pay-per-use` `sidebar` [[patterns/geist|geist]]
**Category:** [[categories/product|product]]
**Tech:** `shadcn/ui + Tailwind (oklch tokens)` `Privy (auth)` `Stripe (payments)` `Dub (link tracking)` [[tech/google-tag-manager|Google Tag Manager]]
**Colors:** [[colors/dark|dark]] [[colors/warm|warm]] [[colors/cool|cool]]
**Fonts:** `Geist Variable 100-900`

## Related sites
[[sites/eko.lumaris.works|eko.lumaris.works]] [[sites/heyneuma.com|heyneuma.com]] [[sites/nicolasbustamante.com|nicolasbustamante.com]] [[sites/sceneai.art|sceneai.art]] [[sites/tyronec.com|tyronec.com]]
