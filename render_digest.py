#!/usr/bin/env python3
"""
Render candidates JSON → self-contained HTML digest.

Usage: python render_digest.py [in.json] [out.html]
Defaults: data/latest.json → digest/latest.html

Honors optional per-candidate fields `why` (one-line rationale) and
`final_rank` (set by the Claude taste-ranking pass). Candidates with
final_rank sort first by it; otherwise by heuristic score.
"""
import html
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent

BUCKETS = [
    ("analysis_hype", "Analysis & Hype", "#0e7a4f", "#e7f5ee"),
    ("cold_water", "Cold Water", "#1d5fa8", "#e8f0fa"),
    ("fun", "The Fun Stuff", "#a86308", "#fdf3e2"),
]

CSS = """
:root { color-scheme: light; }
* { box-sizing: border-box; }
body { margin:0; padding:32px 16px 64px; background:#f5f6f8; color:#1a1d21;
  font:15px/1.5 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif; }
.wrap { max-width:780px; margin:0 auto; }
header { margin-bottom:28px; }
h1 { font-size:26px; margin:0 0 4px; letter-spacing:-.02em; }
.sub { color:#5b6470; font-size:13.5px; }
.banner { background:#fff7d6; border:1px solid #e8d99a; border-radius:10px;
  padding:10px 14px; font-size:13.5px; margin:14px 0 0; color:#6b5a12; }
h2 { font-size:15px; text-transform:uppercase; letter-spacing:.08em; margin:34px 0 12px;
  padding-bottom:6px; border-bottom:2px solid #e3e6ea; display:flex; align-items:center; gap:8px;}
h2 .count { font-weight:500; color:#8a919b; text-transform:none; letter-spacing:0; font-size:13px;}
.card { background:#fff; border:1px solid #e3e6ea; border-radius:12px;
  padding:14px 16px 12px; margin-bottom:12px; box-shadow:0 1px 2px rgba(16,24,40,.04); }
.top { display:flex; align-items:baseline; gap:10px; margin-bottom:6px; flex-wrap:wrap;}
.handle { font-weight:650; font-size:14px; text-decoration:none; color:#1a1d21; }
.handle span { color:#5b6470; font-weight:450; }
.pill { font-size:11.5px; font-weight:650; padding:2px 8px; border-radius:99px; }
.tier { font-size:11px; color:#8a919b; border:1px solid #e3e6ea; border-radius:99px; padding:1px 7px;}
.txt { white-space:pre-wrap; font-size:14.5px; margin:2px 0 8px; }
.why { font-size:13px; color:#0e7a4f; background:#f2faf6; border-left:3px solid #bfe3d0;
  padding:6px 10px; border-radius:0 8px 8px 0; margin:0 0 8px; }
.meta { display:flex; gap:14px; font-size:12.5px; color:#8a919b; flex-wrap:wrap; }
.meta a { color:#1d5fa8; text-decoration:none; font-weight:600; }
footer { margin-top:40px; font-size:12.5px; color:#8a919b; text-align:center; }
"""


def fmt_n(n):
    if n is None:
        return "–"
    n = int(n)
    return f"{n/1000:.1f}k" if n >= 1000 else str(n)


def card(c, accent, bg):
    handle = c.get("author_handle") or "unknown"
    name = c.get("author_name") or ""
    url = c.get("url")
    link = f'<a class="handle" href="{html.escape(url)}">' if url else '<span class="handle">'
    link_close = "</a>" if url else "</span>"
    why = f'<div class="why">{html.escape(c["why"])}</div>' if c.get("why") else ""
    tier = f'<span class="tier">{c["tier"]}</span>' if c.get("tier") else ""
    when = ""
    if c.get("created_at"):
        try:
            when = datetime.fromisoformat(c["created_at"]).strftime("%a %b %-d")
        except ValueError:
            when = c["created_at"][:10]
    open_link = f'<a href="{html.escape(url)}">Open on X →</a>' if url else ""
    media = f"· {c['media_type']}" if c.get("media_type") else ""
    return f"""
    <div class="card">
      <div class="top">
        {link}@{html.escape(handle)} <span>{html.escape(name)}</span>{link_close}
        <span class="pill" style="color:{accent};background:{bg}">{c.get('score','')}</span>
        {tier}
      </div>
      <div class="txt">{html.escape(c.get('text') or '')}</div>
      {why}
      <div class="meta">
        <span>♥ {fmt_n(c.get('likes'))}</span><span>⇄ {fmt_n(c.get('retweets'))}</span>
        <span>{when} {media}</span><span>via {html.escape(c.get('source') or '')}</span>
        {open_link}
      </div>
    </div>"""


def main():
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "data" / "latest.json"
    dst = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "digest" / "latest.html"
    data = json.loads(src.read_text())
    cands = data.get("candidates", [])

    def sort_key(c):
        return (0, c["final_rank"]) if c.get("final_rank") else (1, -c.get("score", 0))

    sections = ""
    for key, label, accent, bg in BUCKETS:
        group = sorted([c for c in cands if c.get("bucket_guess") == key], key=sort_key)
        if not group:
            continue
        cards = "\n".join(card(c, accent, bg) for c in group)
        sections += f'<h2 style="color:{accent}">{label} <span class="count">{len(group)} candidates</span></h2>\n{cards}\n'

    w = data.get("window", {})
    demo = ('<div class="banner">Demo digest — built from historical FF Newsletter '
            "picks to preview the format and validate the scoring rubric.</div>"
            if data.get("demo") else "")
    kept = data.get("counts", {}).get("kept", len(cands))
    raw = data.get("counts", {}).get("raw", "?")
    html_out = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>FF Tweet Scout — Weekly Digest</title><style>{CSS}</style></head><body>
<div class="wrap">
<header>
  <h1>🏈 FF Tweet Scout — Weekly Digest</h1>
  <div class="sub">Window {w.get('since','?')} → {w.get('until','?')} ·
  {kept} candidates from {raw} collected · generated {data.get('generated_at','')[:16]}</div>
  {demo}
</header>
{sections}
<footer>FF Tweet Scout · scored against docs/taste-profile.md · for The FF Newsletter</footer>
</div></body></html>"""

    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(html_out)
    print(f"Wrote {dst} ({len(cands)} candidates)")


if __name__ == "__main__":
    main()
