---
url: https://motionsites.ai/
title: "MotionSites — Premium Hero Prompts"
category: tools-build
aesthetics: [dark, developer-product]
tags: [dark-saas, template-gallery, prompt-marketplace, copy-to-clipboard, freemium-paywall, filter-chips, animated-headline, lazy-loaded-grid, shadcn-radix, geo-pricing]
extracted_at: 2026-06-06
---
# MotionSites — Premium Hero Prompts
> Your Design AI Superpowers In One Click.  ·  [motionsites.ai](https://motionsites.ai/)

![motionsites.ai](../../../screenshots/motionsitesai.png)

**What it is** — A marketplace/library of ready-to-paste “premium hero prompts” for AI website builders — the pitch is literally “Unlock your AI Design Superpowers” and “Your Design AI Superpowers In One Click.” You browse a gallery of polished hero-section designs, copy the prompt behind one, paste it into your AI tool, and get an award-winning-looking landing page. It's run by DesignRocket (“Powered by DesignRocket”) as the prompt-pack arm of that design-education brand.

**What it shows** — A dark landing page with a big animated headline (“Unlock your AI Design Superpowers”) over a “Go Unlimited” CTA, then an enormous filterable gallery of hero-section templates — cards like “3D Portfolio,” “Pulse 3D,” “Design Rocket,” “Inner Circle,” “Prisma” — each a rich preview thumbnail with Copy / Premium badges and Type/Mixed filter chips. The page is extremely media-dense (333 <img>, 167 <svg>, 2 <video>) and very long (scrollHeight ~17.6k px) because it lazy-loads the full catalog.

**How it works** — Top nav splits the catalog into Sections / Backgrounds plus Contact and Pricing, with a Type/Mixed filter row above the grid to narrow templates. Each card exposes a Copy action (grab the prompt) gated by free vs Premium, and the whole thing pushes toward “Go Unlimited” (a paywall managed via ParityDeals geo-pricing). A Meta Pixel tracks conversions. It's a single long scroll — the gallery streams in as you go — with hover states on the cards and CTAs.

**How it's designed** — A dark, product-y SaaS look: near-black ground (rendered body bg rgb 23,23,23) with off-white text (rgb 245,245,245) and a single vivid blue brand color (--primary hsl 230 100% 55%) for rings/CTAs, on a generous 1rem corner radius. It's a React app built on the shadcn/Radix token system (the :root carries the full --background/--card/--primary/--sidebar HSL set, and Radix portal ids appear in the DOM) and was produced with Lovable / gpt-engineer (its OG image lives under gpt-engineer-file-uploads). Notably the heavy display headline renders in the system UI sans stack — a Google Fonts stylesheet is linked but document.fonts reports nothing loaded on the sampled nodes — so the drama comes from scale (56px/900) and motion, not a webfont. The card thumbnails carry the visual weight.

**Palette** — Near-black ground (rgb 23/23/23), off-white text (rgb 245/245/245), single vivid blue brand accent (--primary hsl 230 100% 55%); 1rem radius.
**Fonts** — System UI sans on the sampled text (Google Fonts linked but no webfont loaded on these nodes); display drama is size+weight (56px/900), not a typeface.

## Connections
**Aesthetics:** [[aesthetics/dark|dark]] [[aesthetics/developer-product|developer-product]]
**Patterns:** `dark-saas` `template-gallery` `prompt-marketplace` `copy-to-clipboard` `freemium-paywall` `filter-chips` `animated-headline` `lazy-loaded-grid` `shadcn-radix` `geo-pricing`
**Category:** [[categories/tools-build|tools-build]]
**Tech:** [[tech/react|React]] `shadcn / Radix UI` `Lovable (gpt-engineer)` `ParityDeals (geo pricing)` [[tech/meta-pixel|Meta Pixel]] [[tech/jsdelivr|jsDelivr]]
**Colors:** [[colors/dark|dark]] [[colors/cool|cool]]
**Fonts:** [[fonts/system-fonts|system-fonts]]

## Related sites
[[sites/sceneai.art|sceneai.art]] [[sites/the-cafelist.com|the-cafelist.com]]
