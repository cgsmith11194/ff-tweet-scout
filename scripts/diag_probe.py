#!/usr/bin/env python3
"""One-off Apify probe matrix — diagnose all-mock collections (9/9 incident).
Runs 4 tiny actor runs and writes results to data/diag/. Never edits latest.json."""
import json, os, sys, time
from datetime import datetime, timedelta, timezone
from pathlib import Path
import requests, yaml

ROOT = Path(__file__).resolve().parent.parent
CONFIG = yaml.safe_load((ROOT / "config" / "sources.yaml").read_text())
APIFY = "https://api.apify.com/v2"
TOKEN = os.environ["APIFY_TOKEN"]
ACTOR = CONFIG["apify"]["actor"]

def run(terms, max_items, query_type="Latest"):
    payload = {"searchTerms": terms, "maxItems": max_items,
               "queryType": query_type, "lang": "en"}
    r = requests.post(f"{APIFY}/acts/{ACTOR}/runs", params={"token": TOKEN},
                      json=payload, timeout=60)
    r.raise_for_status()
    d = r.json()["data"]
    rid, ds = d["id"], d["defaultDatasetId"]
    status = d["status"]
    deadline = time.time() + 300
    while status in ("READY", "RUNNING") and time.time() < deadline:
        time.sleep(10)
        status = requests.get(f"{APIFY}/actor-runs/{rid}",
                              params={"token": TOKEN}, timeout=60).json()["data"]["status"]
    items = requests.get(f"{APIFY}/datasets/{ds}/items",
                         params={"token": TOKEN, "format": "json", "clean": "true",
                                 "limit": 1000}, timeout=120).json()
    mock = sum(1 for it in items if it.get("type") == "mock_tweet" or it.get("id") == -1)
    real = len(items) - mock
    return {"run_id": rid, "status": status, "items": len(items), "mock": mock,
            "real": real,
            "sample": [ {k: str(it.get(k))[:160] for k in ("type","id","text","createdAt","created_at","author")} for it in items[:2] ]}

now = datetime.now(timezone.utc)
since_time = int((now - timedelta(days=7)).timestamp())
handles = CONFIG["accounts"]["tier1"][: CONFIG["account_query"]["handles_per_query"]]
batch = " OR ".join(f"from:{h}" for h in handles)
filters = "-filter:nativeretweets -filter:replies"

probes = {
  "1_verbatim_failing": f"({batch}) since_time:{since_time} {filters}",
  "2_no_date_clause":   f"({batch}) {filters}",
  "3_bare_handles":     f"({batch})",
  "4_keyword_control":  "NFL",
}
out = {"generated_at": now.isoformat(), "actor": ACTOR, "probes": {}}
for name, q in probes.items():
    print(f"--- {name}: {q[:120]}")
    try:
        out["probes"][name] = {"query": q, **run([q], 20)}
    except Exception as e:
        out["probes"][name] = {"query": q, "error": str(e)}
    print(json.dumps(out["probes"][name], indent=1)[:500])

# recent actor runs overview
try:
    rr = requests.get(f"{APIFY}/actor-runs", params={"token": TOKEN, "desc": 1, "limit": 8}, timeout=60).json()
    out["recent_runs"] = [
        {"id": x["id"], "actor": x.get("actId"), "status": x["status"],
         "started": x.get("startedAt"), "results": (x.get("stats") or {}).get("itemCount") or (x.get("chargedEventCounts") or {}) }
        for x in rr.get("data", {}).get("items", [])]
except Exception as e:
    out["recent_runs_error"] = str(e)

# account balance / limits
try:
    lim = requests.get(f"{APIFY}/users/me/limits", params={"token": TOKEN}, timeout=60).json()
    out["limits"] = lim.get("data")
except Exception as e:
    out["limits_error"] = str(e)

p = ROOT / "data" / "diag"
p.mkdir(exist_ok=True)
(p / f"diag-{now.strftime('%Y%m%dT%H%M')}.json").write_text(json.dumps(out, indent=1, default=str))
print("wrote diag file")
