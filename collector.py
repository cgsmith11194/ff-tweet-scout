#!/usr/bin/env python3
"""
FF Tweet Scout — weekly collector.

Pulls the trailing week of tweets from tracked accounts + stat-pattern
searches via an Apify actor, normalizes across actor schemas, kills
anti-pattern tweets, scores the rest against the FF Newsletter taste
rubric (docs/taste-profile.md), and writes data/latest.json.

Env:  APIFY_TOKEN (required)  |  WINDOW_DAYS (optional override)
"""
import json
import math
import os
import re
import sys
import time
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

import requests
import yaml

ROOT = Path(__file__).parent
CONFIG = yaml.safe_load((ROOT / "config" / "sources.yaml").read_text())
APIFY_BASE = "https://api.apify.com/v2"

# ----------------------------------------------------------------------------
# Scoring — mirrors docs/taste-profile.md §5
# ----------------------------------------------------------------------------
WEIGHTS = {
    "bullets_cap": 22,
    "density_cap": 18,
    "insight_cap": 18,
    "split_cap": 12,
    "second_level_cap": 14,
    "tier1": 14,
    "tier2": 8,
    "fun": 6,
    "news": 12,
    "news_boost": 10,
    "engagement_cap": 10,
    "kill_promo": -100,
    "kill_reply": -100,
    "kill_retweet": -100,
    "pure_link": -60,
    "injury_news": -35,
}

BULLET_RE = re.compile(r"^\s*(?:[•▪●○‣▸►–—\-\*]|\d{1,2}[.):])\s+\S", re.M)
NUM_RE = re.compile(r"[\d%.]")

INSIGHT_PATTERNS = [
    r"\bonly \w+(?: \w+)? (?:to|with|in|since)\b",
    r"\bfirst .{0,25}\bsince\b",
    r"\bin nfl history\b",
    r"\bsuper bowl era\b",
    r"\bmin\.? ?\d",
    r"\bon pace\b|\bpacing for\b",
    r"\bwould (?:rank|be|have finished|finish)\b",
    r"\bcareer[- ](?:high|low)\b",
    r"\ball[- ]time\b",
    r"\bsince (?:19|20)\d\d\b",
    r"\bmost .{0,30}\b(?:ever|in|since)\b",
    r"\brecord for\b|\bnfl record\b",
    r"\blast (?:player|qb|rb|wr|te|team) to\b",
    r"\bnot a single\b",
    r"\b(?:has|have|had) ever\b",
]
SPLIT_PATTERNS = [
    r"\bwith(?:out)?\b.{0,40}\b(?:on|off) the field\b",
    r"\bwithout\b|\bw/o\b|\bw/out\b",
    r"\bweeks? ?\d{1,2} ?[-–] ?\d{1,2}\b",
    r"\bbefore\b.{0,50}\bafter\b",
    r"\bin games both\b|\bboth (?:were )?healthy\b",
    r"\bsince (?:week ?\d|taking over|becoming the starter)\b",
    r"\bvs\.? \b",
    r"\bfirst \d+ games\b.{0,60}\blast \d+ games\b",
]
SECOND_LEVEL_PATTERNS = [
    r"\bunder (?:hc |coach )?[A-Z][a-z]+ [A-Z][a-z]+\b",
    r"\bplay[- ]?call",
    r"\bsituation[- ]neutral\b|\bneutral pace\b|\bpace\b",
    r"\bproe\b|\bpass rate over expectation\b",
    r"\bover expected\b|\bryoe\b|\bcpoe\b|\bepa\b",
    r"\byards? per route\b|\byprr\b|\bper route\b",
    r"\bper (?:carry|attempt|touch|dropback|scramble)\b",
    r"\bsuccess rate\b",
    r"\bsnap (?:share|rate|count)\b",
    r"\broute (?:share|rate|participation)\b",
    r"\btarget share\b|\b1st read\b|\bfirst read\b",
    r"\bo[- ]?line\b|\boffensive line\b|\bpass block\b|\brun block\b",
    r"\$\d|\bmillion\b|\bincentive\b|\bcontract year\b",
    r"\badp\b|\bpriced as\b|\bbeing drafted as\b|\bcost you a\b",
    r"\bexpected (?:fantasy )?points\b|\bxfp\b",
]
PROMO_PATTERNS = [
    r"\bgiveaway\b", r"\bpromo code\b", r"\buse code\b", r"\bdiscount\b",
    r"\bsign[- ]?up\b", r"\bsubscribe\b", r"% ?off\b", r"\blink in bio\b",
    r"\brt to win\b", r"\benter to win\b", r"\bjoin (?:my|our)\b",
    r"\bdraft kings promo\b", r"\bsportsbook bonus\b",
]
INJURY_NEWS_PATTERNS = [
    r"\bcarted off\b", r"\bmri\b", r"\bplaced on ir\b", r"\bout for the season\b",
    r"\bruled out\b", r"\bexpected to miss\b", r"\bweek[- ]to[- ]week\b",
    r"\bday[- ]to[- ]day\b", r"\bsources?:\b",
]
# Sunday mode treats news as signal, not noise — superset of the injury list.
NEWS_PATTERNS = INJURY_NEWS_PATTERNS + [
    r"\bquestionable\b", r"\bdoubtful\b", r"\binactive\b", r"\bwill not play\b",
    r"\bexpected to play\b", r"\bgame[- ]time decision\b", r"\belevated\b",
    r"\bactivated\b", r"\bdowngraded\b", r"\bupgraded to\b", r"\bofficially out\b",
    r"\bdid not practice\b", r"\blimited practice\b", r"\bfull practice\b",
    r"\binjury report\b", r"\bsigned\b", r"\bwaived\b", r"\breleased\b",
]
COLD_PATTERNS = [
    r"\bworst\b", r"\blowest\b", r"\bdead last\b", r"\bfewest\b",
    r"\bhasn'?t\b|\bhas not\b", r"\b0 (?:yards|catches|targets|tds|touchdowns)\b",
    r"\bdecline\b", r"\bconcern", r"\bstruggl", r"\bbenched\b",
    r"\bdrop(?:ped|s)? (?:down )?to\b", r"\bloses?\b|\blost\b",
    r"\bdid not\b|\bdidn'?t\b", r"\bjust (?:one|two|three|\d+) (?:catch|catches|grabs|yards|targets)\b",
    r"\bnot a single\b", r"\b(?:2[5-9]|3[0-2])(?:th|st|nd|rd)\b",
]


