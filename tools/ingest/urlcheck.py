#!/usr/bin/env python3
"""Mechanical prefilter: is this URL worth an enrichment chunk?

Built for a specific failure. PR #1 — the first agent-sourced batch — recommended
`terminalindustries.com` as its strongest site ("the entire video is a design
breakdown of this site"). The domain was parked. An agent that cannot fetch cannot
validate, so every URL it supplies is a claim; this module is where the claim gets
checked, before `claude -p` spends a chunk on it.

What the real case taught: status codes would not have caught it. The parked domain
answered **200** with this entire body —

    <!DOCTYPE html><html><head><script>window.onload=function(){
    window.location.href="/lander"}</script></head></html>

114 bytes, no title, no stylesheet, a JS bounce to a GoDaddy lander. So the test has
to be about whether a page has any content, not whether the server was polite.

The bias is deliberate and one-directional: **reject only on clear evidence, let doubt
through.** Dropping a real design site costs us something irreplaceable (it was
recommended by a human or an agent that watched it); letting a bad one through costs
one wasted chunk and an item that enrichment already handles correctly. So a 403 is
NOT a rejection — plenty of good sites bot-block a bare urllib request and open fine
in the real browser Playwright drives.

Set NEOUD_SKIP_URLCHECK=1 to bypass entirely (offline runs).
"""
import concurrent.futures
import os
import re
import ssl
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
TIMEOUT = 12
READ_BYTES = 65536
WORKERS = 8

# A page under this size with no title and no stylesheet is not a website.
STUB_BYTES = 2000

# Hosts that only ever serve parking/for-sale pages.
PARKING_HOSTS = (
    "sedoparking.com", "afternic.com", "hugedomains.com", "bodis.com",
    "parkingcrew.net", "above.com", "dan.com", "uniregistry.com",
    "squadhelp.com", "domainmarket.com", "buydomains.com",
)

# Text that only appears on a parking page. Matched against a SMALL body only, so a
# real site writing the words "for sale" is never caught by this.
PARKING_MARKERS = (
    "/lander", "buy this domain", "domain is for sale", "domain may be for sale",
    "this domain is for sale", "the domain name you entered", "domain parking",
)

# Server said no, but a real browser may still get in — never a rejection.
INCONCLUSIVE_STATUSES = (401, 403, 406, 429)


class Verdict:
    __slots__ = ("url", "ok", "reason", "final_url", "status")

    def __init__(self, url, ok, reason, final_url=None, status=None):
        self.url, self.ok, self.reason = url, ok, reason
        self.final_url, self.status = final_url or url, status

    def __repr__(self):
        return f"<{'OK ' if self.ok else 'REJECT'} {self.url} — {self.reason}>"


def looks_like_stub(body):
    """True when a body carries no page at all. Pure; testable.

    Deliberately narrow: small AND titleless AND unstyled. A small page that bothered
    to set a title or load CSS is somebody's real minimal site, not a parking stub.
    """
    if body is None:
        return False
    text = body.strip()
    if len(text) >= STUB_BYTES:
        return False
    low = text.lower()
    # Match the title's CONTENT, not just "a non-space follows the tag" — the `<` of
    # the closing tag satisfies that, so `<title>  </title>` read as a real title.
    m = re.search(r"<title[^>]*>([^<]*)", low)
    has_title = bool(m and m.group(1).strip())
    has_css = ('rel="stylesheet"' in low or "rel='stylesheet'" in low
               or "<style" in low)
    return not (has_title or has_css)


def classify(status=None, final_url="", body=None, err=None):
    """Decide from an already-fetched result. Pure; testable without a network.

    Returns (ok, reason).
    """
    if err:
        return False, f"unreachable ({err})"
    if status in (404, 410):
        return False, f"gone (HTTP {status})"
    if status is not None and status >= 500:
        return False, f"server error (HTTP {status})"
    if status in INCONCLUSIVE_STATUSES:
        # Bot-blocked, not dead. Let the real browser decide.
        return True, f"allowed despite HTTP {status} (may bot-block urllib)"

    host = re.sub(r"^https?://", "", final_url or "").split("/")[0].lower()
    host = host[4:] if host.startswith("www.") else host
    if any(host == p or host.endswith("." + p) for p in PARKING_HOSTS):
        return False, f"parked (redirects to {host})"

    if body is not None:
        small = len(body.strip()) < max(STUB_BYTES * 2, 4000)
        low = body.lower()
        if small:
            for m in PARKING_MARKERS:
                if m in low:
                    return False, f"parked (page is a {m!r} stub)"
        if looks_like_stub(body):
            return False, f"no page here ({len(body.strip())} bytes, no title, no css)"
    return True, "ok"


def fetch(url, timeout=TIMEOUT):
    """GET the first READ_BYTES. Returns (status, final_url, body, err)."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
            return r.status, r.url, r.read(READ_BYTES).decode("utf-8", "replace"), None
    except urllib.error.HTTPError as e:
        try:
            body = e.read(READ_BYTES).decode("utf-8", "replace")
        except Exception:
            body = None
        return e.code, getattr(e, "url", url), body, None
    except Exception as e:                      # URLError, timeout, SSL, DNS…
        return None, url, None, f"{type(e).__name__}"


def check(url, timeout=TIMEOUT):
    status, final_url, body, err = fetch(url, timeout)
    ok, reason = classify(status, final_url, body, err)
    return Verdict(url, ok, reason, final_url, status)


def check_many(urls, workers=WORKERS, timeout=TIMEOUT):
    """Check in parallel, preserving input order."""
    if os.environ.get("NEOUD_SKIP_URLCHECK") == "1":
        return [Verdict(u, True, "skipped (NEOUD_SKIP_URLCHECK=1)") for u in urls]
    urls = list(urls)
    if not urls:
        return []
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(workers, len(urls))) as ex:
        return list(ex.map(lambda u: check(u, timeout), urls))


def main():
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("urls", nargs="+")
    args = ap.parse_args()
    bad = 0
    for v in check_many(args.urls):
        print(f"{'OK    ' if v.ok else 'REJECT'} {v.url} — {v.reason}"
              + (f" → {v.final_url}" if v.final_url != v.url else ""))
        bad += 0 if v.ok else 1
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
