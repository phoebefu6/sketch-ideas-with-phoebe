#!/usr/bin/env python3
"""Create a stable public-source fingerprint for queue deduplication."""

from __future__ import annotations

import argparse
import hashlib
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse


TRACKING_KEYS = {
    "fbclid",
    "gclid",
    "mc_cid",
    "mc_eid",
    "ref",
    "source",
    "utm_campaign",
    "utm_content",
    "utm_medium",
    "utm_source",
    "utm_term",
}


def canonicalize(raw_url: str) -> tuple[str, str]:
    parsed = urlparse(raw_url.strip())
    host = parsed.netloc.lower().removeprefix("www.")
    query = parse_qs(parsed.query, keep_blank_values=False)

    if host in {"youtube.com", "m.youtube.com", "youtu.be"}:
        if host == "youtu.be":
            video_id = parsed.path.strip("/").split("/")[0]
        elif parsed.path == "/watch":
            video_id = (query.get("v") or [""])[0]
        elif parsed.path.startswith("/shorts/") or parsed.path.startswith("/live/"):
            video_id = parsed.path.strip("/").split("/")[1]
        else:
            video_id = ""
        if video_id:
            canonical = f"https://www.youtube.com/watch?v={video_id}"
            return canonical, f"youtube:{video_id}"

    clean_query = {
        key: values
        for key, values in query.items()
        if key.lower() not in TRACKING_KEYS
    }
    encoded = urlencode(sorted((key, value) for key, values in clean_query.items() for value in values))
    canonical = urlunparse((parsed.scheme.lower() or "https", host, parsed.path.rstrip("/") or "/", "", encoded, ""))
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:24]
    return canonical, f"url:{digest}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    args = parser.parse_args()
    canonical, fingerprint = canonicalize(args.url)
    print(f"canonical={canonical}")
    print(f"fingerprint={fingerprint}")


if __name__ == "__main__":
    main()