def _count(patterns, text):
    t = text.lower()
    return sum(1 for p in patterns if re.search(p, t, re.I))


def score_tweet(t, tiers, mode="weekly"):
    """Returns (score, parts, killed_reason)."""
    text = t["text"] or ""
    parts = {}

    if t.get("is_retweet"):
        return 0, {}, "retweet"
    if t.get("is_reply"):
        return 0, {}, "reply"
    if _count(PROMO_PATTERNS, text):
        return 0, {}, "promo"

    stripped = re.sub(r"https?://\S+", "", text).strip()
    if len(stripped) < 30 and re.search(r"https?://", text) and not t.get("has_media"):
        return 0, {}, "pure_link"

    bullets = len(BULLET_RE.findall(text))
    parts["bullets"] = min(WEIGHTS["bullets_cap"], 8 + 3.5 * bullets) if bullets >= 2 else 0

    density = 100 * len(NUM_RE.findall(stripped)) / max(len(stripped), 1)
    parts["density"] = min(WEIGHTS["density_cap"], density * 2.0)

    parts["insight"] = min(WEIGHTS["insight_cap"], 6 * _count(INSIGHT_PATTERNS, text))
    parts["split"] = min(WEIGHTS["split_cap"], 4 * _count(SPLIT_PATTERNS, text))
    parts["second_level"] = min(
        WEIGHTS["second_level_cap"], 3.5 * _count(SECOND_LEVEL_PATTERNS, text)
    )

    handle = (t["author_handle"] or "").lower()
    tier = tiers.get(handle, "")
    parts["tier"] = {"tier1": WEIGHTS["tier1"], "tier2": WEIGHTS["tier2"],
                     "fun": WEIGHTS["fun"], "news": WEIGHTS["news"]}.get(tier, 0)

    eng = (t.get("likes") or 0) + 2 * (t.get("retweets") or 0)
    parts["engagement"] = min(
        WEIGHTS["engagement_cap"], max(0.0, (math.log10(eng + 1) - 1.5) * 4)
    )

    if mode == "sunday":
        parts["news_boost"] = (
            WEIGHTS["news_boost"]
            if (tier == "news" or _count(NEWS_PATTERNS, text))
            else 0
        )
        penalty = 0
    else:
        penalty = WEIGHTS["injury_news"] if _count(INJURY_NEWS_PATTERNS, text) else 0
    parts["penalty"] = penalty

    score = max(0.0, min(100.0, sum(parts.values())))
    return round(score, 1), {k: round(v, 1) for k, v in parts.items()}, None


