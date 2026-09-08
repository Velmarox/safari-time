# Safari Time - Game Overview

**Format:** 5 reels x 3 rows, 10 fixed paylines, video slot.
**Market:** Montana VGM route. Max bet $2.00, max payout $800 per play.
**Theme:** African savanna - card royals (J Q K A), Giraffes, Zebras, Rhinos, Elephants, Lions, a WILD and an AFRICA bonus medallion.
**Target RTP:** 92%. Solved at **91.97%** (see `02_Math_Model/Par_Sheet.md`).

## Wagering

| Bet | Per line |
| --- | --- |
| $0.50 | 5c |
| $1.00 | 10c |
| $1.50 | 15c |
| $2.00 | 20c |

All 10 lines are always in play. Bets step in 50c increments; the $2.00 ceiling is the Montana statutory limit.

## Base game

1. RNG picks one of 100 virtual stops per reel (10 billion combinations).
2. The reel shows that stop and the two below it.
3. **Expanding WILD:** WILD lands only on reels 2, 3 and 4 - never on the first or last reel. If a WILD is visible anywhere on a reel, the whole reel becomes WILD before pays are evaluated.
4. Each payline is read **left to right** from reel 1. Three or more matching symbols (WILD substitutes) pay from the paytable; only the best win per line is paid.
5. AFRICA symbols are counted anywhere on screen. 3 / 4 / 5 award 10 / 15 / 20 Free Games **plus a bonus prize of the total bet times the number of free games** (10x / 15x / 20x total bet), paid on the trigger. Only one AFRICA can be visible per reel, so 5 is the maximum. WILD does not substitute for AFRICA, and the strips are laid out so a WILD and an AFRICA can never show on the same reel.

## Free Games

- Played at the triggering bet. The feature strips are currently identical to the base strips (kept separate in `config.py` so they can diverge later).
- A WILD that lands (reels 2, 3 and 4 only, as always) expands its reel and that reel **stays WILD** for every remaining free game. Three locked reels means every line has at least three WILDs.
- AFRICA symbols still appear on the feature strips but award nothing - no retrigger (configurable; see `RETRIGGER` in `engine/config.py`).
- Feature wins accumulate into the same play total as the base spin and share the $800 cap.

## Presentation (web prototype)

- On PLAY every reel rolls. Reel 1 lands 0.8 s later and each following reel keeps rolling until **half a second after the previous landing**, so a full spin settles over about 2.8 s. While the reels roll the PLAY button reads **STOP**; pressing it snaps every reel still rolling onto its result at once. Timings are constants at the top of the spin code (`FIRST_LAND_MS`, `LAND_INTERVAL_MS`, `LAND_MS`).
- Expanding wilds flash and grow into the column after the reel stops.
- AFRICA is a blue/silver medallion so it stands apart from the gold symbol set. Each AFRICA that lands plays a brass hit pitched a whole step higher than the previous one in that spin (G, A, B, C#, D#) - but only while the bonus is still reachable: with no AFRICA on reels 1-3, an AFRICA on reel 4 or 5 lands silently.
- Winning lines cycle with the payline drawn over the reels and the winning segment highlighted; the message bar names the line, symbol, count and award.
- Bonus trigger: scatters pulse, the bonus prize is added to the win meter, then a "BONUS TRIGGERED - N FREE GAMES" card showing the prize. Locked reels carry a gold glow during the feature. A summary card closes the feature.
- Wins of 25x bet or more get a BIG WIN card.
- Credits are demo credits stored in the browser. A footer link adds $20.
- Sound: looping music (base game / Free Games), spin start and a whir per reel roll, a click per reel stop, the rising Africa brass hit described above, a WILD sting on expansion or lock, small/medium win jingles, the animal call of a winning symbol (Lion, Elephant, Giraffe, Rhino), a bonus fanfare, and a lion roar on BIG WIN. Mute toggle in the top bar, remembered per browser. Nothing plays until the first tap (browser autoplay rules).

## Open design decisions

These are set in `engine/config.py` and the maths re-solves in seconds if changed:

| Decision | Current | Note |
| --- | --- | --- |
| `PAY_DIRECTION` | `left` | Confirmed left-to-right (v0.1.1). The strips mirror reel 1/5 and 2/4, so `right` solves to the same RTP; `both` would not and needs re-tuning. |
| `WILD_REELS` | `(1, 2, 3)` | Confirmed (v0.2.0): WILD never appears on reels 1 or 5, base game included. Removing the outer-reel wilds cut the base game from 75% to 61%; the paytable was rescaled x1.17 to bring the total back to 92%. |
| `STICKY_MODE` | `column` | A feature WILD locks the whole reel. `cell` locks only the landing square (much lower feature EV). |
| `RETRIGGER` | `False` | Scatters in Free Games do nothing. Confirmed by the IGT reference ("the bonus cannot be retriggered"). |
| `SCATTER_PAY` | `= FREE_SPINS_AWARD` | Confirmed (v0.3.0): the trigger pays total bet x free games awarded, per the IGT reference. Worth 6.5 points of RTP. |
| `FEATURE_COUNTS` | same as base | The reference game states its bonus reels have a different symbol composition. Ours are identical; no data to weight them from. |
| Cabinet limits | $2.00 / 20c line | Montana: max total bet $2.00, max line bet 20c. The reference game's $4.00 / 40c is a different jurisdiction and is deliberately not adopted. |
