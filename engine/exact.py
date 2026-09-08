"""
Safari Time - exact base game mathematics.

The base game does not need Monte Carlo. Two observations make it solvable in
closed form:

1. Expanding wilds are a COLUMN property. For a given reel and stop, either the
   3-symbol window contains a Wild - in which case every row of that column
   reads Wild - or it does not, and each row reads its own symbol. So for each
   (reel, row) we can tabulate the exact distribution of the "effective" symbol
   over all 100 stops.

2. A payline touches exactly ONE row per reel, and the five reels stop
   independently. So the joint distribution along a payline is just the product
   of five (reel, row) marginals.

That leaves the chain evaluation, which we solve with a dynamic program over
the five positions. The key trick: the set of symbols still able to extend the
chain is always either "every paying symbol" (while we have seen nothing but
Wilds) or a single symbol. Two kinds of state, not 2^9.

Only the stateful Free Games feature needs simulating - see engine/simulate.py.
"""

from __future__ import annotations

from functools import lru_cache

from . import config as cfg

ALL = "ALL"      # every paying symbol still alive (nothing but Wilds so far)
DEAD = "DEAD"    # chain broken, nothing can extend

# When a run of Wilds is finally broken by a real symbol X at position n, every
# OTHER symbol dies right there with a chain of exactly n. This table gives the
# best of those fallback awards: {X: {n: (award, symbol_that_earns_it)}}.
BEST_OTHER = {}
for _x in cfg.PAY_SYMBOLS:
    BEST_OTHER[_x] = {}
    for _n in range(0, 6):
        best = (0, None)
        for _s in cfg.PAY_SYMBOLS:
            if _s != _x and cfg.line_pay(_s, _n) > best[0]:
                best = (cfg.line_pay(_s, _n), _s)
        BEST_OTHER[_x][_n] = best

# Best award from ANY symbol at chain length n (a pure-Wild run pays this).
BEST_ANY = {}
for _n in range(0, 6):
    best = (0, None)
    for _s in cfg.PAY_SYMBOLS:
        if cfg.line_pay(_s, _n) > best[0]:
            best = (cfg.line_pay(_s, _n), _s)
    BEST_ANY[_n] = best


# ---------------------------------------------------------------------------
# Per (reel, row) effective-symbol distributions
# ---------------------------------------------------------------------------

def effective_distributions(strips: list, expanding: bool = True) -> list:
    """
    dists[reel][row] -> {symbol: probability}

    The "effective" symbol is what the payline evaluator actually sees, i.e.
    after expanding wilds have been applied.
    """
    dists = []
    for strip in strips:
        per_row = [dict() for _ in range(cfg.ROWS)]
        for stop in range(cfg.STOPS):
            win = [strip[(stop + r) % cfg.STOPS] for r in range(cfg.ROWS)]
            has_wild = expanding and cfg.WILD in win
            for row in range(cfg.ROWS):
                sym = cfg.WILD if has_wild else win[row]
                per_row[row][sym] = per_row[row].get(sym, 0) + 1
        for row in range(cfg.ROWS):
            per_row[row] = {s: n / cfg.STOPS for s, n in per_row[row].items()}
        dists.append(per_row)
    return dists


def scatter_distribution(strips: list) -> dict:
    """
    Exact distribution of the number of Africa symbols on the board.

    Scatters are counted on the raw grid and at most one can be visible per
    reel, so this is a Poisson-binomial over five independent reels.
    """
    per_reel = []
    for strip in strips:
        hits = sum(
            1 for stop in range(cfg.STOPS)
            if cfg.AFRICA in [strip[(stop + r) % cfg.STOPS] for r in range(cfg.ROWS)]
        )
        per_reel.append(hits / cfg.STOPS)

    dist = {0: 1.0}
    for p in per_reel:
        nxt = {}
        for count, prob in dist.items():
            nxt[count] = nxt.get(count, 0.0) + prob * (1 - p)
            nxt[count + 1] = nxt.get(count + 1, 0.0) + prob * p
        dist = nxt
    return dist


