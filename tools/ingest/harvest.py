import re
from .config import TWITTER_HOSTS, UTILITY_DENYLIST

_URL = re.compile(r'https?://[^\s"\\<>]+')

def _walk(node, sink):
    if isinstance(node, str):
        sink.extend(_URL.findall(node))
    elif isinstance(node, dict):
        for v in node.values():
            _walk(v, sink)
    elif isinstance(node, list):
        for v in node:
            _walk(v, sink)

def deep_external_urls(record):
    """Every external (non-platform) http(s) URL anywhere in the record, ordered, unique."""
    raw = []
    _walk(record, raw)
    seen, out = set(), []
    for u in raw:
        u = u.rstrip(').,\';"')
        if any(h in u for h in TWITTER_HOSTS):
            continue
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out

def split_primary(urls):
    """Return (primary_candidates, all_urls). Utility/footer links can't be primary."""
    primary = [u for u in urls if not any(d in u for d in UTILITY_DENYLIST)]
    return primary, list(urls)
