---
url: http://nskyc.com
domain: nskyc.com
title: "NYC Sky Color (nskyc.com)"
vertical: unclassified
mode: 
vibe: []
topics: []
extracted_at: 2026-07-10
tags:
---
# NYC Sky Color (nskyc.com)
> unavailable — not captured this run (Playwright MCP outage; see extracted_via).  ·  [nskyc.com](http://nskyc.com)


**Vertical:** #unclassified  ·  **Vibe:** —  ·  **Topics:** —  ·  **Mode:** —

## What it is
NYC Sky Color (nskyc.com) — the 'average color of the avg NYC sky' site the tweet links to: a single-purpose page that samples New York City's sky and displays the current average color as a full-bleed swatch, refreshing as the sky changes through the day. WebFetch returned HTTP 403 (the page is live but blocks non-browser fetchers), so this is grounded in the tweet's own gloss, not a direct fetch.

## What it shows
Not captured — no screenshot or DOM probe this run (see extracted_via).

## How it works
Not captured.

## How it's designed
Not captured — no getComputedStyle / document.fonts / CSS-variable data was obtainable without a live browser, so no color or font claims are made.

## Design data
- **Palette:** unavailable — blocked by the Playwright MCP outage this run.
- **Fonts:** unavailable — blocked by the Playwright MCP outage this run.
- **Fonts loaded:** system only (no webfont)
- **Tech stack:** Blocked non-browser fetchers with HTTP 403 (WebFetch); site is reachable, just not scriptable without a real browser.
- **Keywords:** single-purpose, color-swatch, generative-art, nyc, not-captured
- **Media mix:** 
- **Responsive:** unavailable — site not probed (Playwright MCP outage this run).
- **Extracted:** 2026-07-10 · Playwright MCP was unavailable this whole run: the daemon's --mcp-config launches `npx @playwright/mcp@latest`, which now requires Node >=20, but tools/ingest/enrich.sh and the launchd plist pinned PATH to Node v18.20.8, so the MCP server printed a version error and exited before connecting — browser tools never came up (root-caused and fixed in this same commit; see ITERATIONS.md). No screenshot or DOM probe was possible for any teardown_domain this run; entries below are grounded in WebFetch text-fetches and the tweet's own text/media where available, never in eyeballed colors or fonts.

## Related sites
—
