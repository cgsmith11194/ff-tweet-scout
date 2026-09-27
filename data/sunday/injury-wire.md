# Injury Wire source of truth
#
# Edit this table (GitHub web editor works fine, phone included), commit to main,
# and the render-wire Action regenerates assets/sunday/injury-wire.png within ~2 min.
# Rules:
#   - Columns: Player | Pos/Team | Status | Injury | Prognosis
#   - Status values (anything else renders as a gray badge):
#       IN / OUT    = LOCKED — official team inactives (1:00 games, posted ~11:30 ET)
#                     or a formal Friday ruled-out/IR designation (any window)
#       EXP IN / EXP OUT = latest beat reporting for late-window + island games —
#                     NOT locked (hollow badge); prognosis must say when it locks
#       PENDING     = no read at all yet; prognosis says when the answer lands
#   - Keep rows sorted by fantasy relevance; not-locked rows go last (the renderer
#     draws the section divider automatically before the first EXP/PENDING row)
#   - Leave Pos/Team empty for game-level rows (e.g. "GB@MIN · MIA@LV")
#   - Pipes (|) can't appear inside cell text; commas and dashes are fine

| Player | Pos/Team | Status | Injury | Prognosis |
|---|---|---|---|---|
| Kyler Murray | QB · MIN | IN | Concussion | Cleared protocol, starts at Tampa Bay (4:05) — Wentz back to the bench |
| Sam Darnold | QB · SEA | IN | Glute | Off the report entirely and starting — the Drew Lock streamer is dead |
| Caleb Williams | QB · CHI | OUT | Hamstring (Gr. 2) | Out 3-4 weeks; Keenum likely Monday, Bagent (concussion) questionable behind him |
| Nico Collins | WR · HOU | OUT | Hamstring | Second straight week; "decent chance" for Week 4 vs Dallas |
| Rico Dowdle | RB · PIT | OUT | Toe | Ruled out Friday — with Warren banged up, the Steelers room is thin |
| Michael Pittman Jr. | WR · PIT | IN | Foot | Will play, per Schefter |
| DJ Moore | WR · BUF | IN | Shoulder | Officially active |
| Keon Coleman | WR · BUF | IN | Ankle | Officially active |
| Jalen Coker | WR · CAR | IN | Ankle | Active — and Xavier Legette (knee) is officially inactive beside him |
| AD Mitchell | WR · NYJ | OUT | Finger | Officially inactive; Sterling Shepard elevated |
| Slayton + Singletary | NYG | OUT | — | Both HEALTHY inactives for the nor'easter game |
| Hollywood Brown | WR · PHI | OUT | — | Out Monday; Barkley and DeVonta Smith are both clean |
| Zay Flowers | WR · BAL | EXP OUT | Hamstring | "True game-time decision" and the team isn't counting on him — São Paulo actives ~2:55 ET |
| Brock Bowers | TE · LV | EXP IN | Knee | Expected "barring a surprise" — locks ~2:55 ET (4:25) |
| Jaylen Warren | RB · PIT | EXP IN | Shoulder | Expected per Schefter this morning — confirm at kickoff |
| Mike Evans | WR · SF | EXP IN | Hip | Good to go per reporting — locks ~2:35 ET (4:05) |
| Kaelon Black | RB · SF | EXP IN | Groin | Expected to play — locks ~2:35 ET |
| Jaylen Wright | RB · MIA | EXP OUT | — | Listed doubtful; Caleb Douglas is ruled out |
| Puka Nacua | WR · LAR | EXP OUT | Hip, groin | Doubtful for SNF, expected back Week 4 — locks ~6:50 ET; Whittington also doubtful |
