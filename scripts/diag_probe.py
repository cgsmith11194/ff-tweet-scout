#!/usr/bin/env python3
"""Diag/archaeology runner. If .github/diag-queries.json exists, runs those
searches (supports sort/max_items per query) and dumps raw hits to data/diag/.
Otherwise runs the default cross-actor probe matrix."""
import json, os, time
from datetime import datetime, timezone
from pathlib import Path
import requests, yaml

ROOT = Path(__file__).resolve().parent.parent
CONFIG = yaml.safe_load((ROOT / "config" / "sources.yaml").read_text())
APIFY = "https://api.apify.com/v2"
TOKEN = os.environ["APIFY_TOKEN"]
ACTOR = CONFIG["apify"]["actor"]

def run(payload):
    r = requests.post(f"{APIFY}/acts/{ACTOR}/runs", params={"token": TOKEN},
                      json=payload, timeout=60)
    r.raise_for_status()
    d = r.json()["data"]; rid, ds = d["id"], d["defaultDatasetId"]
    status = d["status"]; deadline = time.time() + 360
    while status in ("READY", "RUNNING") and time.time() < deadline:
        time.sleep(10)
        status = requests.get(f"{APIFY}/actor-runs/{rid}",
                              params={"token": TOKEN}, timeout=60).json()["data"]["status"]
    return requests.get(f"{APIFY}/datasets/{ds}/items",
                        params={"token": TOKEN, "format": "json", "clean": "true",
                                "limit": 1000}, timeout=120).json()

now = datetime.now(timezone.utc)
qfile = ROOT / ".github" / "diag-queries.json"
out = {"generated_at": now.isoformat(), "actor": ACTOR, "results": {}}
if qfile.exists():
    for q in json.loads(qfile.read_text()):
        name = q["name"]
        payload = {"searchTerms": [q["query"]], "maxItems": q.get("max_items", 15),
                   "sort": q.get("sort", "Top"), "tweetLanguage": "en"}
        print("---", name, "|", q["query"])
        try:
            items = run(payload)
            out["results"][name] = {"query": q["query"], "items": [
                {"id": str(it.get("id")), "url": it.get("url") or it.get("twitterUrl"),
                 "createdAt": str(it.get("createdAt")),
                 "author": (it.get("author") or {}).get("userName"),
                 "likes": it.get("likeCount"),
                 "text": (it.get("text") or "")[:500]}
                for it in items if it.get("type") == "tweet"]}
        except Exception as e:
            out["results"][name] = {"query": q["query"], "error": str(e)[:300]}
else:
    out["results"]["note"] = "no diag-queries.json; default probes not run"
p = ROOT / "data" / "diag"; p.mkdir(exist_ok=True)
(p / f"diag-{now.strftime('%Y%m%dT%H%M%S')}.json").write_text(json.dumps(out, indent=1, default=str))
print("wrote diag file")
