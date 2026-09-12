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
#   - Keep rows sorted by fantasy relevance; PENDING rows go last (the renderer
#     draws the section divider automatically before the first PENDING row)
#   - Leave Pos/Team empty for game-level rows (e.g. "JAX@DEN · LV@HOU")
#   - Pipes (|) can't appear inside cell text; commas and dashes are fine

| Player | Pos/Team | Status | Injury | Prognosis |
|---|---|---|---|---|
| Tee Higgins | WR · CIN | IN | — | Questionable during the week — active for the 1:00 |
| Lamar Jackson | QB · BAL | IN | Illness | Full practice Thursday — full go (SNF) |
| CeeDee Lamb | WR · DAL | IN | Illness | Returned Friday — full go |
| Alvin Kamara | RB · NO | OUT | Ankle/knee | Inactive; committee behind him, no announced lead |
| Rashee Rice | WR · KC | OUT | — | Ruled out Friday (tweet above) |
| David Njoku | TE · CLE | OUT | — | Inactive |
| Keon Coleman | WR · BUF | OUT | Healthy scratch | Coach's decision; Gabe Davis also out |
| Woody Marks | RB · HOU | OUT | — | Ruled out; 4:25 window |
| Justin Fields | QB · NYJ | OUT | — | Inactive; downgrades the whole Jets offense |
| Dalton Kincaid | TE · BUF | IN | Knee | Full participant Friday |
| Javonte Williams | RB · DAL | IN | Stinger/neck | Expected to play; no snap-count reporting |
| Tua Tagovailoa | QB · MIA | OUT | — | Emergency third QB only |
| Sterling Shepard | WR · TB | OUT | — | Inactive |
| Noah Fant | TE · CIN | OUT | — | Inactive |
| Dylan Sampson | RB · CLE | OUT | — | Inactive |
| Mason Taylor | TE · NYJ | OUT | — | Inactive |
| Matt Prater | K · BUF | OUT | — | Replacement kicker in 14 mph wind |
| Drake London | WR · ATL | EXP IN | PCL sprain | Beat reports say plays, no cap — locks at ~2:35 ET actives |
| Marvin Harrison Jr. | WR · ARI | EXP IN | — | Expected back per reporting — locks at ~2:35 ET actives |
| JAX@DEN · LV@HOU · PIT@DET |  | PENDING | — | Remaining GTDs minor; actives ~2:55 ET |
| SF@IND | MNF | PENDING | — | Statuses Monday — watch Pearsall, Guerendo, Giddens; posted to the Discord |
