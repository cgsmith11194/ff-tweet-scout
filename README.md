# FF Tweet Scout

Weekly tweet collector + ranker for [The FF Newsletter](https://theffnewsletter.substack.com). Finds tweets that match the newsletter's taste — dense bulleted stat blocks, historical "only club" framing, with/without splits, quantified coaching tendencies, market-vs-production gaps — and stages them for Thursday's issue.

## How the week flows

```
Wed 3:00pm PT   GitHub Actions (this repo)
                └─ collector.py: pulls trailing-7-days tweets via Apify
                   (45+ tracked accounts + 8 stat-pattern searches),
                   dedupes, kills promos/replies/injury-news,
                   scores 0–100 against the taste rubric
                   → data/latest.json (top ~160 candidates)
                └─ render_digest.py → digest/latest.html (heuristic fallback)

Wed 5:00pm PT   Claude (scheduled Cowork task)
                └─ reads data/latest.json from this repo,
                   applies docs/taste-profile.md for final taste ranking,
                   delivers the styled digest in chat
```

If the Claude session ever misses a week, `digest/latest.html` in this repo is a purely-heuristic version of the same digest.

## Files

| Path | Purpose |
|---|---|
| `collector.py` | Apify collection + normalization + scoring |
| `render_digest.py` | Renders candidates → self-contained HTML |
| `config/sources.yaml` | Accounts (tiered), searches, caps — **edit this to tune** |
| `docs/taste-profile.md` | The selection-taste analysis + rubric (the "brain") |
| `data/latest.json` | Most recent candidate set (overwritten weekly) |
| `data/candidates-YYYY-MM-DD.json` | Weekly archive |
| `digest/latest.html` | Heuristic fallback digest |
| `.github/workflows/collect.yml` | Wednesday cron |

## Costs

kaitoeasyapi actor ≈ $0.25 / 1,000 tweets; typical week ≈ 2–3k tweets ≈ **$0.50–0.75/week**, inside Apify's free-plan $5/month credit. Volume knobs: `account_query.max_items` and each search's `max_items` in `config/sources.yaml`.

## Tuning

- Add/remove accounts in `config/sources.yaml` (tier affects scoring).
- Add a search when you notice a stat pattern you like that we're missing.
- Raise `min_faves` on noisy searches; lower `keep_top` for a tighter file.
- Scoring weights live at the top of `collector.py` (`WEIGHTS`).
