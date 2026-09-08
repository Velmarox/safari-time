# Safari Time - Game Overview

**Format:** 5 reels x 3 rows, 10 fixed paylines, video slot.
**Market:** Montana VGM route. Max bet $2.00, max payout $800 per play.
**Theme:** African savanna - card royals (J Q K A), Giraffes, Zebras, Rhinos, Elephants, Lions, a WILD and an AFRICA bonus medallion.
**Target RTP:** 92%. Solved at **92.39%** (see `02_Math_Model/Par_Sheet.md`).

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
3. **Expanding WILD:** if a WILD is visible anywhere on a reel, the whole reel becomes WILD before pays are evaluated.
4. Each payline is read **left to right** from reel 1. Three or more matching symbols (WILD substitutes) pay from the paytable; only the best win per line is paid.
5. AFRICA symbols are counted anywhere on screen. 3 / 4 / 5 award 10 / 15 / 20 Free Games. Only one AFRICA can be visible per reel, so 5 is the maximum.

## Free Games

- Played at the triggering bet on a separate set of reel strips.
- WILDs exist **only on reels 2, 3 and 4**.
- A WILD that lands expands its reel and that reel **stays WILD** for every remaining free game. Three locked reels means every line has at least three WILDs.
- AFRICA symbols still appear on the feature strips but award nothing - no retrigger (configurable; see `RETRIGGER` in `engine/config.py`).
- Feature wins accumulate into the same play total as the base spin and share the $800 cap.

## Presentation (web prototype)

- Reels stop left to right with a short blur and a settle bounce.
- Expanding wilds flash and grow into the column after the reel stops.
- Winning lines cycle with the payline drawn over the reels and the winning segment highlighted; the message bar names the line, symbol, count and award.
- Bonus trigger: scatters pulse, then a "BONUS TRIGGERED - N FREE GAMES" card. Locked reels carry a gold glow during the feature. A summary card closes the feature.
- Wins of 25x bet or more get a BIG WIN card.
- Credits are demo credits stored in the browser. A footer link adds $20.

## Open design decisions

These are set in `engine/config.py` and the maths re-solves in seconds if changed:

| Decision | Current | Note |
| --- | --- | --- |
| `PAY_DIRECTION` | `left` | Confirmed left-to-right (v0.1.1). The strips mirror reel 1/5 and 2/4, so `right` solves to the same RTP; `both` would not and needs re-tuning. |
| `STICKY_MODE` | `column` | A feature WILD locks the whole reel. `cell` locks only the landing square (much lower feature EV). |
| `RETRIGGER` | `False` | Scatters in Free Games do nothing. |
| `SCATTER_PAY` | all 0 | AFRICA awards free games only, matching screenshot 2 (WIN $0.00 on trigger). |
