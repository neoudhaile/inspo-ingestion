# Queue — the in-repo inbox

Drop a `*.txt` file here (by PR or by hand) and the next daemon fire ingests it,
then deletes it. This is how an agent with no access to the Mac feeds the pipeline.

Format — same as the `~/Downloads/inspo-urls*.txt` drop-files, one URL per line,
`#` comments ignored:

```
# source: https://x.com/someone/status/123 (video)
# why: three portfolio sites with scroll-driven type
https://example.com
# ^ the hero does a cursor-tracked WebGL displacement the screenshot won't catch
https://another.com
```

Rules:

- One file per batch; name it `<yyyymmdd>-<slug>.txt`.
- Only bare `http(s)` URLs count as content. Everything else must be a `#` comment.
- Don't touch anything else under `inspo/` — the rest is generated and your edits
  would be overwritten on the next rebuild.
- The file is removed only after its ingest succeeds, so a failed run retries it.

## URLs are checked before they cost anything

Every URL is fetched at drain time and dropped if it is dead or parked, before
`claude -p` sees it. This exists because PR #1's strongest recommendation,
`terminalindustries.com`, was a parked domain that answered **200 OK** with a
114-byte JS bounce to a GoDaddy lander — so the check is about whether a page has
content, not whether the server was polite.

It errs toward letting things through. A `403` is not a rejection: plenty of real
sites block a bare `urllib` request and open fine in the browser Playwright drives.
Dropping a site somebody watched a video to find is the expensive mistake; a wasted
chunk is the cheap one.

Rejected URLs are written to `inspo/_archive/<stamp>-<name>.rejected.txt` **with
their notes and the reason**, so a wrong call is auditable and a domain that comes
back can be re-queued. Redirects are resolved and rewritten to the final address.