# ---------------------------------------------------------------------------
# Exact expected line award
# ---------------------------------------------------------------------------

def _line_expectation(cell_dists: tuple) -> dict:
    """
    Exact expected award for one payline, in line bets, broken down by the
    (symbol, chain length) combination that actually paid.

    `cell_dists` is five hashable ((symbol, prob), ...) tuples in SCAN order.
    Returns {(symbol, chain): expected_award}.
    """

    def better(a: tuple, b: tuple) -> tuple:
        return a if a[0] >= b[0] else b

    @lru_cache(maxsize=None)
    def walk(k: int, alive, best: tuple) -> dict:
        # `best` = (award, symbol, chain) of the best already-dead candidate.
        if alive is DEAD or k == cfg.REELS:
            if alive is ALL:
                award, sym = BEST_ANY[cfg.REELS]
                final = (award, sym, cfg.REELS)
            elif alive is DEAD:
                final = (0, None, 0)
            else:
                final = (cfg.line_pay(alive, cfg.REELS), alive, cfg.REELS)
            award, sym, chain = better(best, final)
            return {(sym, chain): float(award)} if award > 0 else {}

        out = {}
        for sym, prob in cell_dists[k]:
            if alive is ALL:
                if sym == cfg.WILD:
                    nxt_alive, nxt_best = ALL, best
                elif sym == cfg.AFRICA:
                    award, s = BEST_ANY[k]
                    nxt_alive, nxt_best = DEAD, better(best, (award, s, k))
                else:
                    award, s = BEST_OTHER[sym][k]
                    nxt_alive, nxt_best = sym, better(best, (award, s, k))
            elif sym == cfg.WILD or sym == alive:
                nxt_alive, nxt_best = alive, best
            else:
                nxt_alive = DEAD
                nxt_best = better(best, (cfg.line_pay(alive, k), alive, k))

            for combo, value in walk(k + 1, nxt_alive, nxt_best).items():
                out[combo] = out.get(combo, 0.0) + prob * value
        return out

    result = walk(0, ALL, (0, None, 0))
    walk.cache_clear()
    return result


def base_line_math(strips: list = None) -> dict:
    """
    Exact expected base game line award per play.

    Returns the total in line bets, the total as a fraction of the total bet
    (= RTP contribution), and a per-combination breakdown.
    """
    strips = strips or cfg.BASE_STRIPS
    dists = effective_distributions(strips, expanding=True)

    if cfg.PAY_DIRECTION == "both":
        raise NotImplementedError(
            'PAY_DIRECTION "both" is not exactly solvable by this DP - the two '
            "readings share cells. Use the Monte Carlo simulator for that setup."
        )
    order = (list(range(cfg.REELS)) if cfg.PAY_DIRECTION == "left"
             else list(reversed(range(cfg.REELS))))

    combos = {}
    total = 0.0
    for payline in cfg.PAYLINES:
        cell_dists = tuple(
            tuple(sorted(dists[payline[i][0]][payline[i][1]].items()))
            for i in order
        )
        for combo, value in _line_expectation(cell_dists).items():
            combos[combo] = combos.get(combo, 0.0) + value
            total += value

    return {
        "expected_line_bets": total,
        "rtp": total / cfg.LINES,     # total bet = LINES x line bet
        "combos": combos,
    }


def scatter_math(strips: list = None) -> dict:
    """Exact scatter trigger probabilities and scatter RTP contribution."""
    strips = strips or cfg.BASE_STRIPS
    dist = scatter_distribution(strips)

    trigger = sum(p for n, p in dist.items() if n >= 3)
    rtp = sum(p * cfg.SCATTER_PAY[min(n, 5)] for n, p in dist.items() if n >= 3)

    return {
        "distribution": dist,
        "trigger_probability": trigger,
        "trigger_one_in": (1 / trigger) if trigger else float("inf"),
        "rtp": rtp,
    }
