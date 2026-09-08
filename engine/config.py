"""
Safari Time / Wildlife Montana - game configuration (the par sheet in code form).

Everything defining the game's maths lives here. The engine, the exact solver,
the Monte Carlo simulator and the web front-end all read this one module, so
the game you play is provably the game you modelled.

Money is handled in integer CENTS everywhere. Never floats.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# 1. SYMBOLS
# ---------------------------------------------------------------------------
# Integer IDs ordered by payout size (lowest first), per the art sheet.

J, Q, K, A, GIRAFFE, ZEBRA, RHINO, ELEPHANT, LION, WILD, AFRICA = range(1, 12)

SYMBOL_NAMES = {
    J: "J", Q: "Q", K: "K", A: "A",
    GIRAFFE: "Giraffes", ZEBRA: "Zebras", RHINO: "Rhinos",
    ELEPHANT: "Elephants", LION: "Lions",
    WILD: "Wild", AFRICA: "Africa",
}

# Symbols with their own paytable entry; these can start a line chain.
PAY_SYMBOLS = (J, Q, K, A, GIRAFFE, ZEBRA, RHINO, ELEPHANT, LION)

# ---------------------------------------------------------------------------
# 2. CABINET / WAGERING
# ---------------------------------------------------------------------------
# Montana VGM constraints: max bet $2.00, max payout $800 per play.

LINES = 10
BET_STEP_CENTS = 50
MIN_BET_CENTS = 50
MAX_BET_CENTS = 200
BET_LEVELS_CENTS = list(range(MIN_BET_CENTS, MAX_BET_CENTS + 1, BET_STEP_CENTS))

MAX_PAYOUT_CENTS = 80_000       # $800.00 hard regulatory ceiling per play


def line_bet_cents(total_bet_cents: int) -> int:
    """Line bet = total bet / LINES. 50c/10 = 5c per line at minimum bet."""
    assert total_bet_cents % LINES == 0, "total bet must divide evenly by LINES"
    return total_bet_cents // LINES


# ---------------------------------------------------------------------------
# 3. REEL GEOMETRY
# ---------------------------------------------------------------------------

REELS = 5
ROWS = 3
STOPS = 100                     # virtual stops per strip -> 100^5 combinations

# WILD lands only on the middle three reels - in the base game and in Free
# Games alike. Reels 1 and 5 never show one.
WILD_REELS = (1, 2, 3)
FEATURE_WILD_REELS = WILD_REELS  # reels whose Wilds stick during Free Games

# ---------------------------------------------------------------------------
# 4. PAY DIRECTION
# ---------------------------------------------------------------------------
# Chains read LEFT TO RIGHT from reel 1 (conventional; matches the reference
# screenshots). "right" anchors on reel 5; "both" pays each line whichever way
# gives the larger award. The strips are mirror-symmetric, so "left" and
# "right" solve to the same RTP; "both" does not and needs re-tuning.

PAY_DIRECTION = "left"          # "right" | "left" | "both"
MIN_CHAIN = 3

# ---------------------------------------------------------------------------
# 5. PAYLINES
# ---------------------------------------------------------------------------
# Ten lines over the 5x3 window, each 5 (reel, row) pairs listed left-to-right.
# PAY_DIRECTION decides which end they are scanned from.
# Row 0 = top, row 1 = middle, row 2 = bottom.

PAYLINES = [
    [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1)],   # 1  middle
    [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)],   # 2  top
    [(0, 2), (1, 2), (2, 2), (3, 2), (4, 2)],   # 3  bottom
    [(0, 0), (1, 1), (2, 2), (3, 1), (4, 0)],   # 4  V
    [(0, 2), (1, 1), (2, 0), (3, 1), (4, 2)],   # 5  inverted V
    [(0, 1), (1, 0), (2, 0), (3, 0), (4, 1)],   # 6  shallow top
    [(0, 1), (1, 2), (2, 2), (3, 2), (4, 1)],   # 7  shallow bottom
    [(0, 0), (1, 0), (2, 1), (3, 2), (4, 2)],   # 8  descending
    [(0, 2), (1, 2), (2, 1), (3, 0), (4, 0)],   # 9  ascending
    [(0, 1), (1, 0), (2, 1), (3, 0), (4, 1)],   # 10 zigzag
]
assert len(PAYLINES) == LINES

# ---------------------------------------------------------------------------
# 6. PAYTABLE
# ---------------------------------------------------------------------------
# Award as a MULTIPLE OF THE LINE BET, indexed by chain length (3, 4, 5).
# Solved for the RTP target by engine/tune.py.

PAYTABLE = {
    #            3    4     5
    J:        (  9,  35,  120),
    Q:        (  9,  35,  120),
    K:        ( 20,  70,  180),
    A:        ( 20,  70,  180),
    GIRAFFE:  ( 30,  90,  300),
    ZEBRA:    ( 30, 140,  400),
    RHINO:    ( 40, 200,  600),
    ELEPHANT: ( 80, 350,  950),
    LION:     (120, 450, 1500),
}


def line_pay(symbol: int, chain: int) -> int:
    """Award for `chain` of `symbol`, as a multiple of the line bet."""
    if chain < MIN_CHAIN:
        return 0
    return PAYTABLE[symbol][chain - MIN_CHAIN]


# Best award available for a chain of length n across all symbols. A chain made
# purely of Wilds pays as the highest-value symbol it could stand in for.
BEST_PAY = {n: max(line_pay(s, n) for s in PAY_SYMBOLS) for n in range(0, 6)}

# ---------------------------------------------------------------------------
# 7. SCATTER / FREE GAMES
# ---------------------------------------------------------------------------
# Africa scatters pay nothing on their own; they only award Free Games.

SCATTER_PAY = {3: 0, 4: 0, 5: 0}          # multiples of TOTAL bet
FREE_SPINS_AWARD = {3: 10, 4: 15, 5: 20}

# Free Games wild behaviour:
#   "column" - a Wild expands its whole reel and that reel STAYS wild for the
#              rest of the feature (base game expanding wild + "wilds stay").
#   "cell"   - only the landing coordinate locks.
STICKY_MODE = "column"

RETRIGGER = False               # scatters during Free Games award nothing
MAX_FREE_SPINS = 200            # safety cap should RETRIGGER be enabled

# ---------------------------------------------------------------------------
# 8. VIRTUAL REEL STRIPS
# ---------------------------------------------------------------------------
# Symbol counts per 100-stop strip; each column must sum to STOPS.
# Reels 1 and 5 are the two most restrictive strips and mirror each other, so
# the maths is identical whichever end the chain is anchored on.

BASE_COUNTS = {
    #            R1  R2  R3  R4  R5
    J:        [ 21, 18, 18, 18, 21],
    Q:        [ 18, 17, 16, 17, 18],
    K:        [ 16, 15, 15, 15, 16],
    A:        [ 14, 13, 13, 13, 14],
    GIRAFFE:  [ 10, 11, 11, 11, 10],
    ZEBRA:    [  8,  9, 10,  9,  8],
    RHINO:    [  5,  7,  7,  7,  5],
    ELEPHANT: [  3,  4,  4,  4,  3],
    LION:     [  2,  2,  2,  2,  2],
    WILD:     [  0,  1,  1,  1,  0],
    AFRICA:   [  3,  3,  3,  3,  3],
}

# Free Games use the same strips today. Kept separate so the feature can be
# weighted differently later without touching the base game.
FEATURE_COUNTS = {sym: list(row) for sym, row in BASE_COUNTS.items()}

for _counts in (BASE_COUNTS, FEATURE_COUNTS):
    for _r in range(REELS):
        assert (_counts[WILD][_r] > 0) == (_r in WILD_REELS), (
            f"Wild count on reel {_r + 1} contradicts WILD_REELS"
        )


def build_strip(counts_for_reel: dict, stops: int = STOPS) -> list:
    """
    Lay a strip out deterministically, spreading each symbol as evenly as
    possible around the 100 stops.

    At every position we place whichever symbol is furthest behind its fair
    share so far (largest deficit wins, lowest ID breaks ties). That keeps rare
    symbols maximally separated, which is what enforces the "only one Africa
    per reel at a time" rule without any special-casing.
    """
    placed = {sym: 0 for sym in counts_for_reel}
    strip = []
    for pos in range(stops):
        target_share = (pos + 1) / stops
        best_sym, best_deficit = None, None
        for sym, total in sorted(counts_for_reel.items()):
            if placed[sym] >= total:
                continue
            deficit = total * target_share - placed[sym]
            if best_deficit is None or deficit > best_deficit:
                best_sym, best_deficit = sym, deficit
        assert best_sym is not None
        strip.append(best_sym)
        placed[best_sym] += 1
    assert len(strip) == stops
    return strip


def build_strips(counts: dict) -> list:
    strips = []
    for reel in range(REELS):
        per_reel = {sym: row[reel] for sym, row in counts.items() if row[reel] > 0}
        total = sum(per_reel.values())
        assert total == STOPS, f"reel {reel + 1} counts sum to {total}, need {STOPS}"
        strips.append(build_strip(per_reel))
    return strips


BASE_STRIPS = build_strips(BASE_COUNTS)
FEATURE_STRIPS = build_strips(FEATURE_COUNTS)


def _assert_one_scatter_per_window(strips: list, label: str) -> None:
    """Enforce: at most one Africa scatter visible on a reel at a time."""
    for i, strip in enumerate(strips):
        for s in range(STOPS):
            window = [strip[(s + r) % STOPS] for r in range(ROWS)]
            if window.count(AFRICA) > 1:
                raise AssertionError(
                    f"{label} reel {i + 1} stop {s}: two Africa share a window"
                )


_assert_one_scatter_per_window(BASE_STRIPS, "base")
_assert_one_scatter_per_window(FEATURE_STRIPS, "feature")
