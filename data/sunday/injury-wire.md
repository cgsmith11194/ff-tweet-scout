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
| Zay Flowers | WR · BAL | OUT | Hamstring | Downgraded Saturday; the room behind him is Bateman-Walker-Wester |
| Nico Collins | WR · HOU | OUT | Hamstring | Ruled out Friday |
| Joe Burrow | QB · CIN | IN | Back | Officially active with no limitations — "totally good," per Burrow himself |
| Tua Tagovailoa | QB · ATL | OUT | Oblique | Inactive again; Rush starts vs CAR — Penix is out but nearing a return |
| Chris Olave | WR · NO | IN | Hamstring | Officially active |
| Alvin Kamara | RB · NO | IN | Knee | Off the report entirely — season debut |
| Jalen McMillan | WR · TB | IN | Knee | Active, but not a full-time role yet |
| Kyler Murray | QB · ARI | OUT | Concussion | Ruled out (4:25) |
| Chig Okonkwo | TE · TEN | OUT | Hamstring | Ruled out |
| Jauan Jennings | WR · SF | OUT | Personal | Ruled out (4:25) |
| Bears, entire roster | CHI | IN | — | Zero designations — first fully clean Bears report since Week 7, 2022 |
| Ladd McConkey | WR · LAC | EXP IN | Ribs | Trending the right way, flak jacket if he goes — locks ~2:35 ET actives |
| RJ Harvey | RB · DEN | EXP OUT | Hamstring | Unlikely per Schefter — locks ~2:35 ET actives |
| Brock Bowers | TE · LV | EXP OUT | Knee | Doubtful, expected back Week 3 — locks ~2:35 ET |
| Kaelon Black | RB · SF | EXP IN | Groin | Expected to play — locks ~2:55 ET |
| Michael Pittman Jr. | WR · IND | PENDING | Foot | Questionable for SNF — actives ~6:50 ET |
| Puka Nacua | WR · LAR | EXP OUT | Hip | Trending the "wrong way" per Schefter; true game-time call Monday — Whittington also doubtful |
