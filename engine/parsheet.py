"""
Safari Time - par sheet generator.

Writes the Markdown par sheet into the docs folder: strips, paytable, exact
per-combination contributions, scatter odds and the solved RTP.

    python -m engine.parsheet                     # 200k features per count
    python -m engine.parsheet --features 1000000  # the publishable run
"""

from __future__ import annotations

import argparse
import glob
import os
import sys
from datetime import date

from . import config as cfg
from . import exact, simulate

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def docs_dir() -> str:
    hits = sorted(glob.glob(os.path.join(ROOT, "SafariTime_Docs_v*")))
    if not hits:
        raise SystemExit("no SafariTime_Docs_v* folder found")
    return os.path.join(hits[-1], "02_Math_Model")


def strip_table(strips: list) -> str:
    lines = ["| Stop | R1 | R2 | R3 | R4 | R5 |", "| ---: | :-: | :-: | :-: | :-: | :-: |"]
    short = {cfg.WILD: "**W**", cfg.AFRICA: "**AF**", cfg.GIRAFFE: "Gi", cfg.ZEBRA: "Ze",
             cfg.RHINO: "Rh", cfg.ELEPHANT: "El", cfg.LION: "Li"}
    for s in range(cfg.STOPS):
        cells = [short.get(strips[r][s], cfg.SYMBOL_NAMES[strips[r][s]]) for r in range(cfg.REELS)]
        lines.append(f"| {s} | " + " | ".join(cells) + " |")
    return "\n".join(lines)


def counts_table(counts: dict) -> str:
    lines = ["| ID | Symbol | R1 | R2 | R3 | R4 | R5 |", "| --: | --- | --: | --: | --: | --: | --: |"]
    for sym, row in counts.items():
        lines.append(f"| {sym} | {cfg.SYMBOL_NAMES[sym]} | " + " | ".join(str(n) for n in row) + " |")
    return "\n".join(lines)


