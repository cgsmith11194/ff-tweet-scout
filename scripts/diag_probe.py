#!/usr/bin/env python3
"""Diag v2 — cross-actor probe: kaito vs apidojo (search + timeline endpoints)."""
import json, os, time
from datetime import datetime, timedelta, timezone
from pathlib import Path
import requests, yaml

ROOT = Path(__file__).resolve().parent.parent
CONFIG = yaml.safe_load((ROOT / "config" / "sources.yaml").read_text())
APIFY = "https://api.apify.com/v2"
TOKEN = os.environ["APIFY_TOKEN"]

def run(actor, payload, cap=20):
    payload = dict(payload); payload.setdefault("maxItems", cap)
    r = requests.post(f"{APIFY}/acts/{actor}/runs", params={"token": TOKEN},
                      json=payload, timeout=60)
    r.raise_for_status()
    d = r.json()["data"]; rid, ds = d["id"], d["defaultDatasetId"]
    status = d["status"]; deadline = time.time() + 360
    while status in ("READY", "RUNNING") and time.time() < deadline:
        time.sleep(10)
        status = requests.get(f"{APIFY}/actor-runs/{rid}",
                              params={"token": TOKEN}, timeout=60).json()["data"]["status"]
    items = requests.get(f"{APIFY}/datasets/{ds}/items",
                         params={"token": TOKEN, "format": "json", "clean": "true",
                                 "limit": 1000}, timeout=120).json()
    mock = sum(1 for it in items if it.get("type") == "mock_tweet" or str(it.get("id")) == "-1"
               or it.get("noResults") or "KaitoEasyAPI" in str(it.get("text",""))[:60])
    return {"run_id": rid, "status": status, "items": len(items), "mock": mock,
            "real": len(items) - mock,
            "sample": [{k: str(it.get(k))[:140] for k in
                        ("type","id","text","createdAt","created_at","noResults","author","url") if it.get(k) is not None}
                       for it in items[:2]]}

now = datetime.now(timezone.utc)
since_time = int((now - timedelta(days=7)).timestamp())
handles = CONFIG["accounts"]["tier1"][: CONFIG["account_query"]["handles_per_query"]]
batch = " OR ".join(f"from:{h}" for h in handles)
q_verbatim = f"({batch}) since_time:{since_time} -filter:nativeretweets -filter:replies"

APIDOJO = "apidojo~tweet-scraper"
KAITO = CONFIG["apify"]["actor"]
probes = [
  ("kaito_keyword_recheck", KAITO, {"searchTerms": ["NFL"], "queryType": "Latest", "lang": "en"}),
  ("apidojo_search_verbatim", APIDOJO, {"searchTerms": [q_verbatim], "sort": "Latest"}),
  ("apidojo_search_keyword", APIDOJO, {"searchTerms": ["NFL"], "sort": "Latest"}),
  ("apidojo_timeline_handles", APIDOJO, {"twitterHandles": handles[:5], "sort": "Latest"}),
]
out = {"generated_at": now.isoformat(), "probes": {}}
for name, actor, payload in probes:
    print("---", name)
    try:
        out["probes"][name] = {"actor": actor, "payload": payload, **run(actor, payload)}
    except Exception as e:
        out["probes"][name] = {"actor": actor, "payload": payload, "error": str(e)[:300]}
    print(json.dumps(out["probes"][name], default=str)[:400])

p = ROOT / "data" / "diag"; p.mkdir(exist_ok=True)
(p / f"diag-{now.strftime('%Y%m%dT%H%M')}.json").write_text(json.dumps(out, indent=1, default=str))
print("wrote diag v2 file")
