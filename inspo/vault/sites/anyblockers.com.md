---
url: https://anyblockers.com/
title: "anyblockers"
category: tutorial
aesthetics: [editorial, light, minimal]
tags: [personal-blog, digital-garden, serif-editorial, chronological-index, read-time-labels, light-mode, minimalist, text-only, newsletter-embed]
extracted_at: 2026-06-05
---
# anyblockers
> I'm Eric, currently working on the future of developer tooling at Cursor.  ·  [anyblockers.com](https://anyblockers.com/)

![anyblockers.com](../../../screenshots/anyblockerscom.png)

**What it is** — The personal site / writing blog of eric zakariasson, the author of the tweet — a developer at Cursor. The opening line is the whole identity: 'I'm Eric, currently working on the future of developer tooling at Cursor. My days are spent thinking about how developer experience evolves in an AI-native world.' This is the author's portfolio, not the subject of the bookmark; it's a reverse-chronological essay index.

**What it shows** — A narrow, centered single column: a three-paragraph intro (with inline links to Cursor and Twitter) followed by a year-grouped list of posts (2026, 2025, 2024). Each entry is a serif title plus a read-time and a right-aligned date — e.g. 'Working with coding agents' (8 min read), 'GPT-5 Prompting Guide (with OpenAI)', 'How we systematically analyze user feedback with LLMs' (18 min read), 'Postgres as a search engine', 'Building RAG with Postgres'. A small footer toolbar holds theme toggle, X, GitHub, LinkedIn and RSS.

**How it works** — A pure index-and-read blog: scroll the chronological list and click a title to read the essay. Outbound chrome is minimal — the footer toolbar links to social profiles and the RSS feed, and a theme toggle switches light/dark. A newsletter is wired in via an embedded beehiiv widget. There's no nav bar beyond the inline intro links; the page is one quiet ~1,252px scroll.

**How it's designed** — An intentionally bookish, almost-no-chrome reading layout: a warm off-white paper ground (#fdfcfb) with soft near-black ink (rgba(26,24,15,0.8)) set in Apple's 'New York' serif (the only loaded webface) for a literary, print-essay feel. There are zero images in the body (img: 0; the 6 SVGs are footer icons) — text carries everything. Built on Tailwind (full --tw-* token set present) with Shiki for code highlighting (--shiki-dark-bg / --code-gutter-width vars), PostHog for analytics, and a beehiiv newsletter embed. The serif + generous measure + year headers make it read like a quiet digital garden.

**Palette** — Warm off-white paper (#fdfcfb) with soft near-black ink (rgba(26,24,15,0.8)); grey hairline borders (rgb(229,231,235)); no chromatic accent.
**Fonts** — Apple 'New York' serif (system-served) for everything; no display face.

## Connections
**Aesthetics:** [[aesthetics/editorial|editorial]] [[aesthetics/light|light]] [[aesthetics/minimal|minimal]]
**Patterns:** [[patterns/personal-blog|personal-blog]] `digital-garden` `serif-editorial` `chronological-index` `read-time-labels` [[patterns/light-mode|light-mode]] [[patterns/minimalist|minimalist]] [[patterns/text-only|text-only]] `newsletter-embed`
**Category:** [[categories/tutorial|tutorial]]
**Tech:** [[tech/tailwind-css|Tailwind CSS]] `Shiki (code highlighting)` [[tech/posthog|PostHog]] `beehiiv (newsletter embed)`
**Colors:** [[colors/light|light]] [[colors/warm|warm]]
**Fonts:** `New York`

## Related sites
[[sites/amanml.com|amanml.com]] [[sites/axiaisacat.indiehacker.bio|axiaisacat.indiehacker.bio]] [[sites/daryl.cv|daryl.cv]] [[sites/designrebuilds.vercel.app|designrebuilds.vercel.app]] [[sites/noahzender.com|noahzender.com]]
