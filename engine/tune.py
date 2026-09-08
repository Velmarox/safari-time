"""
Safari Time - RTP tuner.

Every line award is a multiple of the line bet, so the line and feature parts
of RTP are LINEAR in the paytable: double every entry and they double. The
scatter prize is a fixed multiple of the total bet and does not move, so it is
held out of the scaling:

    scale = (target_rtp - scatter_rtp) / (current_rtp - scatter_rtp)

The scaled paytable is then rounded to "nice" numbers that read well on a pay
screen, and re-solved so you see exactly what the rounding cost you.

Usage:
    python -m engine.tune                 # target 92%
    python -m engine.tune --target 0.90
    python -m engine.tune --features 500000

NOTE: since v0.4.0 the paytable is fixed to the reference game and RTP is
solved by weighting the reels instead (see Math_Spec.md section 6). Use this
only for what-if questions.

It prints a PAYTABLE block to paste into engine/config.py - it does not edit
the file for you. Re-run engine/simulate.py after pasting to confirm.
"""

from __future__ import annotations

import argparse
import sys

from . import config as cfg
from . import simulate


def nice(value: float) -> int:
    """Round to a figure that looks deliberate on a pay screen."""
    if value < 10:
        return max(1, round(value))
    if value < 50:
        return int(round(value / 5.0) * 5)
    if value < 200:
        return int(round(value / 10.0) * 10)
    return int(round(value / 25.0) * 25)


def scaled_paytable(scale: float) -> dict:
    out = {}
    for sym, (a, b, c) in cfg.PAYTABLE.items():
        out[sym] = (nice(a * scale), nice(b * scale), nice(c * scale))
    return out


def rtp_with_paytable(paytable: dict, features: int, seed: int) -> float:
    """
    Temporarily swap the paytable in, re-solve, swap back.

    exact.py caches BEST_ANY/BEST_OTHER at import, so those are rebuilt too.
    """
    from . import exact
    from importlib import reload

    original = cfg.PAYTABLE
    cfg.PAYTABLE = paytable
    cfg.BEST_PAY = {n: max(cfg.line_pay(s, n) for s in cfg.PAY_SYMBOLS) for n in range(0, 6)}
    try:
        reload(exact)
        reload(simulate)
        return simulate.total_rtp(features=features, seed=seed)["total_rtp"]
    finally:
        cfg.PAYTABLE = original
        cfg.BEST_PAY = {n: max(cfg.line_pay(s, n) for s in cfg.PAY_SYMBOLS) for n in range(0, 6)}
        reload(exact)
        reload(simulate)


def main(argv: list) -> None:
    ap = argparse.ArgumentParser(description="Solve the paytable for a target RTP")
    ap.add_argument("--target", type=float, default=0.92)
    ap.add_argument("--features", type=int, default=100_000)
    ap.add_argument("--seed", type=int, default=1)
    args = ap.parse_args(argv)

    r = simulate.total_rtp(features=args.features, seed=args.seed)
    current, scatter = r["total_rtp"], r["scatter_rtp"]
    scale = (args.target - scatter) / (current - scatter)
    print(f"Current RTP {current:.4%} (of which scatter prize {scatter:.4%})  ->  "
          f"target {args.target:.2%}  ->  line paytable scale x{scale:.4f}")

    proposal = scaled_paytable(scale)
    achieved = rtp_with_paytable(proposal, args.features, args.seed)
    print(f"Rounded paytable achieves {achieved:.4%}")
    print()
    print("PAYTABLE = {")
    print("    #            3    4     5")
    for sym in cfg.PAY_SYMBOLS:
        a, b, c = proposal[sym]
        name = cfg.SYMBOL_NAMES[sym].upper().rstrip("S") if sym > cfg.A else cfg.SYMBOL_NAMES[sym]
        print(f"    {name + ':':<10}({a:>3d}, {b:>3d}, {c:>4d}),")
    print("}")


if __name__ == "__main__":
    main(sys.argv[1:])
