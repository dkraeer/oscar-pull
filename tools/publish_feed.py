#!/usr/bin/env python3
"""Publish the daily feed: copy sleep.bmp + briefing.epub into an output
directory and write catalog.json with absolute URLs for the Oscar Daily
Pull device.json catalog (items carry their own download URL).

Usage:
  python3 publish_feed.py --base https://host/path --out DIR \
      --bmp dashboard.bmp --epub briefing.epub --label "Friday, October 23"
"""
import argparse
import json
import shutil
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True, help="Public base URL of the feed (no trailing slash)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--bmp", required=True)
    ap.add_argument("--epub", required=True)
    ap.add_argument("--label", required=True, help='e.g. "Friday, October 23"')
    ap.add_argument("--sample", action="store_true")
    args = ap.parse_args()

    base = args.base.rstrip("/")
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(args.bmp, out / "sleep.bmp")
    shutil.copyfile(args.epub, out / "briefing.epub")
    suffix = " (sample)" if args.sample else ""
    catalog = {
        "items": [
            {"id": "sleep.bmp", "title": f"Dashboard — {args.label}", "url": f"{base}/sleep.bmp"},
            {"id": "briefing.epub", "title": f"Briefing — {args.label}{suffix}", "url": f"{base}/briefing.epub"},
        ]
    }
    (out / "catalog.json").write_text(json.dumps(catalog, indent=1))
    print("published feed to", out)


if __name__ == "__main__":
    main()
