# Bookmark enrichment

You are given `inspo/_inbox/new-items.json`. Produce `inspo/_inbox/enriched-items.json`
with the schema below. Use the Playwright MCP for link resolution AND teardowns. The
Playwright browser runs **isolated and logged out of X**, so tweet *replies* are usually
not visible — rely on the tweet body + export metadata for links, and treat any reply
links as a best-effort bonus.

## Rules

0. **Direct URL submissions:** items with `"source": "manual-url"` are not tweets — they
   are URLs submitted directly (pasted link, browser bookmark, another app). Skip the
   tweet-opening (2b) and media (6) steps; the given URL IS the subject: set it as
   `primary_url` and ALWAYS include its domain in `teardown_domains` (that's why it was
   submitted). If the URL is a specific page (not the homepage), tear down THAT page —
   and ALSO open the domain root, because the essence (7e) must say both what was
   shared and what site it lives on.
   Copy the null author/tweet fields through unchanged.

1. **Keep every item.** Never drop one. Link-free items still get a title, category, tags.

2. **Resolve every link to its REAL destination.** Tweets only contain `t.co` stubs.
   For each item:
   a. Start from `all_urls` (these are already expanded to real URLs from the export
      metadata — this is your primary source and works without any login).
   b. Best-effort: open the `tweet` URL with Playwright to confirm the real destination
      (the link text shows the true domain) and pick up any extra links visible on the
      main tweet. The browser is logged out, so author replies usually won't render —
      do not block or fail on missing replies.
   c. Union everything into `all_urls` (deduped, real URLs — never leave a bare `t.co`).
   d. Record provenance in `resolved_links`: one object per link
      `{ "raw": "<t.co or as-seen>", "resolved": "<final url>", "role": "primary|author-portfolio|related|reply-link", "source": "tweet-body|reply|metadata" }`.

3. **Primary URL:** choose the subject site (the thing the tweet is actually about) from
   the resolved links — never a `t.co`, never a utility/aggregator (linktr.ee, cal.com,
   calendly, typefully, medium, docs.google, substack root, bare github/youtube). If a
   tweet showcases a site AND links the author's portfolio, the showcased site is primary;
   demote the rest to `related_urls`. If nothing qualifies, set `primary_url`/
   `primary_domain` to null and tag accordingly (e.g. `uncategorized`).

4. **List tweets** (many sites in one tweet/thread): keep one item; put every site in
   `all_urls`/`related_urls`; tag `directory`/`thread`; mark each design-worthy domain in
   `teardown_domains`.

5. **Category** ∈ the existing set in `inspiration.json.meta.categories`.
   **Tags** drawn from `meta.all_tags` (you may add new tags when warranted).

6. **Attached media — view it and describe what it showcases.** For EVERY item that has
   a non-empty `media` array, look at each media item and add a one–two sentence
   `description` to that entry capturing the cool thing being shown (a UI, a product, an
   animation, an artwork, a place). Many bookmarks have NO link and the showcase lives
   entirely in the media, so this is the only signal — do it for every media item.
   - **Photo:** run `bash tools/ingest/fetch_image.sh "<original_url>" "<id>-<n>"`; it
     prints a local path. `Read` that file to view the image, then describe it.
   - **Video:** `browser_navigate` to the video's `original_url` (Chromium decodes H.264;
     the bundled ffmpeg cannot). Run a `browser_evaluate` that waits for metadata, reads
     `duration`, and seeks the `<video>` to ~25% of duration; take a screenshot; repeat the
     seek+screenshot at ~55% and ~85% (3 frames total). View the frames and describe the
     motion / sequence / what's demoed across the clip. If seeking fails, fall back to
     `fetch_image.sh "<thumbnail_url>" "<id>-<n>"` and describe that poster still.
   Keep descriptions about the CONTENT shown, not the video player chrome. Preserve each
   entry's `type`/`original_url`/`thumbnail_url`; just add `description`.

