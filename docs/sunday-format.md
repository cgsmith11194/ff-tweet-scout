# Sunday Brief — format & content spec

*In-season Sunday AM edition (regular season only). The Sunday scheduled session fetches this file; edit it anytime to tune sections, voice, or thresholds. All general house rules from `docs/substack-format.md` apply — bulleted lists (never comma run-ons), exactly one link per item on the fantasy-takeaway name, no emojis or ALL-CAPS, light declarative rewording, never alter or invent a number.*

## Purpose

Not a stats digest — Thursday owns analysis. Sunday closes loops and arms decisions: what we told readers to watch, what broke since Thursday morning, and what's actionable before lineups lock.

## Sections, in order

### 1. Closing the Loop

Every "developing / something to watch / keep an eye on" item from Thursday's free edition, resolved.

Format per item:
> **[Player/situation]** — Thursday we flagged {one-clause recap}. {What actually happened: designation, practice pattern, beat reporting, depth-chart move}. The read: {one clause — start/sit/pivot implication}.

Rules: pull the watch items from the actual published Thursday post (never from memory); if an item is still unresolved, say "still open" honestly rather than forcing a conclusion; link on the player name to the best source (tweet from the collection, or the report).

### 2. Since Thursday

Late-breaking NEWS since Thursday morning — updates, not analysis. Grouped bullets:

- **Out / IR** — ruled-out players with the one-line beneficiary read
- **Game-time calls** — notable Questionable tags with the practice-week pattern (DNP-DNP-LP etc.) and expected pregame decision timing
- **Roster moves** — elevations, activations, signings that matter for lineups
- **Coachspeak that matters** — usage-changing quotes only

Every bullet: link on the player name (candidate `url` field or fetched source). Fantasy-relevant only — no big-picture league news unless it changes a lineup decision today.

### 3. The Actionables

- **Line moves** — diff today's odds snapshot against Wednesday's (`data/odds-*.json`). Report moves of ≥1.0 point (spread) or ≥1.5 (total):
  > • {AWAY @ HOME}: spread {opened} → {now}; total {opened} → {now}. The read: {pace/gamescript implication in one clause}.
  Arithmetic must be recomputed in code, never eyeballed.
- **Weather watch** — only games where weather is actionable: sustained wind ≥15 mph or gusts ≥25, precip ≥50%, temp ≤15°F. One bullet per flagged game with the read (downgrade deep passing/kickers, boost run rate). Domes/closed roofs never appear (see `config/stadiums.yaml`). If nothing qualifies: one line — "No weather worth planning around this week."

## Voice

Same newsletter voice, tightened for morning scanning: short declaratives, "The read:" pattern for implications, no hedging padding ("we'll see!"), no filler intros. Length target: readable in three minutes.

---

# Inactives Addendum (separate deliverable, ~12:10pm ET)

Official inactives drop 11:30am ET (90 min before early kickoff) — after the main brief ships. A second light pull runs ~11:45am ET (`data/inactives-latest.json`), and the addendum lands ~12:10pm ET / 9:10am PT as its own short paste-ready block to slot in before sending.

Sections:

- **Inactives — early window**: notable inactives only (fantasy-relevant players, surprise scratches), grouped by game. Each bullet: player, status, and the beneficiary read ("• [Player] inactive — {backup} inherits the early-down work"). Full 7-inactive lists are noise; relevance only.
- **Game-time calls, resolved**: every Questionable player the main brief flagged as a game-time decision → active or inactive.
- **Late window / primetime — best known**: reported expectations for 4pm ET and primetime games (clearly labeled as reports, not official).

Rules: official-designation claims must trace to an insider/beat tweet in the pull or a fetched source — never inferred. If the pull is stale or empty, deliver a diagnostic, not guesses. Keep the whole addendum under ~20 bullets; it's a delta, not a second brief.