def guess_bucket(t, tiers, mode="weekly"):
    handle = (t["author_handle"] or "").lower()
    text = t["text"] or ""
    if mode == "sunday" and (
        tiers.get(handle) == "news" or _count(NEWS_PATTERNS, text) >= 1
    ):
        return "news"
    stat_density = 100 * len(NUM_RE.findall(text)) / max(len(text), 1)
    is_quote = bool(re.search(r'["“”].{8,}["“”]', text))
    if tiers.get(handle) == "fun" or (
        stat_density < 4
        and (t.get("media_type") in ("video", "animated_gif") or is_quote)
    ):
        return "fun"
    if _count(COLD_PATTERNS, text) >= 2 or (
        _count(COLD_PATTERNS, text) == 1
        and not re.search(r"\b(?:best|leaders?|most|highest|1st|top)\b", text, re.I)
    ):
        return "cold_water"
    return "analysis_hype"


# ----------------------------------------------------------------------------
# Apify collection
# ----------------------------------------------------------------------------
def build_queries(since, until, mode="weekly"):
    acc = CONFIG["accounts"]
    aq = CONFIG["account_query"]
    date_clause = f"since:{since} until:{until}"
    base_filters = "-filter:nativeretweets -filter:replies"

    queries, account_queries = [], []
    handles = acc["tier1"] + acc["tier2"] + acc["fun"]
    if mode == "sunday":
        handles = handles + acc.get("news", [])
    n = aq["handles_per_query"]
    for i in range(0, len(handles), n):
        batch = " OR ".join(f"from:{h}" for h in handles[i : i + n])
        account_queries.append(f"({batch}) {date_clause} {base_filters}")

    searches = list(CONFIG["searches"])
    if mode == "sunday":
        searches += CONFIG.get("sunday", {}).get("searches", [])
    for s in searches:
        q = f'{s["query"]} min_faves:{s["min_faves"]} {date_clause} {base_filters}'
        queries.append({"q": q, "max_items": s["max_items"], "name": s["name"]})

    return account_queries, queries


def snapshot_odds(stamp):
    """Keyless ESPN scoreboard snapshot -> data/odds-{stamp}.json.
    Wednesday snapshots are the baseline; Sunday snapshots diff against them
    for the Sunday Brief's line-move section. Never fails the run."""
    if not CONFIG.get("odds", {}).get("espn_snapshot", False):
        return
    try:
        r = requests.get(
            "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard",
            timeout=30,
        )
        r.raise_for_status()
        games = []
        for ev in r.json().get("events", []):
            comp = (ev.get("competitions") or [{}])[0]
            odds = (comp.get("odds") or [{}])[0]
            games.append(
                {
                    "game": ev.get("shortName"),
                    "date": ev.get("date"),
                    "spread": odds.get("details"),
                    "over_under": odds.get("overUnder"),
                    "provider": (odds.get("provider") or {}).get("name"),
                }
            )
        out_path = ROOT / "data" / f"odds-{stamp}.json"
        out_path.write_text(json.dumps({"captured_at": stamp, "games": games}, indent=1))
        print(f"Odds snapshot: {len(games)} games -> {out_path.name}")
    except Exception as e:
        print(f"WARNING: odds snapshot failed ({e}) — continuing without it")


