#!/usr/bin/env bash
# Download a tweet image (photo original OR video poster thumbnail) to /tmp so the
# enricher can Read/view it. Prints the local path on success, nothing on failure.
#   Usage: fetch_image.sh <image_url> <prefix>
# (Video MOTION frames are captured separately via Playwright seek+screenshot —
#  Chromium decodes H.264; Playwright's bundled ffmpeg cannot demux tweet videos.)
set -euo pipefail
URL="${1:?usage: fetch_image.sh <url> <prefix>}"
PREFIX="${2:-media}"
OUT="/tmp/neoud-media"
mkdir -p "$OUT"
IMG="$OUT/${PREFIX}.jpg"
if curl -fsSL -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)" -e "https://twitter.com/" -o "$IMG" "$URL"; then
  echo "$IMG"
fi