def main(argv: list) -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--features", type=int, default=200_000)
    ap.add_argument("--seed", type=int, default=1)
    args = ap.parse_args(argv)

    r = simulate.total_rtp(features=args.features, seed=args.seed)
    base, scat = r["base"], r["scatter"]

    out = []
    w = out.append
    w(f"# Safari Time - Par Sheet\n")
    w(f"Generated {date.today().isoformat()} by `python -m engine.parsheet --features {args.features}`. "
      f"Every figure below is derived from `engine/config.py`; edit that file and regenerate rather than editing this one.\n")

    w("## Summary\n")
    w("| Metric | Value |\n| --- | ---: |")
    w(f"| **Total RTP** | **{r['total_rtp']:.4%}** |")
    w(f"| Base game line RTP (exact) | {r['base_line_rtp']:.4%} |")
    w(f"| Scatter RTP (exact) | {r['scatter_rtp']:.4%} |")
    w(f"| Free Games RTP (Monte Carlo) | {r['feature_rtp']:.4%} |")
    w(f"| Free Games share of RTP | {r['feature_rtp'] / r['total_rtp']:.1%} |")
    w(f"| Bonus trigger | 1 in {r['trigger_one_in']:.1f} spins |")
    w(f"| Lines | {cfg.LINES} fixed |")
    w(f"| Pay direction | {cfg.PAY_DIRECTION} (anchored on reel {'5' if cfg.PAY_DIRECTION == 'right' else '1'}) |")
    w(f"| Bets | {', '.join(f'${b / 100:.2f}' for b in cfg.BET_LEVELS_CENTS)} |")
    w(f"| Max payout per play | ${cfg.MAX_PAYOUT_CENTS / 100:,.2f} (Montana VGM cap) |")
    w(f"| Virtual stops | {cfg.STOPS} per reel = {cfg.STOPS ** cfg.REELS:,} combinations |")
    w(f"| Sticky wild mode | {cfg.STICKY_MODE} |")
    w(f"| Retrigger | {'yes' if cfg.RETRIGGER else 'no'} |\n")

    w("## Paytable (multiples of line bet)\n")
    w("| Symbol | 3 | 4 | 5 |\n| --- | --: | --: | --: |")
    for sym in reversed(cfg.PAY_SYMBOLS):
        a, b, c = cfg.PAYTABLE[sym]
        w(f"| {cfg.SYMBOL_NAMES[sym]} | {a} | {b} | {c} |")
    w("| Wild | substitutes for all but Africa; expands the reel | | |")
    w("| Africa (scatter) | 10 free games | 15 free games | 20 free games |\n")
    top = max(cfg.PAYTABLE[s][2] for s in cfg.PAY_SYMBOLS)
    w(f"Top line award: {top}x line bet = {top / cfg.LINES:.0f}x total bet "
      f"(${top / cfg.LINES * cfg.MAX_BET_CENTS / 100:,.2f} at max bet).\n")

    w("## Scatter (Africa) odds\n")
    w("Exactly one Africa can be visible per reel; the count is Poisson-binomial over five reels.\n")
    w("| Africa on screen | Probability | 1 in | Award |\n| --: | --: | --: | --- |")
    for n, p in sorted(scat["distribution"].items()):
        award = f"{cfg.FREE_SPINS_AWARD[min(n, 5)]} free games" if n >= 3 else "-"
        w(f"| {n} | {p:.6f} | {1 / p:,.1f} | {award} |")
    w("")

    w("## Free Games (Monte Carlo)\n")
    w(f"{args.features:,} features simulated per spin count. Awards in multiples of total bet.\n")
    w("| Free games | Mean | Std dev | Max seen | Avg reels locked | Zero-win features |\n| --: | --: | --: | --: | --: | --: |")
    for spins, fe in sorted(r["features"].items()):
        w(f"| {spins} | {fe['mean_total_bets']:.2f}x | {fe['sd_line_bets'] / cfg.LINES:.2f}x | "
          f"{fe['max_line_bets'] / cfg.LINES:.0f}x | {fe['mean_sticky']:.2f} | {fe['zero_rate']:.1%} |")
    w("")

    w("## Base game contribution by combination (exact)\n")
    w("Fraction of total bet returned by each winning combination, summed over all 10 lines.\n")
    w("| Symbol | 3 | 4 | 5 | Total |\n| --- | --: | --: | --: | --: |")
    combos = base["combos"]
    for sym in reversed(cfg.PAY_SYMBOLS):
        vals = [combos.get((sym, n), 0.0) / cfg.LINES for n in (3, 4, 5)]
        w(f"| {cfg.SYMBOL_NAMES[sym]} | " + " | ".join(f"{v:.4%}" for v in vals) + f" | {sum(vals):.4%} |")
    w(f"| **All** | | | | **{base['rtp']:.4%}** |\n")

    w("## Symbol counts per 100-stop strip\n")
    w("### Base game\n")
    w(counts_table(cfg.BASE_COUNTS) + "\n")
    w("### Free Games (no Wild on reels 1 and 5)\n")
    w(counts_table(cfg.FEATURE_COUNTS) + "\n")

    w("## Paylines\n")
    w("Rows: 0 = top, 1 = middle, 2 = bottom. Each entry is the row used on reels 1-5.\n")
    w("| Line | R1 | R2 | R3 | R4 | R5 |\n| --: | :-: | :-: | :-: | :-: | :-: |")
    for i, line in enumerate(cfg.PAYLINES):
        w(f"| {i + 1} | " + " | ".join(str(row) for _, row in line) + " |")
    w("")

    w("## Base game reel strips\n")
    w(strip_table(cfg.BASE_STRIPS) + "\n")
    w("## Free Games reel strips\n")
    w(strip_table(cfg.FEATURE_STRIPS) + "\n")

    path = os.path.join(docs_dir(), "Par_Sheet.md")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out))
    print(f"wrote {path}")
    print(f"TOTAL RTP {r['total_rtp']:.4%}")


if __name__ == "__main__":
    main(sys.argv[1:])