7. **Teardown:** for each domain in `teardown_domains`, navigate to its REAL resolved URL
   at 1440×900. Skip domains that fail to load; do not block other items. Steps:

   a. **Capture:** take one `browser_take_screenshot` with `fullPage: true` saved as
      `screenshots/<domain-without-dots>.png` (relative to the repo root, i.e. the
      bookmark-ingestion dir); set the entry's `screenshot` field to that same relative
      path. Do a hover and a scroll.

   b. **DOM probe (MANDATORY — run ONE `browser_evaluate` on the loaded page):** return a
      JSON object with: `meta` (title, description, og:image, twitter:card, canonical,
      favicon href), `:root` CSS custom properties (`--*`), `[...document.fonts]` (family +
      weight + status), sampled rendered colors via `getComputedStyle` on `html/body`, the
      `<h1>`, a primary button, and any accent element (return real rgb values), element
      counts `{img, canvas, video, svg, iframe}`, all `<h1>`/`<h2>` text, `scrollHeight` and
      `innerHeight`, framework globals present (`__NUXT__`, `__NEXT_DATA__`, `data-v-app`,
      `__sveltekit`, React root, etc.), and unique `document.scripts` + stylesheet hostnames
      (for tech/analytics/font-CDN detection).

   c. **Mobile pass (cheap, text-first):** `browser_resize(390, 844)`, run a small
      `browser_evaluate` capturing how layout changed (nav collapsed? columns reflowed?
      hidden/added elements? new scrollHeight), then `browser_resize(1440, 900)` back. One
      sentence in `responsive_note`. A mobile screenshot is OPTIONAL — only take one if the
      mobile design is dramatically different and worth the image cost.

   d. **Optional weight:** if useful, `browser_network_requests` for an approximate request
      count + notable hosts (CDN, analytics). Don't add page-loads for it.

   e. **ESSENCE (MANDATORY — write this BEFORE any prose).** You have the live site;
      this is the only stage in the pipeline where meaning comes from the source rather
      than from a description of it. Everything downstream — clustering, cluster names,
      the purpose vault — is built from this block, so get it right here. If the URL is
      a sub-page, you must also have opened the domain root (rule 0).
      ```
      "essence": {
        "subject":  the thing actually shared — product, project, article, app, person,
        "host":     the site it lives on, if different from the subject; else null,
        "does":     one sentence: what a user can concretely DO with the subject,
        "for_whom": who it is for, a few words,
        "domain":   the subject matter or industry it serves ("fashion and apparel",
                    "music production", "indie games"; "general" only if truly none),
        "kind":     what kind of thing it IS ("design tool", "marketplace", "personal
                    portfolio", "open-source library", "newsletter", "web toy")
      }
      ```
      Describe the product, publication, project or person — **never the page**.
      `kind` may never be "landing page", "home page", "marketing site" or "website";
      those name the page. A site that opens "the landing page for X" is X. Keep
      `domain` separate from `kind`: a 3D garment tool is kind "design tool", domain
      "fashion and apparel", and merging them loses whichever is weaker. Only state
      what the site supports; never infer an identity from a fragment of a page title.
      An invalid essence is dropped at apply time and backfilled later, so a guess is
      worse than a plain answer.

   f. **Write the `site_designs` entry.** Prose stays the star, and each field has one
      job — keep them apart so the notes read cleanly and the embeddings stay sharp:
      - `what_it_is` — the essence, in 2–3 sentences of prose. The thing, not the page.
      - `what_it_shows` — the content and offering actually presented; quote the real
        `<h1>` as the pitch. No layout chrome.
      - `how_it_works` — the visitor's experience: what they do, what happens.
      - `how_its_designed` — the visual and interaction craft, grounded in the probe.
      **Frameworks, analytics, hosting and other tech go ONLY in the `tech_stack`
      sidecar, never in any prose field** — in prose they make unrelated sites look
      alike (two sites once clustered together on shared Next.js-and-analytics
      vocabulary). Then the structured sidecar from the probe (see schema). **Color and font claims MUST come from the DOM
      probe (`getComputedStyle` / `document.fonts` / CSS vars), never from eyeballing the
      screenshot.** If a value isn't in the DOM, say so (e.g. "system fonts only, no webfont
      payload"). Keep the one-line `palette` / `fonts` as the human summary, backed by the
      structured arrays.

8. Copy `id`, `author`, `name`, `author_profile`, `tweet`, `date` through unchanged.
   Set `text` = the tweet's `full_text`. Set `source` = "bookmarks-export".

## Output schema

Top-level `{ "source_export", "items": [...], "site_designs": {...} }`. Each item:
`id, title, author, name, author_profile, tweet, date, category, tags[], primary_url,
primary_domain, related_urls[], all_urls[], media[] (each {type, original_url,
thumbnail_url, description}), resolved_links[], text, source, teardown_domains[]`.

Each `site_designs[domain]` — PROSE (keep as the focus):
`url, title, tagline, screenshot, extracted_at,
extracted_via` (record the viewport(s) actually captured AND `"logged_out": true` when the
site was viewed without auth, so logged-out captures are flagged not silently asserted),
`what_it_is, what_it_shows, how_it_works, how_its_designed, palette, fonts,
pattern_keywords[]`.

…plus ESSENCE (MANDATORY — see 7e; validated at apply time, an invalid one is dropped):
- `essence: {subject, host, does, for_whom, domain, kind}` — `host` is null when the
  subject is the whole site; every other field is a non-empty string.

…plus STRUCTURED sidecar (all from the DOM probe; omit a field only if truly unavailable):
- `tech_stack: string[]` — framework + analytics + host, e.g. `["Nuxt/Vue","PostHog","Cloudflare"]`
- `palette_tokens: [{name, value, kind}]` — `kind` ∈ `"var"|"rendered"`; real values only
- `fonts_loaded: string[]` — e.g. `["SF Pro 400","EB Garamond 400"]`, or `[]` = system-only
- `meta: {description, og_image, twitter_card, canonical, favicon}` — null where absent
- `media_mix: {img, canvas, video, svg, iframe}` — integer counts
- `page_height_px: number`, `is_single_screen: boolean`
- `headings: string[]` — verbatim `<h1>`/`<h2>` text (the site's own pitch copy)
- `responsive_note: string` — one line on the mobile (390×844) layout change
- `links_out: [{label, href}]` — notable CTA/social/outbound links (optional)
- `weight: {requests, hosts[]}` — optional, from network requests

…plus RELATEDNESS FACETS (MANDATORY — this is how sites connect in the knowledge graph):
Read `tools/ingest/taxonomy.json` (small file; the controlled vocabulary) and classify the
site using ONLY its values:
- `facets: { "vertical": <exactly one taxonomy.vertical key — what the site IS>,
             "mode": <exactly one taxonomy.mode key — dominant color mode>,
             "vibe": [1-3 taxonomy.vibe keys — how it genuinely feels],
             "topics": [0-3 taxonomy.topic keys — what it's ABOUT; empty list if unclear] }`
Do not invent values outside the taxonomy. Topics create the cross-cluster bridges
(e.g. a personal blog ABOUT startups gets `"topics": ["startups"]`), so classify them
from the site's actual subject matter, not its aesthetics.

Write ONLY the file. Do not modify `inspiration.json` or `inspiration.md` — the
deterministic writer does that.
