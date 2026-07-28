#!/usr/bin/env python3
"""
Corpus builder for the FF Newsletter tweet scout.

Pulls every post from theffnewsletter.substack.com, extracts each embedded
tweet (Substack stores the full tweet JSON in the embed's data-attrs), and
writes a corpus of historically-selected tweets for taste analysis.
"""
import json
import re
import sys
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

BASE = "https://theffnewsletter.substack.com"
OUT = Path(__file__).parent / "corpus"
OUT.mkdir(exist_ok=True)

S = requests.Session()
S.headers.update(
    {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
    }
)


def get_archive():
    posts, offset = [], 0
    while True:
        r = S.get(
            f"{BASE}/api/v1/archive",
            params={"sort": "new", "offset": offset, "limit": 50},
            timeout=30,
        )
        r.raise_for_status()
        batch = r.json()
        if not batch:
            break
        posts.extend(batch)
        print(f"  archive: {len(posts)} posts so far", flush=True)
        if len(batch) < 50:
            break
        offset += 50
        time.sleep(0.4)
    return posts


def get_post(slug):
    r = S.get(f"{BASE}/api/v1/posts/{slug}", timeout=30)
    r.raise_for_status()
    return r.json()


def parse_tweets(body_html, post_meta):
    """Extract tweet embeds from Substack body HTML."""
    soup = BeautifulSoup(body_html, "html.parser")
    tweets = []
    for div in soup.find_all(attrs={"data-attrs": True}):
        classes = div.get("class") or []
        if "tweet" not in classes:
            continue
        try:
            attrs = json.loads(div["data-attrs"])
        except (json.JSONDecodeError, KeyError):
            continue
        qt = attrs.get("quoted_tweet") or {}
        tweets.append(
            {
                "newsletter_date": post_meta["post_date"][:10],
                "newsletter_title": post_meta["title"],
                "newsletter_slug": post_meta["slug"],
                "tweet_url": attrs.get("url", ""),
                "username": attrs.get("username", ""),
                "name": attrs.get("name", ""),
                "tweet_date": attrs.get("date", ""),
                "full_text": attrs.get("full_text", ""),
                "like_count": attrs.get("like_count"),
                "retweet_count": attrs.get("retweet_count"),
                "n_photos": len(attrs.get("photos") or []),
                "has_video": bool(attrs.get("video_url")),
                "quoted_username": qt.get("username", ""),
                "quoted_text": qt.get("full_text", ""),
            }
        )
    # count non-tweet embeds / images for context
    n_images = len(soup.find_all("img"))
    x_links = [
        a["href"]
        for a in soup.find_all("a", href=True)
        if re.search(r"(twitter\.com|x\.com)/\w+/status/", a["href"])
    ]
    return tweets, n_images, x_links


def main():
    print("Fetching archive...", flush=True)
    archive = get_archive()
    json.dump(archive, open(OUT / "archive_raw.json", "w"), indent=1)
    print(f"Total posts: {len(archive)}")

    corpus, post_summaries, failures = [], [], []
    for i, p in enumerate(archive):
        slug, title = p["slug"], p["title"]
        try:
            post = get_post(slug)
            body = post.get("body_html") or ""
            meta = {
                "post_date": p.get("post_date", ""),
                "title": title,
                "slug": slug,
            }
            tweets, n_images, x_links = parse_tweets(body, meta)
            corpus.extend(tweets)
            post_summaries.append(
                {
                    "date": meta["post_date"][:10],
                    "title": title,
                    "slug": slug,
                    "n_tweet_embeds": len(tweets),
                    "n_images": n_images,
                    "n_bare_x_links": len(x_links),
                    "wordcount": p.get("wordcount"),
                }
            )
            print(
                f"[{i+1}/{len(archive)}] {meta['post_date'][:10]} "
                f"{title[:45]:45s} tweets={len(tweets)} imgs={n_images}",
                flush=True,
            )
        except Exception as e:
            failures.append({"slug": slug, "error": str(e)})
            print(f"[{i+1}/{len(archive)}] FAILED {slug}: {e}", flush=True)
        time.sleep(0.35)

    json.dump(corpus, open(OUT / "corpus.json", "w"), indent=1)
    json.dump(post_summaries, open(OUT / "post_summaries.json", "w"), indent=1)
    json.dump(failures, open(OUT / "failures.json", "w"), indent=1)

    print("\n=== SUMMARY ===")
    print(f"posts: {len(archive)}, tweet embeds: {len(corpus)}, failures: {len(failures)}")
    from collections import Counter

    by_user = Counter(t["username"].lower() for t in corpus if t["username"])
    print("\nTop 30 accounts by times featured:")
    for u, c in by_user.most_common(30):
        print(f"  {c:3d}  @{u}")


if __name__ == "__main__":
    main()
