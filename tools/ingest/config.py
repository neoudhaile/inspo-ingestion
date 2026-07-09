from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
INSPO = REPO / "inspo"
INSPIRATION_JSON = INSPO / "inspiration.json"
INSPIRATION_MD = INSPO / "inspiration.md"
LEDGER = INSPO / "_ledger.json"
INBOX = INSPO / "_inbox"
ARCHIVE = INSPO / "_archive"
DOWNLOADS = Path.home() / "Downloads"
EXPORT_GLOB = "twitter-Bookmarks-*.json"

# Hosts that are the platform itself — never a destination site.
TWITTER_HOSTS = ("twitter.com", "t.co", "x.com", "twimg.com", "pbs.twimg")

# Utility links that should never be chosen as a primary site (kept in all_urls).
UTILITY_DENYLIST = (
    "linktr.ee", "typefully.com", "cal.com", "calendly.com",
    "medium.com", "docs.google.com", "framer.link", "substack.com",
    "github.com", "youtube.com", "youtu.be",
)

# MD managed-region markers.
MD_REGION_START = "<!-- AUTO-INGEST:START — do not edit inside this region by hand -->"
MD_REGION_END = "<!-- AUTO-INGEST:END -->"
