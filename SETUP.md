# Setup — one-time, ~10 minutes

## 1. Apify (the tweet data source)

1. Create a free account at [apify.com](https://apify.com) (free plan includes **$5/month in usage credit** — our ~2–3k tweets/week ≈ $0.50–0.75/week fits inside it).
2. Go to **Settings → API & Integrations** and copy your **Personal API token**.

## 2. GitHub repo (the engine room)

1. Create a new repo, e.g. `ff-tweet-scout`. **Public is recommended** (free unlimited Actions minutes, and Claude can read the data without a token). The only things stored here are code and public tweets — your Apify token lives in encrypted secrets, never in the repo.
2. Upload the contents of this folder to the repo root (drag-and-drop on github.com works, or `git push`). Keep the folder structure, including `.github/workflows/collect.yml`.
3. In the repo: **Settings → Secrets and variables → Actions → New repository secret**
   - Name: `APIFY_TOKEN`
   - Value: the token from step 1.

## 3. First run (validates everything)

1. Go to the **Actions** tab → enable workflows if prompted.
2. Select **weekly-collect** → **Run workflow** (the manual button).
3. Wait ~3–6 minutes. When it's green, confirm the repo now contains:
   - `data/latest.json` — the scored candidates
   - `digest/latest.html` — the heuristic fallback digest
4. Sanity-check cost: Apify console → your actor run should show a couple thousand results ≈ well under $1.

## 4. Tell Claude

Reply in the Cowork chat with your repo URL (e.g. `github.com/you/ff-tweet-scout`). Claude will then create the **Wednesday 5pm PT** scheduled task that reads `data/latest.json`, does the final taste-ranking against `docs/taste-profile.md`, and delivers the styled digest in chat every week.

> Prefer not to click through all this? Paste a GitHub personal access token (repo scope) + your Apify token in chat instead, and Claude will create the repo, push the code, set the secret, and kick off the first run for you via the GitHub API.

## Notes

- **Schedule**: Actions cron fires Wed 22:00 UTC (3pm PDT / 2pm PST); the Claude digest task fires Wed 5pm PT in summer (4pm PST in winter — UTC-pinned; say the word if you want it shifted each DST change).
- **Private repo variant**: works too, but Claude needs a fine-grained read-only PAT to fetch `data/latest.json`; you'd provide that when Claude sets up the scheduled task.
- **In-season tuning**: expect higher volume Sep–Dec; if a week's run nears your Apify credit, lower `max_items` values in `config/sources.yaml`.
