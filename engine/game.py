"""
Safari Time - spin engine.

Deterministic, side-effect free evaluation of a single play:

    stops -> raw 5x3 grid -> expanding wilds -> line + scatter awards

A "play" is one base spin plus, if triggered, the whole Free Games feature.
All awards are returned in CENTS and the regulatory ceiling is applied to the
play total, not to individual lines.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field

from . import config as cfg


# ---------------------------------------------------------------------------
# Grid construction
# ---------------------------------------------------------------------------

def window(strip: list, stop: int) -> list:
    """The 3 symbols visible on a reel when it lands on `stop`."""
    n = len(strip)
    return [strip[(stop + r) % n] for r in range(cfg.ROWS)]


def grid_from_stops(strips: list, stops: list) -> list:
    """
    Build the raw 5x3 grid. Indexed grid[reel][row]; reel 0 is leftmost,
    row 0 is the top.
    """
    return [window(strips[i], stops[i]) for i in range(cfg.REELS)]


def expand_wilds(grid: list) -> list:
    """
    Base game transform: any Wild anywhere in a column takes the whole column.

        [J, Zebra, Wild]  ->  [Wild, Wild, Wild]

    Returns a new grid; the input is left alone so callers can still show the
    pre-expansion landing frame in the animation.
    """
    out = []
    for column in grid:
        if cfg.WILD in column:
            out.append([cfg.WILD] * cfg.ROWS)
        else:
            out.append(list(column))
    return out


def apply_sticky(grid: list, sticky: set) -> list:
    """
    Free Games transform: overwrite locked positions with Wild before
    evaluating. `sticky` holds reel indices in "column" mode, or (reel, row)
    pairs in "cell" mode.
    """
    out = [list(col) for col in grid]
    if cfg.STICKY_MODE == "column":
        for reel in sticky:
            out[reel] = [cfg.WILD] * cfg.ROWS
    else:
        for reel, row in sticky:
            out[reel][row] = cfg.WILD
    return out


def collect_sticky(grid: list, sticky: set) -> set:
    """
    Add any Wilds that landed on the middle three reels to the locked set.
    Reels 1 and 5 carry no Wild on the feature strips, but we filter anyway so
    the rule is enforced by the engine rather than only by the strip data.
    """
    new = set(sticky)
    for reel in cfg.FEATURE_WILD_REELS:
        for row in range(cfg.ROWS):
            if grid[reel][row] == cfg.WILD:
                if cfg.STICKY_MODE == "column":
                    new.add(reel)
                else:
                    new.add((reel, row))
    return new


# ---------------------------------------------------------------------------
# Line evaluation
# ---------------------------------------------------------------------------

def _scan_order(direction: str) -> list:
    """Reel visiting order for a chain scan."""
    return list(range(cfg.REELS)) if direction == "left" else list(reversed(range(cfg.REELS)))


def evaluate_line(grid: list, payline: list, direction: str) -> tuple:
    """
    Score one payline in one direction.

    Returns (symbol, chain_length, award_in_line_bets). A run of Wilds pays as
    the best symbol it could substitute for, which is why we take the maximum
    across every candidate symbol rather than just reading the anchor cell.
    """
    order = _scan_order(direction)
    cells = [grid[payline[i][0]][payline[i][1]] for i in order]

    best = (None, 0, 0)
    for sym in cfg.PAY_SYMBOLS:
        chain = 0
        for cell in cells:
            if cell == sym or cell == cfg.WILD:
                chain += 1
            else:
                break
        award = cfg.line_pay(sym, chain)
        if award > best[2]:
            best = (sym, chain, award)
    return best


def evaluate_lines(grid: list, line_bet: int) -> tuple:
    """
    Score every payline. Returns (total_cents, [win dicts]).

    Only the single best award is paid per line - under PAY_DIRECTION "both" a
    line pays whichever direction is worth more, never both at once.
    """
    directions = ("left", "right") if cfg.PAY_DIRECTION == "both" else (cfg.PAY_DIRECTION,)

    total = 0
    wins = []
    for index, payline in enumerate(cfg.PAYLINES):
        best = (None, 0, 0)
        best_dir = None
        for direction in directions:
            result = evaluate_line(grid, payline, direction)
            if result[2] > best[2]:
                best, best_dir = result, direction
        if best[2] > 0:
            cents = best[2] * line_bet
            total += cents
            wins.append({
                "line": index + 1,
                "symbol": best[0],
                "count": best[1],
                "direction": best_dir,
                "multiplier": best[2],
                "cents": cents,
            })
    return total, wins


# ---------------------------------------------------------------------------
# Scatter evaluation
# ---------------------------------------------------------------------------

def count_scatters(grid: list) -> int:
    """
    Africa symbols anywhere on the board. Counted on the RAW grid, before wild
    expansion, so an expanding wild can never wipe out a bonus trigger.
    """
    return sum(col.count(cfg.AFRICA) for col in grid)


def scatter_award(count: int, total_bet: int) -> tuple:
    """Returns (cents, free_spins) for a scatter count."""
    if count < 3:
        return 0, 0
    capped = min(count, 5)
    return cfg.SCATTER_PAY[capped] * total_bet, cfg.FREE_SPINS_AWARD[capped]


# ---------------------------------------------------------------------------
# Spins
# ---------------------------------------------------------------------------

@dataclass
class SpinResult:
    stops: list
    raw_grid: list
    grid: list                       # post-expansion / post-sticky
    line_cents: int = 0
    scatter_cents: int = 0
    scatters: int = 0
    free_spins: int = 0
    wins: list = field(default_factory=list)
    sticky: set = field(default_factory=set)

    @property
    def cents(self) -> int:
        return self.line_cents + self.scatter_cents


@dataclass
class PlayResult:
    base: SpinResult
    feature_spins: list = field(default_factory=list)
    base_cents: int = 0
    feature_cents: int = 0
    capped: bool = False

    @property
    def cents(self) -> int:
        return self.base_cents + self.feature_cents

    @property
    def triggered(self) -> bool:
        return bool(self.feature_spins)


def base_spin(rng: random.Random, total_bet: int) -> SpinResult:
    """One base game spin: expanding wilds, 10 lines, scatter check."""
    line_bet = cfg.line_bet_cents(total_bet)
    stops = [rng.randrange(cfg.STOPS) for _ in range(cfg.REELS)]
    raw = grid_from_stops(cfg.BASE_STRIPS, stops)

    scatters = count_scatters(raw)
    grid = expand_wilds(raw)
    line_cents, wins = evaluate_lines(grid, line_bet)
    scatter_cents, free_spins = scatter_award(scatters, total_bet)

    return SpinResult(
        stops=stops, raw_grid=raw, grid=grid,
        line_cents=line_cents, scatter_cents=scatter_cents,
        scatters=scatters, free_spins=free_spins, wins=wins,
    )


def feature_spin(rng: random.Random, total_bet: int, sticky: set) -> SpinResult:
    """
    One free game. Wilds land only on the middle three reels (enforced by the
    feature strips), expand their column, and stay locked for the rest of the
    feature.
    """
    line_bet = cfg.line_bet_cents(total_bet)
    stops = [rng.randrange(cfg.STOPS) for _ in range(cfg.REELS)]
    raw = grid_from_stops(cfg.FEATURE_STRIPS, stops)

    scatters = count_scatters(raw)
    sticky = collect_sticky(raw, sticky)
    grid = apply_sticky(expand_wilds(raw), sticky)
    line_cents, wins = evaluate_lines(grid, line_bet)

    free_spins = 0
    if cfg.RETRIGGER:
        _, free_spins = scatter_award(scatters, total_bet)

    return SpinResult(
        stops=stops, raw_grid=raw, grid=grid,
        line_cents=line_cents, scatters=scatters,
        free_spins=free_spins, wins=wins, sticky=set(sticky),
    )


def play(rng: random.Random, total_bet: int, keep_spins: bool = True) -> PlayResult:
    """
    A full play: one base spin plus the Free Games feature if it triggers.
    The regulatory ceiling is applied once, to the play total.

    `keep_spins=False` skips retaining per-spin records - the simulator uses
    that to run millions of plays without accumulating garbage.
    """
    base = base_spin(rng, total_bet)
    result = PlayResult(base=base, base_cents=base.cents)

    remaining = base.free_spins
    awarded = remaining
    sticky: set = set()
    spins = []

    while remaining > 0:
        remaining -= 1
        spin = feature_spin(rng, total_bet, sticky)
        sticky = spin.sticky
        result.feature_cents += spin.cents
        if keep_spins:
            spins.append(spin)
        if spin.free_spins and awarded + spin.free_spins <= cfg.MAX_FREE_SPINS:
            remaining += spin.free_spins
            awarded += spin.free_spins

    result.feature_spins = spins if keep_spins else [None] * awarded

    if result.cents > cfg.MAX_PAYOUT_CENTS:
        overflow = result.cents - cfg.MAX_PAYOUT_CENTS
        result.feature_cents = max(0, result.feature_cents - overflow)
        if result.cents > cfg.MAX_PAYOUT_CENTS:
            result.base_cents = cfg.MAX_PAYOUT_CENTS - result.feature_cents
        result.capped = True

    return result
