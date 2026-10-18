# Sunday Special — format & pipeline spec

*Sunday-morning Season Pass edition, branded "11th Hour." Collection: Sunday
cron (news mode, Thu→Sun window) + inactives sweeps. Build: Claude session
starts 10:00am ET sharp; DRAFT in Chris's hands by 10:30am ET, full issue with
the EXPECTED wire by ~11:00am ET (Chris, 10/11 — the old wait-for-officials
flow shipped too late to act on). Companion to substack-format.md, which
governs voice and paste mechanics; this file covers what's different on
Sundays.*

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

## Writing rules

- Every section opens with ONE plain line saying what it is / how to use it
  (Matchup Lab's notes that WR/DB edges are more predictive than RB/DL ones).
- Useful over clever: no coined shorthand ("fence case"), no vague callbacks.
  Every line should tell the reader something they can act on.
- Tier and matchup content renders as bulleted lists, never prose blobs.

## Sections, in order

1. **Intro** — two sentences, kickoff countdown.
2. **☔ Weather** — anchor embed: the RuvenKotz slate report; then Worst / Not
   notable / Best tier lines covering EVERY game incl. SNF/MNF.
3. **🌡️ Game Environment** — game-script tweets + tier lines, every game.
   **Fantasy-first framing (Chris, 10/10): this is not an odds column.** Each
   line LEADS with the fantasy consequence — expected pace, volume, game
   script, who gains or loses touches — and carries the total and spread only
   as a compact parenthetical data point, e.g. "(44.5, ARI -2.5)". No
   sportsbook voice anywhere in the section: no "chalk," "cover," "fade the
   number," "the books," "cashes," or betting-pick framing; "fade" survives
   only as a fantasy start/sit verb aimed at players, never at teams against
   a line. Make shootouts and one-sidedness pronounced (member request,
   Trophy Room 9/12): projected-close high-scoring games bump everything;
   projected-lopsided games hand the stronger team's early-down RB the
   closing script while the weaker team's RBs and the stronger team's
   secondary pass-catchers lose late-game work — say which players that
   touches, one clause, no essay. Line-vetting (the three-book cross-check)
   is an internal process: surface discrepancies to Chris in the delivery
   note, never in the letter body.
4. **🔬 Matchup Lab** — DEFENSIVE MATCHUPS ONLY (Chris, 10/18): every item is
   a player-vs-defense edge grounded in coverage scheme (1-high/Cover 3 rates
   vs a player's per-route splits), front/run-fit data (stuff rate, yards
   before/after contact, scheme-on-scheme like outside-zone vs an
   outside-zone-killing front), or personnel (a shadow corner, a returning DB,
   a missing nickel). NEVER a restatement of injuries (wire's job),
   environment/script (Environment's job), or usage trends with no defensive
   component. WR/CB + RB/DL tweets are the backbone (web fallback common);
   Best / Worst tiers.
5. **🧾 Receipts** — LAST SUNDAY'S calls only (never Thursday content): one
   line each, what we called, what happened, hit or miss.
6. **🧵 Threads We Were Waiting On** — closes out the NON-INJURY storylines
   Thursday's issue left open (Chris, 10/11): role decisions, trades, QB
   pecking orders, usage trends, Waiver Weapon / Trade Target follow-through —
   with the resolving tweet where one exists. Injuries are explicitly NOT this
   section's job — the wire owns every status, and this section at most points
   to it ("if he plays - see wire"). Not a place to re-reference stats that
   already appear elsewhere in the issue.
7. **🚑 Injury Wire (EXPECTED — ships ~10:30-11:00 ET; Chris, 10/11)** — the
   wire no longer waits for the official inactives. It ships WITH the issue
   carrying the latest reads: IN/OUT solid badges only for formal rulings
   (Friday ruled-out/IR, official announcements); EXP IN/EXP OUT hollow
   badges for reported leans; PENDING amber for true game-time calls with no
   lean. Any player who FLIPS when the ~11:30 ET official inactives post gets
   trued up in the Trophy Room Discord (Chris posts; the session supplies the
   flip list from the post-officials sweeps). The issue's wire intro tells
   readers to watch the Discord for the true-up. Format: a TABLE: Player | Status | Injury |
   Prognosis, sorted by fantasy relevance; offense only; skip pre-existing
   season-enders. **Rendering:** Substack has no native tables and its LaTeX
   block is single-line MathJax, so the wire ships as an image. Source of
   truth is `data/sunday/injury-wire.md` (a markdown table anyone can edit in
   the GitHub web editor); the `render-wire` Action re-renders
   `assets/sunday/injury-wire.png` (+ a dated copy) within ~2 min of any
   commit to it. The paste doc embeds the raw.githubusercontent URL with the
   full table content in the alt text (screen readers / image-blocked email).
   **Pending** sub-list names every fantasy-relevant GTD by window
   (4:05 / 4:25 / SNF / MNF) with when their actives drop — never a bare
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
- **Team attribution (hard rule, added 9/27 after Kyler-to-MIN shipped wrong in
  the Week 2 wire; same failure as Likely-to-NYG and Montgomery-off-DET):
  a player's team NEVER comes from the model's memory.** Every named player in
  the wire, matchup lab, designations, and streamers carries a team sourced
  from (a) the quoted tweet's own text, or (b) a fresh web check. A tweet that
  names a player without a team gets verified before the row is written — or
  the team is omitted. 2026 rosters have moved too much for priors.
- **Wire exhaustiveness + two-tier sourcing:** the wire is built efficiently in
  two passes. (1) **1:00 games — official only:** statuses come from each
  team's official inactives post (~11:30 ET, via the inactives sweep); these
  are LOCKED and render IN/OUT. No Twitter-sniffing needed where an official
  list exists. (2) **Late windows + SNF/MNF — latest reporting:** Friday
  ruled-out/IR designations are official (OUT); everything else is the most
  recent beat read, rendered EXP IN / EXP OUT (hollow badge = not locked),
  with the lock time in the prognosis. Every fantasy-relevant offensive player
  appears — including healthy scratches and benchings, which cost a reader's
  lineup exactly like injuries do. Late-window and MNF question marks get
  named, never summarized away.

## Discord addendum

~2:45pm ET, a short late-window update (actives for 4:05/4:25, anything that
broke bad) posts to the Trophy Room via `DISCORD_WEBHOOK_URL` repo secret
(Server Settings → Integrations → Webhooks; POST {"content": "..."} to the
webhook). Members-only; the newsletter plugs it.
