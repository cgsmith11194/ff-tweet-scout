# The FF Newsletter — Tweet Selection Taste Profile

*Derived from 7 issues of theffnewsletter.substack.com (Nov 2025 – Jul 2026), ~380 embedded tweets. This document is the ranking brain for the weekly tweet scout: the deterministic pre-scorer in `collector.py` implements the weights, and the weekly Claude session uses the archetypes + exemplars below for final taste ranking.*

---

## 1. What the newsletter is

A weekly (Thursday AM, in-season) digest of "the best fantasy football headlines from each week," built almost entirely from curated tweets organized into recurring sections:

| Section | Tweets/issue | Character |
|---|---|---|
| Analysis & Hype | 19–45 | Positive-direction stat nuggets: efficiency, usage, historical pace |
| Cold Water | 7–20 | Same formats, negative direction: declines, unsustainability, structural concerns |
| Waiver Weapons | 0–2 | Matchup/opportunity stats supporting adds |
| Trade Target Thursday | 0–1 | Prose + occasional supporting tweet |
| The Fun Stuff | 11–24 | Videos, absurd stats, quotes, memes |

**Editorial voice:** objective, numbers-first, information-dense. A pick almost always contains a *specific number with context* (a rank, a threshold, a historical frame, a split). Pure opinion tweets essentially never make Analysis/Cold Water.

## 2. Source leaderboard (observed appearances, 7 recent issues)

**Tier 1 — the backbone (~55% of analysis picks):**
@Ihartitz (~34 — alone ~10% of all picks), @ffdataroma (~15), @GuruFantasyWrld (~11), @SmolaDS (~9), Underdog/@UnderdogNFL (~12 combined), @kyle_borg (~8), @jagibbs_23 (~7), @LateRoundQB (~7), @CoopAFiasco (~6), @BenjaminSolak (~6), @danorlovsky7 (~5), @dynasty_im (~5), @ChrisWechtFF (~5), @MySportsUpdate (~5), @MikeClayNFL (~4), @FantasyPtsData (~4), @HaydenWinks (~4), @YahooFantasy (~4)

**Tier 2 — regulars (2–3 each):**
@MattHarmon_BYB, @ScottKacsmar, @LordReebs, @DavisMattek, @TheFFBallers, @tejfbanalytics, @heathcummingssr, @adamlevitan, @dwainmcfarland, @RyanMc23, @TheoAshNFL, @nflplus, @SleeperNFL, @JoshNorris, @koestreicher34, @BenFennell_NFL, @DrakeFantasy, @EvanRinglerFF, @fantasysmyth, @zm_cox, @kyle... plus credible one-timers worth monitoring: @TheFantasyPT, @Michael_Nania, @PFF_NateJahnke, @NFL_Researcher, @DynastyZoltanFF, @ryanj_heath, @JoRo_NFL, @SigmundBloom, @dave_bfr, @Nate_Tice, @AustinAbbottFF, @PFF_Fantasy, @PFF_RyanSmith

**Fun Stuff regulars:** @mlfootball (~7), @NFL_DovKleiman, @SharpFootball, @NFLMemes/@NFL_Memes, @Schultz_Report, @JayCuda, @PeteBlackburn, @bykevinclark, @upandadamsshow

**Key structural fact:** ~40% of picks come from accounts featured only once in the sample (@jnradio_glenn, @vikingzfanpage, @Devoted2DET, @kentweyrauch…). The *format* travels, not the byline — which is why the scraper also runs stat-pattern searches, not just account timelines.

## 3. The seven archetypes that get picked

### A. Bulleted stat block with rank context (the signature format)
Multiple `•` lines, each a stat + parenthetical rank. Maximum info per pixel.
> **@PFF_RyanSmith:** De'Von Achane on the ground this season: • 90.7 PFF run grade (1st) • 4.10 yards after contact per attempt (1st) • 42 missed tackles forced (8th) • 35 runs of 10+ yards (1st)

> **@ffdataroma:** Tetairoa McMillan over the past month: • 29.8% target share (6th in NFL) • 36.1% 1st read target share (8th) • 39.5% of team's receiving yards (3rd) • 15.9% 1st downs per route rate (3rd)

### B. Ranked mini-leaderboard
"1. X 2. Y 3. Z" with values; often with a twist entry that IS the story.
> **@jagibbs_23:** Fantasy Points per Route Run Leaders in 2025: 1. Jaxon Smith-Njigba: 0.81 2. Puka Nacua: 0.74 3. Amon-Ra St. Brown: 0.60 …

> **@danorlovsky7:** QB EPA leaderboard if you exclude drops: 1. Drake Maye (104.1) 2. Jordan Love (81.2) …

### C. Historical "only club" / first-since framing
A short list mixing Hall of Famers with one surprising current name — the surprise is the pick.
> **@nflplus:** Players with 7,000+ rush yards and 70+ touchdowns prior to turning 27: • HOF Emmitt Smith • HOF Jim Brown • HOF LaDainian Tomlinson • Jonathan Taylor

> **@Ihartitz:** The only rookie wide receivers to score 100+ PPR points in their first five career games: • Randy Moss • Puka Nacua • Emeka Egbuka

