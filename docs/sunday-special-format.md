# Sunday Special — format & pipeline spec

*Sunday-morning Season Pass edition. Collection: the 14:30 UTC Sunday cron (news
mode, Thu→Sun window + the 7:30am PT sweep). Build: Claude session, send 8:30am
PT / 11:30am ET. Companion to substack-format.md, which governs voice and paste
mechanics; this file covers what's different on Sundays.*

## Principle

**The tweet is the item.** Same edge as the Thursday letter: we read all of
Sunday-morning fantasy Twitter so the reader doesn't. Our value-add is the
tiering, the Wednesday-thread continuity, and one written distillation (the
injury wire). Never paraphrase what a linked website says when a tweet exists.

## Source fallback (in order)

1. **Tweet from the pull** — embed it (bare x.com URL on its own line; Substack
   auto-embeds). One-line house-voice setup only when the tweet needs framing.
2. **Web fallback** — when a content class has no usable tweet in the pull
   (thin weather week, no matchup thread), write the item in house style from a
   web source (RotoWire/weather.com/team sites) with the attribution as the
   item's one link. Mark nothing; it should read seamlessly.
3. Never skip a section because the tweet pull was thin.

## Sections, in order

1. **Intro** — two sentences, kickoff countdown.
2. **☔ Weather** — anchor embed: the RuvenKotz slate report; then Worst / Not
   notable / Best tier lines covering EVERY game incl. SNF/MNF.
3. **🌡️ Game Environment** — totals/game-script tweets + tier lines, every game.
4. **🔬 Matchup Lab** — WR/CB + RB/DL tweets (web fallback common here),
   Best / Not notable / Worst.
5. **🧾 Receipts** — grade last Sunday's calls (and any Thursday call that
   resolved): one line each, hit or miss, no hiding. Tweet-archaeology or the
   box score supplies the evidence.
6. **🧵 Still Open from Thursday** — ONLY live decisions/warnings, each closed
   by a fresh tweet where one exists.
7. **🚑 Injury Wire (11:30 ET)** — bullet lines (no tables; they don't survive
   the Substack paste): `Name, POS TEAM – STATUS (injury) – prognosis/snap
   note`, sorted by fantasy relevance; offense only; skip pre-existing
   season-enders. **Pending** sub-list names every fantasy-relevant GTD by
   window (4:05 / 4:25 / SNF / MNF) with when their actives drop — never a bare
   "check later" row. Beat-tweet receipts embedded beneath.
8. **📺 Streamers + Stat Watch** — streamer recs gated <50% rostered in
   standard redraft, % cited; kicker/DST weather overlay; one stat-watch line.
9. **🏆 Trophy Room Mailbag** — 2-3 member questions from Discord, answered in
   two info-first sentences each. Members by first name/handle.
10. **Send-off** (emoji allowed here only).

## Gates

- Dedupe vs. Wednesday's issue (exact tweet id + same-stat fuzzy).
- Comment check via reply_sample on every near-pick.
- Numbers sanity-check vs. known magnitudes.

## Discord addendum

~2:45pm ET, a short late-window update (actives for 4:05/4:25, anything that
broke bad) posts to the Trophy Room via `DISCORD_WEBHOOK_URL` repo secret
(Server Settings → Integrations → Webhooks; POST {"content": "..."} to the
webhook). Members-only; the newsletter plugs it.
