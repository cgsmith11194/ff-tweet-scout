# Substack paste format — house style

*The weekly Claude session fetches this file to build the paste-ready Substack doc. Edit it anytime to tune the voice — changes take effect the next Wednesday.*

## Structure

- Sections in order, as H2 headings: **Analysis & Hype**, **Cold Water**, **The Fun Stuff**.
- Each pick = one paragraph. Multi-stat tweets keep their list structure as line breaks, using the tweet's own style: `1.` numbering for leaderboards, `•` bullets for stat blocks. En dashes (–) between name and value.
- **Lists get bullets, not comma run-ons.** Any list of names, teams, or setup points (an "only club," camp-buzz names, a multi-point situation breakdown) renders as a `•` bulleted list — one entry per line — never as a long comma string inside a sentence. A comma list is acceptable only for ≤3 short names sharing one value ("Purdy, Jackson, and Herbert, all at −1").

## Rewriting rules (Analysis & Hype / Cold Water)

- Light declarative rewording — read like the newsletter wrote it, not like a screenshot.
- **Strip:** emojis, hashtags, trailing t.co links, ALL-CAPS names (→ proper case), engagement-bait closers ("Thoughts? 🤔", "agree/disagree?", "BUYER-BEWARE"), @-handle noise, tweet-thread artifacts.
- **Keep:** attributions that carry credibility ("per NextGenStats", "PFF grade", "via ESPN"), qualifying thresholds ("min. 175 attempts"), age/year context.
- **Never** alter a number, rank, or name; never add facts not in the tweet. If the tweet jokes a value away (e.g. "(ok ok ok)" instead of a number), omit it — don't invent it.
- **Exactly one hyperlink per item**, on the name that carries the **fantasy takeaway** → the tweet's x.com URL. Link the player or TEAM whose outlook the stat changes going forward — not merely the grammatical subject. Examples: a coaching-change stat links the team affected now (Kubiak's yards-before-contact jumps → link **Raiders**, not Kubiak); a historical "only club" links the current-day member (→ Harold Fannin Jr., not Reggie Bush); a leaderboard links the surprising or actionable entry, wherever it sits in the list; occasionally the right anchor is a phrase ("FF Fallers if you remove Week 18"). Test: if a reader clicks exactly one thing, it should be the thing they'd draft differently because of.

### Before → after example

> **Tweet:** `Worst YAC/R Seasons in FP Data History + min. >55 targets — 1. MIKE EVANS, 2025 (1.33) [age 32] 2. Marvin Jones Jr., 2021 (1.81) ...`
>
> **Item:** Worst yards-after-catch-per-reception seasons on record (min. 55 targets):
> 1. [Mike Evans](https://x.com/...), 2025 (1.33) — age 32
> 2. Marvin Jones Jr., 2021 (1.81) …

## The Fun Stuff rules

Write an **original one-liner in the newsletter's voice**, with the link on the player's name or a short descriptive phrase. The voice: conversational, wry, first-person-plural ("we", "our readers"), light roasting, understated — never exclamation-mark spam, never try-hard.

**Short and punchy is the rule.** One sentence, roughly 15 words or fewer. The LINK carries the content — never re-list the tweet's details (stats, features, list entries) in the caption; the reader clicks to see the thing, the caption just lands the joke. If a line needs a second clause to explain itself, cut the clause. House-approved example: "The [Bills] have their priorities in order with the new stadium build."

House-voice reference lines (from past issues):
- "Kerryon Johnson is officially over it."
- "Bringing Josh Allen out to a playoff game in Buffalo went exactly how you'd expect it to go."
- "Did you say rivalry or robbery?"
- "Sometimes, it's the ones closest to you that hurt you the most - poor Joe Flacco."
- "Any of our readers Titans fans? Is it true that the Nissan Stadium experience is this terrible?"

New-line pattern examples (note the length — link does the work):
- "The [Bills](url) have their priorities in order with the new stadium build."
- "[Puka Nacua](url) put himself fifth on his own top-five list."
- "Zero running backs in this year's [Madden 99 Club](url)."

## Deliverable format

Self-contained HTML file named `FF-Substack-Paste-<YYYY-MM-DD>.html`: Georgia serif, single column, a small instruction note at top separated from the content by an `<hr>`. Everything below the rule is the paste region — H2 headers, `<p>` items with `<br>` line breaks, and `<a>` links all carry over when pasted into the Substack editor. Delivered every week **alongside** the ranked digest HTML, never instead of it.
