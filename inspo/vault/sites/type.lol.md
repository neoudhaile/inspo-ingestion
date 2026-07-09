---
url: https://type.lol/
title: "Discover – type.lol"
category: uncategorized
aesthetics: [editorial, minimal]
tags: [type-directory, foundries, editorial, monochrome, react, custom-fonts, specimen-iframes, minimal]
extracted_at: 2026-07-08
---
# Discover – type.lol
> Discover and explore independent type foundries from around the world. Browse 1,100+ foundries, 14,000+ typefaces, and 1,600+ designers.  ·  [type.lol](https://type.lol/)

![type.lol](../../../screenshots/typelol.png)

**What it is** — A discovery directory for independent type foundries. The h1 is 'Discover type from independent foundries' and the meta description reads 'Discover and explore independent type foundries from around the world. Browse 1,100+ foundries, 14,000+ typefaces, and 1,600+ designers.'

**What it shows** — A crisp black-on-white editorial index of foundries and typefaces, using live type specimens embedded via <iframe> (5 iframes) and a large set of inline <svg> UI marks (49), grouped under section headings like 'Feeling Modern' with a 'Newsletter' block.

**How it works** — A React application (a React root is present) served entirely from its own domain — the probe found no third-party analytics or CDN script hosts, only type.lol — which fits a self-published indie project. Type specimens render in sandboxed iframes so each foundry's own fonts can load in isolation.

**How it's designed** — A restrained monochrome editorial system: getComputedStyle reports a white body background rgb(255,255,255) with near-black text rgb(9,9,11). The typography is, fittingly, entirely bespoke — document.fonts confirms the variable 'GORP Serif' (100–900) loaded as the primary family, with 'Covik Sans Mono', 'Retain' and 'ProGORP' also declared. The semantic <h1> is a small 18px label; the visual weight lives in the specimen previews rather than a giant hero headline. The only :root token is --ease-default: ease.

**Palette** — White canvas, near-black text (rgb 9,9,11); a deliberately monochrome shell so the foundry specimens provide any colour.
**Fonts** — Bespoke type throughout — variable 'GORP Serif' (100–900) loaded as the primary family, with 'Covik Sans Mono', 'Retain' and 'ProGORP' also declared; individual foundry specimens load their own fonts inside iframes.

## Connections
**Aesthetics:** [[aesthetics/editorial|editorial]] [[aesthetics/minimal|minimal]]
**Patterns:** `type-directory` `foundries` [[patterns/editorial|editorial]] [[patterns/monochrome|monochrome]] [[patterns/react|react]] `custom-fonts` `specimen-iframes` [[patterns/minimal|minimal]]
**Category:** [[categories/uncategorized|uncategorized]]
**Tech:** [[tech/react|React]] `Self-hosted (no third-party analytics or CDN scripts detected)`
**Colors:** [[colors/monochrome|monochrome]]
**Fonts:** `GORP Serif (variable 100-900)`

## Related sites
[[sites/animations.dev|animations.dev]] [[sites/asekachov.com|asekachov.com]] [[sites/daviskeene.com|daviskeene.com]] [[sites/designengineer.tools|designengineer.tools]] [[sites/eko.lumaris.works|eko.lumaris.works]]
