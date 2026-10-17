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
