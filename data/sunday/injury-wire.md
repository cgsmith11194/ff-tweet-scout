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
| Alvin Kamara | RB · NO | OUT | Knee (MCL) | Inactive; full participant late in the week but not ready |
| Brock Bowers | TE · LV | OUT | Knee (meniscus) | Ruled out; real chance he returns Week 2 — Mayer inherits |
| A.J. Brown | WR · NE | OUT | Ankle | IR — out about six weeks; Kyle Williams is the beneficiary |
| Tua Tagovailoa | QB · ATL | OUT | Oblique | Inactive along with Penix; Rush starts, Zaccheaus is emergency QB and RB3 |
| Josh Jacobs | RB · GB | OUT | — | Commissioner Exempt list; not with the team (4:25) |
| Emeka Egbuka | WR · TB | IN | — | Not among Tampa's inactives — active after a questionable week |
| Rome Odunze | WR · CHI | IN | Calf | Officially active |
| Alec Pierce | WR · IND | IN | Heel | Plays but not a full go — roughly 20-30 plays with in-game spells |
| Cooper Rush | QB · ATL | IN | Back spasms | Active; felt better Sunday morning |
| Jalen McMillan | WR · TB | OUT | Knee | Inactive |
| Sean Tucker | RB · TB | OUT | Hamstring | Out; goal-line work consolidates behind Irving and Gainwell |
| Tim Patrick | WR · TEN | OUT | Groin | Ruled out Friday |
| Ty Johnson | RB · BUF | OUT | Hamstring | Inactive; small receptions bump to James Cook |
| Jeremiyah Love | RB · ARI | EXP IN | Ankle sprain | Expected to play per Rapoport — locks at ~3:55 ET actives |
| Malik Nabers | WR · NYG | PENDING | Knee | True game-time decision, "murky at best" — SNF actives ~6:50 ET |
| GB@MIN · MIA@LV · WAS@PHI |  | PENDING | — | No other fantasy-relevant GTDs reported; actives ~3:55 ET |
| DEN@KC | MNF | PENDING | — | Statuses Monday; Mahomes is back from the ACL and off the report |
