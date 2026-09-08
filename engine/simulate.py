"""
Safari Time - Monte Carlo simulation.

Two jobs:

1. `feature_ev`   - the Free Games feature has sticky wilds, so its state
                    changes every spin and there is no closed form. We play it
                    out a million times and average.

2. `full_game`    - plays whole rounds (base + feature, with the $800 cap) to
                    validate the exact solver, and to measure things the exact
                    maths does not give directly: hit frequency, volatility,
                    win distribution, and how often the cap bites.

The inner loops are written for speed rather than beauty: precomputed windows,
locals bound once, no dataclasses. They are cross-checked against engine/game.py
by tests/test_engine.py, so any divergence is caught.
"""

from __future__ import annotations

import math
import random
import statistics
import sys
import time

from . import config as cfg
from . import exact
from .game import play

_WILD = cfg.WILD
_AFRICA = cfg.AFRICA
_ROWS = cfg.ROWS
_REELS = cfg.REELS
_STOPS = cfg.STOPS


def _precompute(strips: list) -> list:
    """windows[reel][stop] -> (tuple_of_3_symbols, has_wild)"""
    out = []
    for strip in strips:
        per_stop = []
        for stop in range(_STOPS):
            win = tuple(strip[(stop + r) % _STOPS] for r in range(_ROWS))
            per_stop.append((win, _WILD in win))
        out.append(per_stop)
    return out


def _line_tables():
    """Flatten paylines into scan-ordered (reel, row) tuples plus pay tables."""
    if cfg.PAY_DIRECTION == "left":
        order = list(range(_REELS))
    else:
        order = list(reversed(range(_REELS)))
    lines = [tuple(line[i] for i in order) for line in cfg.PAYLINES]
    best_any = {n: exact.BEST_ANY[n][0] for n in range(6)}
    best_other = {s: {n: exact.BEST_OTHER[s][n][0] for n in range(6)} for s in cfg.PAY_SYMBOLS}
    pay = {s: {n: cfg.line_pay(s, n) for n in range(6)} for s in cfg.PAY_SYMBOLS}
    return lines, best_any, best_other, pay


def _score_grid(grid: list, lines, best_any, best_other, pay) -> int:
    """
    Total line award in LINE BETS for a post-transform grid.

    Per line: count leading Wilds (w). If the first real cell is a paying
    symbol X, its chain is w+1+continuation; every other symbol dies at w. Max
    of those two is provably the same as the max over all nine symbols.
    """
    total = 0
    for line in lines:
        w = 0
        first = None
        first_idx = 0
        for idx, (reel, row) in enumerate(line):
            c = grid[reel][row]
            if c == _WILD:
                w += 1
            else:
                first, first_idx = c, idx
                break
        if first is None:
            total += best_any[5]
            continue
        if first == _AFRICA:
            total += best_any[w]
            continue
        chain = w + 1
        for reel, row in line[first_idx + 1:]:
            c = grid[reel][row]
            if c == first or c == _WILD:
                chain += 1
            else:
                break
        a = pay[first][chain]
        b = best_other[first][w]
        total += a if a > b else b
    return total


def feature_ev(spins: int, features: int = 200_000, seed: int = 1) -> dict:
    """
    Average total award of a Free Games feature of `spins` spins, in LINE BETS.

    Sticky wilds: a Wild on the middle three reels expands its column and that
    column stays wild for the remaining spins.
    """
    if cfg.PAY_DIRECTION == "both":
        raise NotImplementedError("use full_game for PAY_DIRECTION both")

    rng = random.Random(seed)
    rand = rng.randrange
    windows = _precompute(cfg.FEATURE_STRIPS)
    lines, best_any, best_other, pay = _line_tables()
    wild_col = (_WILD,) * _ROWS
    feature_reels = cfg.FEATURE_WILD_REELS
    column_mode = cfg.STICKY_MODE == "column"

    totals = []
    sticky_counts = []
    for _ in range(features):
        sticky = set()
        feature_total = 0
        for _ in range(spins):
            grid = []
            for reel in range(_REELS):
                win, has_wild = windows[reel][rand(_STOPS)]
                if has_wild and reel in feature_reels:
                    if column_mode:
                        sticky.add(reel)
                    else:
                        for row in range(_ROWS):
                            if win[row] == _WILD:
                                sticky.add((reel, row))
                grid.append(wild_col if has_wild else win)
            if sticky:
                if column_mode:
                    grid = [wild_col if r in sticky else grid[r] for r in range(_REELS)]
                else:
                    grid = [list(col) for col in grid]
                    for reel, row in sticky:
                        grid[reel][row] = _WILD
            feature_total += _score_grid(grid, lines, best_any, best_other, pay)
        totals.append(feature_total)
        sticky_counts.append(len(sticky))

    mean = statistics.fmean(totals)
    sd = statistics.pstdev(totals)
    return {
        "spins": spins,
        "features": features,
        "mean_line_bets": mean,
        "mean_total_bets": mean / cfg.LINES,
        "sd_line_bets": sd,
        "stderr_line_bets": sd / math.sqrt(features),
        "max_line_bets": max(totals),
        "mean_sticky": statistics.fmean(sticky_counts),
        "zero_rate": sum(1 for t in totals if t == 0) / features,
    }


