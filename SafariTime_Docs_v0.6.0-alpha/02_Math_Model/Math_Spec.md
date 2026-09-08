# Safari Time - Mathematical Model

How the numbers in `Par_Sheet.md` are produced, and why each part is computed the way it is. Code references are to `engine/`.

## 1. Virtual reels (`config.py`)

Each reel is an array of 100 integer symbol IDs. Symbol counts per reel are set in `BASE_COUNTS`; the strip order is generated deterministically by `build_strip`, which places at each position whichever symbol is furthest behind its fair share. This spreads rare symbols evenly, and with three AFRICA per 100 stops (roughly 33 apart) it guarantees at most one AFRICA in any 3-symbol window. A second pass (`_keep_wild_clear_of_scatter`) moves each WILD, if needed, so it is never within two stops of an AFRICA - the two can therefore never be visible on the same reel, which is what makes "WILD does not substitute for AFRICA" unambiguous on screen. Both guarantees are asserted at import and covered by tests.

Total combinations: 100^5 = 10,000,000,000.

Per-reel window probabilities:

- Base game: P(WILD visible) = 0.09 on each of reels 2 / 3 / 4 (3 Wild stops, each visible from 3 stops); reels 1 and 5 carry no WILD (`WILD_REELS`)
- Free Games (`FEATURE_COUNTS`): P(WILD visible) = 0.03 / 0.06 / 0.03 on reels 2 / 3 / 4
- P(AFRICA visible on a reel) = 9 / 100 = 0.09 on every reel, both strip sets

The feature strips are leaner in Wilds because a feature Wild locks its reel for the rest of the feature (section 4), and carry slightly more Lion / Elephant / Rhino stops to make up the return.

## 2. Scatter combinatorics (`exact.scatter_distribution`)

With at most one AFRICA per reel the on-screen count is a Poisson-binomial over five independent reels with p = 0.09 each:

    P(3+) = 10 p^3 (1-p)^2 + 5 p^4 (1-p) + p^5 = 0.006341  ->  1 in 157.7

The brief asked for roughly 1 in 150. The brief's example weighting (2 AFRICA per reel, p = 0.06) would give about 1 in 500; three per reel is what lands it near 150.

## 3. Base game - exact, not simulated (`exact.base_line_math`)

Two facts make the base game solvable in closed form despite expanding wilds:

**Wild expansion is a column property.** For any reel and stop, either the window contains a WILD (and every row of that column reads WILD) or it does not (and each row reads its own symbol). So for each (reel, row) we tabulate the exact distribution of the *effective* symbol over all 100 stops.

**A payline touches one row per reel.** Reels stop independently, so the joint distribution of the five effective symbols along a line is the product of five (reel, row) marginals.

The chain evaluation is then a dynamic program over the five positions in scan order. The state is the set of symbols that could still extend the chain, which is always either *every paying symbol* (nothing but WILDs seen so far) or *one symbol*. When a WILD run of length n is broken by symbol X, every other symbol dies with a chain of exactly n, so the fallback award `BEST_OTHER[X][n]` is folded in at that point. The final award is the max of the surviving chain and the best fallback, which is exactly what the game engine's "try every symbol, take the best" evaluator computes - `tests/test_engine.py` checks the two agree on 20,000 random grids.

Output: expected award per line in line bets, broken down by (symbol, chain). Summed over 10 lines and divided by 10 (total bet = 10 line bets) it is the base line RTP.

## 4. Free Games - Monte Carlo (`simulate.feature_ev`)

Sticky wilds make the feature stateful: the distribution of spin k depends on which reels locked in spins 1..k-1. No closed form is attempted. The simulator plays the feature out with the feature strips:

1. Spin five stops.
2. Any WILD on reels 2-4 adds that reel to the locked set.
3. Overwrite locked reels with WILD, evaluate the 10 lines, accumulate.
4. Repeat for 10, 15 or 20 spins.

Run 1,000,000 times per spin count and averaged. Standard error is reported alongside the mean.

## 5. Total RTP

    RTP = base_line_RTP + scatter_RTP + sum over n>=3 of P(n AFRICA) x E[feature(n)] / total_bet

Scatter RTP is the bonus prize: P(n AFRICA) x SCATTER_PAY[n], with SCATTER_PAY = 10 / 15 / 20 total bets for n = 3 / 4 / 5 (the IGT reference game's "total bet multiplied by the number of fever games"). It is exact, and worth 6.50 points. The result is checked by `simulate.full_game`, which plays complete rounds through `game.py` (the production path, with the $800 cap) and reports RTP, hit frequency, volatility index and how often the cap bites.

## 6. Tuning - the reels, not the paytable

Since v0.4.0 the paytable is fixed (the reference game's table at $0.20 per line), so RTP is solved by weighting the reel strips in `config.py`. Findings with this paytable:

- **Expanding Wild density is the dominant lever and it compounds.** On the v0.4.0 symbol mix, 3 Wilds on each middle reel gives ~64% base line RTP, 4 gives ~88%, 5 gives ~117%. Two adjacent expanded reels turn every line into a 3+ chain, which is why the response is convex. But Wilds add hits as fast as they add return (v0.4.0's 3-4-3 ran at 1 in 3.5 plays), so they are not the lever for the last few points.
- **Low-to-high symbol swaps add return while removing hits.** A Lion chains far less often than a J, so moving stops from J/Q to Lion/Elephant/Rhino raises RTP and lowers hit frequency at the same time. v0.5.0 keeps Wilds at 3-3-3 and uses this to land ~71% base at ~1 in 4.2, near the reference's 1 in 4.01.
- **Outer-reel stops are the fine adjustment.** Every chain is anchored on reel 1, so one stop on reels 1 and 5 is worth: Zebra ~0.5 point, Elephant ~1, Rhino ~1.2 (measured while landing v0.5.0); the same change on a middle reel moves it less.
- **The feature has its own dial, and it does not touch hit frequency.** A triggered play already counts as a hit (the prize), so anything added inside the feature is pure return. Feature Wilds lock, so their density sets the share: 1-1-1 is worth ~9 points, 1-2-1 ~13.5, 2-2-2 ~25; the shipped 1-2-1 plus a few extra high symbols is ~14.4.
- The trigger prize (6.5 points) does not move with any of this; only the AFRICA count changes it.

`engine/tune.py` still exists and scales the paytable to a target - useful for what-if questions, but its output must not be pasted into `config.py` while the paytable is meant to match the reference. A reel-weighting sweep is a short script that swaps `BASE_COUNTS` / `FEATURE_COUNTS`, rebuilds the strips and calls `simulate.total_rtp` with 20-60k features per variant (a few seconds each).

## 7. The $800 cap

Applied once per play to base + feature. At $2.00 bet it is 400x. With the reference paytable (Lion x5 = 62.5x total bet) only a long feature with two or three locked reels gets near it: measured over 400,000 plays at $2.00 (v0.5.0 maths), the cap bit 9 times, and the full-game RTP was 91.55% (+/-0.89% one sigma) against the uncapped model's 92.13%. At $0.50 bet the cap is 1600x and never applies in practice.

## 8. Volatility

Full-game volatility index (standard deviation of a play's return in bets) is about 5.6, with a 23.8% hit frequency - 1 in 4.2 plays, matching the IGT reference's quoted 1 in 4.01 (v0.4.0 ran hotter, 1 in 3.5, before low-symbol stops were moved to high symbols). Base line wins carry about 77% of total RTP, the feature about 16%, and the fixed trigger prize the remaining 7%: frequent small wins, small top prize - the low-volatility shape the Montana cap pushes towards.