def run_actor(token, search_terms, max_items):
    actor = CONFIG["apify"]["actor"]
    payload = {
        "searchTerms": search_terms,
        "maxItems": max_items,
        "queryType": CONFIG["apify"].get("query_type", "Latest"),
        "lang": "en",
    }
    r = requests.post(
        f"{APIFY_BASE}/acts/{actor}/runs",
        params={"token": token},
        json=payload,
        timeout=60,
    )
    r.raise_for_status()
    run = r.json()["data"]
    run_id, dataset_id = run["id"], run["defaultDatasetId"]

    deadline = time.time() + 60 * CONFIG["apify"].get("timeout_minutes", 20)
    poll = CONFIG["apify"].get("poll_seconds", 15)
    status = run["status"]
    while status in ("READY", "RUNNING") and time.time() < deadline:
        time.sleep(poll)
        rr = requests.get(
            f"{APIFY_BASE}/actor-runs/{run_id}", params={"token": token}, timeout=60
        )
        rr.raise_for_status()
        status = rr.json()["data"]["status"]
        print(f"  run {run_id}: {status}", flush=True)
    if status != "SUCCEEDED":
        print(f"  WARNING: run ended with status {status}; using partial dataset")

    items, offset = [], 0
    while True:
        dr = requests.get(
            f"{APIFY_BASE}/datasets/{dataset_id}/items",
            params={"token": token, "format": "json", "clean": "true",
                    "offset": offset, "limit": 1000},
            timeout=120,
        )
        dr.raise_for_status()
        batch = dr.json()
        if not batch:
            break
        items.extend(batch)
        offset += len(batch)
        if len(batch) < 1000:
            break
    return items


# ----------------------------------------------------------------------------
# Normalization (kaitoeasyapi / apidojo tolerant)
# ----------------------------------------------------------------------------
def _get(d, *paths):
    for path in paths:
        cur = d
        ok = True
        for key in path.split("."):
            if isinstance(cur, dict) and key in cur and cur[key] is not None:
                cur = cur[key]
            else:
                ok = False
                break
        if ok:
            return cur
    return None


def parse_created(v):
    if not v:
        return None
    for fn in (
        lambda x: parsedate_to_datetime(x),
        lambda x: datetime.strptime(x, "%a %b %d %H:%M:%S %z %Y"),
        lambda x: datetime.fromisoformat(x.replace("Z", "+00:00")),
    ):
        try:
            return fn(v).astimezone(timezone.utc).isoformat()
        except Exception:
            continue
    return None


def normalize(item, source):
    if item.get("type") not in (None, "tweet"):
        return None
    text = _get(item, "text", "full_text", "fullText")
    tid = str(_get(item, "id", "id_str", "tweetId") or "")
    if not text or not tid:
        return None
    media = _get(item, "extendedEntities.media", "media") or []
    if isinstance(media, dict):
        media = [media]
    media_type = None
    for m in media:
        mt = m.get("type") if isinstance(m, dict) else None
        if mt in ("video", "animated_gif"):
            media_type = mt
            break
        if mt == "photo":
            media_type = media_type or "photo"
    handle = _get(item, "author.userName", "author.username",
                  "user.screen_name", "username")
    return {
        "id": tid,
        "url": _get(item, "url", "twitterUrl")
        or (f"https://x.com/{handle}/status/{tid}" if handle else None),
        "text": text,
        "author_handle": handle,
        "author_name": _get(item, "author.name", "user.name", "name"),
        "author_followers": _get(item, "author.followers", "author.followersCount",
                                 "user.followers_count"),
        "created_at": parse_created(_get(item, "createdAt", "created_at", "date")),
        "likes": _get(item, "likeCount", "favorite_count", "likes") or 0,
        "retweets": _get(item, "retweetCount", "retweet_count", "retweets") or 0,
        "replies": _get(item, "replyCount", "reply_count") or 0,
        "views": _get(item, "viewCount", "views"),
        "is_reply": bool(_get(item, "isReply", "is_reply")
                         or _get(item, "inReplyToId", "in_reply_to_status_id")),
        "is_retweet": bool(_get(item, "isRetweet", "is_retweet")
                           or _get(item, "retweeted_tweet", "retweetedTweet")),
        "has_media": bool(media),
        "media_type": media_type,
        "quoted_handle": _get(item, "quoted_tweet.author.userName",
                              "quoted_tweet.author.username"),
        "quoted_text": _get(item, "quoted_tweet.text", "quoted_tweet.full_text"),
        "source": source,
    }