def total_rtp(feature_results: dict = None, features: int = 200_000, seed: int = 1) -> dict:
    """
    Combine exact base maths with simulated feature EVs:

        RTP = base_line + scatter + sum_n P(n scatters) * E[feature_n] / bet
    """
    base = exact.base_line_math()
    scat = exact.scatter_math()
    if feature_results is None:
        feature_results = {
            spins: feature_ev(spins, features, seed + spins)
            for spins in sorted(set(cfg.FREE_SPINS_AWARD.values()))
        }

    feature_rtp = 0.0
    for n, p in scat["distribution"].items():
        if n >= 3:
            spins = cfg.FREE_SPINS_AWARD[min(n, 5)]
            feature_rtp += p * feature_results[spins]["mean_total_bets"]

    return {
        "base_line_rtp": base["rtp"],
        "scatter_rtp": scat["rtp"],
        "feature_rtp": feature_rtp,
        "total_rtp": base["rtp"] + scat["rtp"] + feature_rtp,
        "trigger_one_in": scat["trigger_one_in"],
        "features": feature_results,
        "base": base,
        "scatter": scat,
    }


def full_game(plays: int, total_bet: int = cfg.MIN_BET_CENTS, seed: int = 7) -> dict:
    """
    Play complete rounds through the real engine (engine/game.py), with the
    $800 cap applied. Slower than the tuned loops above but it is the actual
    production path, which is the point.
    """
    rng = random.Random(seed)
    wagered = 0
    won = 0
    hits = 0
    triggers = 0
    capped = 0
    biggest = 0
    wins = []
    t0 = time.time()
    for i in range(plays):
        result = play(rng, total_bet, keep_spins=False)
        wagered += total_bet
        won += result.cents
        wins.append(result.cents)
        if result.cents > 0:
            hits += 1
        if result.triggered:
            triggers += 1
        if result.capped:
            capped += 1
        if result.cents > biggest:
            biggest = result.cents
        if (i + 1) % 100_000 == 0:
            print(f"  {i + 1:,} plays  rtp so far {won / wagered:.4f}  "
                  f"({time.time() - t0:.0f}s)", file=sys.stderr)

    mean = won / plays
    var = statistics.pvariance(wins, mu=mean)
    return {
        "plays": plays,
        "total_bet_cents": total_bet,
        "rtp": won / wagered,
        "hit_frequency": hits / plays,
        "trigger_one_in": (plays / triggers) if triggers else float("inf"),
        "capped_plays": capped,
        "biggest_win_cents": biggest,
        "volatility_index": math.sqrt(var) / total_bet,   # SD in units of bet
        "stderr_rtp": math.sqrt(var / plays) / total_bet,
    }


def _fmt_money(cents: int) -> str:
    return f"${cents / 100:,.2f}"


def main(argv: list) -> None:
    import argparse

    ap = argparse.ArgumentParser(description="Safari Time Monte Carlo")
    ap.add_argument("--features", type=int, default=200_000,
                    help="features to simulate per free-spin count")
    ap.add_argument("--plays", type=int, default=0,
                    help="full-game plays to run through engine/game.py")
    ap.add_argument("--bet", type=int, default=cfg.MIN_BET_CENTS,
                    help="total bet in cents for --plays")
    ap.add_argument("--seed", type=int, default=1)
    args = ap.parse_args(argv)

    print(f"Safari Time  |  {cfg.LINES} lines  |  pay {cfg.PAY_DIRECTION}-anchored  "
          f"|  sticky mode {cfg.STICKY_MODE}")
    print("=" * 66)

    t0 = time.time()
    r = total_rtp(features=args.features, seed=args.seed)
    print(f"Base line RTP (exact)      {r['base_line_rtp']:.4%}")
    print(f"Scatter RTP (exact)        {r['scatter_rtp']:.4%}")
    print(f"Feature RTP (simulated)    {r['feature_rtp']:.4%}")
    print(f"TOTAL RTP                  {r['total_rtp']:.4%}")
    print(f"Bonus trigger              1 in {r['trigger_one_in']:.1f} spins")
    print()
    print(f"Free Games EV ({args.features:,} features each, {time.time() - t0:.0f}s):")
    for spins, fe in sorted(r["features"].items()):
        print(f"  {spins:2d} spins  mean {fe['mean_total_bets']:7.2f}x bet  "
              f"(+/-{fe['stderr_line_bets'] / cfg.LINES:.3f})  "
              f"sd {fe['sd_line_bets'] / cfg.LINES:6.2f}x  "
              f"max {fe['max_line_bets'] / cfg.LINES:7.1f}x  "
              f"avg sticky reels {fe['mean_sticky']:.2f}  "
              f"dead {fe['zero_rate']:.1%}")

    if args.plays:
        print()
        print(f"Full-game validation: {args.plays:,} plays at {_fmt_money(args.bet)} "
              f"(cap {_fmt_money(cfg.MAX_PAYOUT_CENTS)})")
        g = full_game(args.plays, args.bet, args.seed)
        print(f"  RTP                {g['rtp']:.4%}  (+/-{g['stderr_rtp']:.4%})")
        print(f"  Hit frequency      {g['hit_frequency']:.2%} of plays")
        print(f"  Bonus trigger      1 in {g['trigger_one_in']:.1f}")
        print(f"  Volatility index   {g['volatility_index']:.2f}")
        print(f"  Biggest win        {_fmt_money(g['biggest_win_cents'])}")
        print(f"  Plays hitting cap  {g['capped_plays']}")


if __name__ == "__main__":
    main(sys.argv[1:])