### D. Split comparison (with/without, before/after, week-range)
Second-level causal framing: teammate presence, coaching change, scheme shift.
> **@SmolaDS:** Puka Nacua scored 4 TDs on a 14.8% TD rate in 3 games without Davante Adams last year. He scored 6 TDs on a 5.9% TD rate in 13 games with Adams.

> **@ffdataroma:** Vikings without vs. with JJ McCarthy starting: Without: • Pass rate over expectation: 4.6% • Pass attempts per game: 35.4 (8th) With: • −3.3% (30th) • 22.0 (dead last)

### E. Structural / second-level angle (coach, contract, O-line, market)
The "beyond 'this coach likes running the ball'" category — tendencies *quantified*, incentives priced, market inefficiency named.
> **@JoshNorris:** Not a single RB has ever hit 250 carries under Sean Payton for his entire tenure as head coach. J.K. Dobbins' 15.3 carries per game last year were the 4th most by a RB across Payton's 18 seasons.

> **@CoopAFiasco:** If Stefon Diggs averages 4-5 catches a game for ~75 yards to close things out, he can make an extra $1.5 to $2M.

> **@GuruFantasyWrld:** If you cut Davante Adams' TD production in half last year (from 14 to 7), he still would've finished as the WR21 in PPG (12.9). He is priced as the WR26 this year.

> **@SmolaDS:** Mike McDaniel offenses' ranks in plays, pace, and situation-neutral pace: • 2022: 27th/20th/23rd … • 2025: 31st/31st/32nd

### F. One-line dagger
A single sentence, one or two numbers, devastating implication. Heavy in Cold Water.
> **@ffdataroma:** Chuba Hubbard did not have a single explosive rush on 134 carries.

> **@MikeClayNFL:** Ricky Pearsall in his first game back: • 84% snap rate • 0 yards.

> **@MikeClayNFL:** One quarterback has finished Top 12 in fantasy points in each of his last 4 games: Jacoby Brissett.

### G. Fun Stuff
Video moments, absurd probability/history, quotes, self-aware league humor. Engagement matters more here; analysis doesn't.
> **@JayCuda:** The Panthers are 6-0 when they have won the opening coin toss, while also being 0-5 when they've lost.

> **@BenWolby:** Most receiving yards over the age of 40: • Jerry Rice: 2509 • Tom Brady: 6 • Marcedes Lewis: 2 • Everybody ever: 0 • Brett Favre: −2 • Aaron Rodgers: −9

> **@CoachspeakIndex:** HC Mike McCarthy described Rico Dowdle as "a bowling ball full of butcher knives" when they were together in Dallas

## 4. Anti-patterns (never picked — auto-kill or heavy penalty)

- **Injury news / insider reporting** (Schefter-style "out 4-6 weeks") — the newsletter assumes you saw the news; it picks the *stat about the consequence* instead
- **First-level takes** — "X had a lot of catches last year," "this offense will be good," vibes-only camp reports
- **Promos, giveaways, discount codes, "RT to win," subscribe links** as the tweet's purpose
- **Rankings screenshots without an argument** (exception: a tweet whose text itself carries the insight)
- **Polls and engagement bait**
- **Betting picks/slips**
- **Replies** (picks are top-level tweets; self-thread heads are fine)

## 5. Scoring rubric

### Deterministic pre-score (collector.py, 0–100)
| Signal | Points |
|---|---|
| Bulleted/numbered list structure (per line, cap) | up to +22 |
| Stat density (digits, %, decimals per 100 chars) | up to +18 |
| Insight markers: "only … since", "first … since", "in NFL history", "min. N", "on pace", "would rank/finish", "career high/low" | up to +18 |
| Split markers: with/without, weeks A–B vs C–D, before/after, "in games both played" | up to +12 |
| Second-level markers: coach-tendency, contract $, O-line, pace/PROE, "over expected", per-route/per-carry rates, priced/ADP vs production | up to +14 |
| Account tier (T1 +14, T2 +8, fun-list +6 in fun bucket) | up to +14 |
| Engagement (log-scaled within batch) | up to +10 |
| Kills: promo/giveaway (−100), poll (−100), reply (−100), pure link tweet (−60), injury-news phrasing (−35) | negative |

### LLM final ranking (weekly session)
Rank the top pre-scored candidates by fit to the archetypes above, enforcing: (1) every Analysis/Cold Water pick must convey a specific, checkable number with context; (2) prefer second-level causal framing over raw production recaps; (3) diversity guardrails — max ~4 per account, spread across positions/teams, both directions (hype AND cold water); (4) 10–15 Analysis & Hype, 6–10 Cold Water, 5–8 Fun Stuff; (5) one-line "why it fits" per pick, naming the archetype.

### Seasonality
- **In-season (Sep–Dec):** weekly usage splits, week-range leaders, waiver-relevant opportunity stats, matchup daggers.
- **Offseason (Jan–Aug):** historical pace/comps, ADP/market-vs-production gaps, coaching-change quantification, camp usage signals, best-ball structure data.