# ----------------------------------------------------------------------------
def main():
    token = os.environ.get("APIFY_TOKEN")
    if not token:
        sys.exit("APIFY_TOKEN env var is required")

    mode = os.environ.get("MODE", "weekly").lower()
    default_window = (
        CONFIG.get("sunday", {}).get("window_days", 3)
        if mode == "sunday"
        else CONFIG.get("window_days", 7)
    )
    window = int(os.environ.get("WINDOW_DAYS", default_window))
    until_dt = datetime.now(timezone.utc)
    since_dt = until_dt - timedelta(days=window)
    since, until = since_dt.strftime("%Y-%m-%d"), (until_dt + timedelta(days=1)).strftime("%Y-%m-%d")
    print(f"Mode: {mode} | Window: {since} → {until} (UTC)")

    account_queries, search_queries = build_queries(since, until, mode)

    print(f"Run 1: {len(account_queries)} account-batch queries")
    raw = [
        (it, "accounts")
        for it in run_actor(token, account_queries, CONFIG["account_query"]["max_items"])
    ]
    print(f"  got {len(raw)} items")

    search_terms = [q["q"] for q in search_queries]
    search_cap = sum(q["max_items"] for q in search_queries)
    print(f"Run 2: {len(search_terms)} pattern searches (cap {search_cap})")
    raw += [(it, "search") for it in run_actor(token, search_terms, search_cap)]
    print(f"  total raw items: {len(raw)}")

    tiers = {}
    for tier_name in ("tier1", "tier2", "fun", "news"):
        for h in CONFIG["accounts"].get(tier_name, []):
            tiers[h.lower()] = tier_name

    seen, candidates, kills, rejects = set(), [], {}, []

    def log_reject(t, reason, score=None):
        rejects.append(
            {
                "id": t["id"],
                "url": t["url"],
                "handle": t["author_handle"],
                "reason": reason,
                "score": score,
                "likes": t.get("likes"),
                "text": (t["text"] or "")[:2000],
            }
        )

    for item, source in raw:
        t = normalize(item, source)
        if not t:
            kills["unparseable"] = kills.get("unparseable", 0) + 1
            continue
        if t["id"] in seen:
            continue
        seen.add(t["id"])
        score, parts, killed = score_tweet(t, tiers, mode)
        if killed:
            kills[killed] = kills.get(killed, 0) + 1
            log_reject(t, killed)
            continue
        bucket = guess_bucket(t, tiers, mode)
        floors = {
            "fun": CONFIG["output"].get("min_score_fun", 8),
            "news": CONFIG["output"].get("min_score_news", 10),
        }
        floor = floors.get(bucket, CONFIG["output"].get("min_score", 25))
        if score < floor:
            kills["low_score"] = kills.get("low_score", 0) + 1
            log_reject(t, f"low_score({bucket})", score)
            continue
        t["score"] = score
        t["score_parts"] = parts
        t["tier"] = tiers.get((t["author_handle"] or "").lower(), "")
        t["bucket_guess"] = bucket
        candidates.append(t)

    candidates.sort(key=lambda x: -x["score"])
    candidates = candidates[: CONFIG["output"].get("keep_top", 160)]

    out = {
        "generated_at": until_dt.isoformat(),
        "mode": mode,
        "window": {"since": since, "until": until, "days": window},
        "counts": {
            "raw": len(raw),
            "unique": len(seen),
            "kept": len(candidates),
            "kills": kills,
        },
        "buckets": {
            b: sum(1 for c in candidates if c["bucket_guess"] == b)
            for b in ("analysis_hype", "cold_water", "fun", "news")
        },
        "candidates": candidates,
    }

    data_dir = ROOT / "data"
    data_dir.mkdir(exist_ok=True)
    stamp = until_dt.strftime("%Y-%m-%d")
    (data_dir / f"candidates-{stamp}.json").write_text(json.dumps(out, indent=1))
    (data_dir / "latest.json").write_text(json.dumps(out, indent=1))
    rejects.sort(key=lambda r: (r["reason"], -(r["score"] or 0)))
    (data_dir / f"rejects-{stamp}.json").write_text(
        json.dumps(
            {
                "generated_at": out["generated_at"],
                "window": out["window"],
                "counts": out["counts"],
                "note": "Every collected tweet that did not make candidates, with reason. "
                "Near-full text kept (2000-char cap) as a corpus for later league-wide "
                "analysis; raw Apify datasets also persist ~1 week in the console.",
                "rejects": rejects,
            },
            indent=1,
        )
    )
    snapshot_odds(stamp)
    print(json.dumps({k: out[k] for k in ("mode", "window", "counts", "buckets")}, indent=2))
    print(f"Wrote data/candidates-{stamp}.json, data/rejects-{stamp}.json, data/latest.json")


if __name__ == "__main__":
    main()
