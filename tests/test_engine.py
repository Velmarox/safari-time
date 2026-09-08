"""
Safari Time engine tests.

Run:  python -m pytest tests -q      (or)      python -m tests.test_engine

The important ones are the cross-checks: the fast line scorer in simulate.py
against a brute-force scorer, and the exact solver against Monte Carlo. If
either drifts, the par sheet is lying.
"""

from __future__ import annotations

import random
import sys
import unittest

sys.path.insert(0, ".")

from engine import config as cfg          # noqa: E402
from engine import exact, game, simulate  # noqa: E402

J, Q, K, A, G, Z, R, E, L, W, S = range(1, 12)


def grid(*columns):
    return [list(c) for c in columns]


def brute_line(cells: list) -> int:
    """Reference scorer: literally try every symbol, take the best award."""
    best = 0
    for sym in cfg.PAY_SYMBOLS:
        chain = 0
        for c in cells:
            if c == sym or c == W:
                chain += 1
            else:
                break
        best = max(best, cfg.line_pay(sym, chain))
    return best


class Config(unittest.TestCase):
    def test_strips_are_100_stops_and_counts_match(self):
        for reel in range(cfg.REELS):
            self.assertEqual(len(cfg.BASE_STRIPS[reel]), cfg.STOPS)
            for sym, row in cfg.BASE_COUNTS.items():
                self.assertEqual(cfg.BASE_STRIPS[reel].count(sym), row[reel])

    def test_only_one_africa_visible_per_reel(self):
        for strips in (cfg.BASE_STRIPS, cfg.FEATURE_STRIPS):
            for strip in strips:
                for stop in range(cfg.STOPS):
                    win = game.window(strip, stop)
                    self.assertLessEqual(win.count(S), 1)

    def test_feature_wilds_only_on_middle_reels(self):
        self.assertNotIn(W, cfg.FEATURE_STRIPS[0])
        self.assertNotIn(W, cfg.FEATURE_STRIPS[4])
        for reel in cfg.FEATURE_WILD_REELS:
            self.assertIn(W, cfg.FEATURE_STRIPS[reel])

    def test_bet_levels_are_montana_legal(self):
        self.assertEqual(cfg.BET_LEVELS_CENTS, [50, 100, 150, 200])
        self.assertEqual(cfg.MAX_PAYOUT_CENTS, 80_000)
        for bet in cfg.BET_LEVELS_CENTS:
            self.assertEqual(cfg.line_bet_cents(bet) * cfg.LINES, bet)

    def test_paytable_is_monotonic(self):
        for sym in cfg.PAY_SYMBOLS:
            a, b, c = cfg.PAYTABLE[sym]
            self.assertLess(a, b)
            self.assertLess(b, c)
        # Symbols ordered by payout size, as the art sheet promises.
        for lo, hi in zip(cfg.PAY_SYMBOLS, cfg.PAY_SYMBOLS[1:]):
            self.assertLessEqual(cfg.PAYTABLE[lo][2], cfg.PAYTABLE[hi][2])


class Evaluation(unittest.TestCase):
    def test_expanding_wild_takes_whole_column(self):
        g = grid([J, Q, K], [J, W, K], [A, A, A], [Z, Z, Z], [L, L, L])
        out = game.expand_wilds(g)
        self.assertEqual(out[1], [W, W, W])
        self.assertEqual(out[0], [J, Q, K])
        self.assertEqual(g[1], [J, W, K], "input must not be mutated")

    def test_three_minimum(self):
        g = grid([J, J, J], [J, J, J], [Q, Q, Q], [Q, Q, Q], [Q, Q, Q])
        self.assertEqual(game.evaluate_line(g, cfg.PAYLINES[0], "left")[2], cfg.line_pay(J, 2))
        self.assertEqual(game.evaluate_line(g, cfg.PAYLINES[0], "right")[2], cfg.line_pay(Q, 3))

    def test_direction_matters(self):
        g = grid([A, A, A], [W, W, W], [W, W, W], [Q, Q, Q], [K, K, K])
        self.assertEqual(game.evaluate_line(g, cfg.PAYLINES[0], "left")[2], cfg.line_pay(A, 3))
        self.assertEqual(game.evaluate_line(g, cfg.PAYLINES[0], "right")[2], 0)

    def test_pure_wild_run_pays_as_best_symbol(self):
        # Right-to-left: W W W W J. As "J" that is a 5-chain worth 100; as
        # "Lion" the four Wilds alone are worth 400. The line must pay 400.
        g = grid([J, J, J], [W, W, W], [W, W, W], [W, W, W], [W, W, W])
        sym, n, award = game.evaluate_line(g, cfg.PAYLINES[0], "right")
        self.assertGreater(cfg.line_pay(L, 4), cfg.line_pay(J, 5))
        self.assertEqual((sym, n, award), (L, 4, cfg.line_pay(L, 4)))

    def test_five_of_a_kind_through_wilds(self):
        g = grid([L, L, L], [W, W, W], [L, L, L], [W, W, W], [L, L, L])
        self.assertEqual(game.evaluate_line(g, cfg.PAYLINES[0], "right")[2], cfg.line_pay(L, 5))

    def test_scatter_breaks_chain_and_counts_pre_expansion(self):
        raw = grid([S, W, J], [J, S, J], [J, J, S], [Q, Q, Q], [Q, Q, Q])
        self.assertEqual(game.count_scatters(raw), 3)
        expanded = game.expand_wilds(raw)
        self.assertEqual(expanded[0], [W, W, W])
        self.assertEqual(game.count_scatters(raw), 3, "raw grid untouched")

    def test_scatter_awards(self):
        self.assertEqual(game.scatter_award(2, 100), (0, 0))
        self.assertEqual(game.scatter_award(3, 100), (0, 10))
        self.assertEqual(game.scatter_award(4, 100), (0, 15))
        self.assertEqual(game.scatter_award(5, 100), (0, 20))

    def test_fast_scorer_matches_brute_force(self):
        rng = random.Random(42)
        lines, best_any, best_other, pay = simulate._line_tables()
        symbols = list(range(1, 12))
        for _ in range(20_000):
            g = [[rng.choice(symbols) for _ in range(3)] for _ in range(5)]
            fast = simulate._score_grid(g, lines, best_any, best_other, pay)
            slow = sum(brute_line([g[r][c] for r, c in line]) for line in lines)
            self.assertEqual(fast, slow, g)

    def test_engine_evaluate_lines_matches_brute_force(self):
        rng = random.Random(7)
        symbols = list(range(1, 12))
        order = list(reversed(range(5))) if cfg.PAY_DIRECTION == "right" else list(range(5))
        for _ in range(5_000):
            g = [[rng.choice(symbols) for _ in range(3)] for _ in range(5)]
            total, _ = game.evaluate_lines(g, 1)
            slow = sum(brute_line([g[line[i][0]][line[i][1]] for i in order]) for line in cfg.PAYLINES)
            self.assertEqual(total, slow)


class FreeGames(unittest.TestCase):
    def test_sticky_column_locks_and_persists(self):
        raw = grid([J, J, J], [J, W, J], [Q, Q, Q], [Q, Q, Q], [Q, Q, Q])
        sticky = game.collect_sticky(raw, set())
        self.assertEqual(sticky, {1})
        later = grid([J, J, J], [K, K, K], [Q, Q, Q], [Q, Q, Q], [Q, Q, Q])
        out = game.apply_sticky(later, sticky)
        self.assertEqual(out[1], [W, W, W])
        self.assertEqual(later[1], [K, K, K], "input must not be mutated")

    def test_wild_on_end_reel_never_sticks(self):
        raw = grid([W, J, J], [J, J, J], [Q, Q, Q], [Q, Q, Q], [J, J, W])
        self.assertEqual(game.collect_sticky(raw, set()), set())

    def test_play_awards_correct_number_of_free_spins(self):
        rng = random.Random(0)
        seen = set()
        for _ in range(200_000):
            result = game.play(rng, 50)
            if result.triggered:
                seen.add((result.base.scatters, len(result.feature_spins)))
        self.assertIn((3, 10), seen)
        for scatters, spins in seen:
            self.assertEqual(spins, cfg.FREE_SPINS_AWARD[min(scatters, 5)])


class Cap(unittest.TestCase):
    def test_play_total_never_exceeds_cap(self):
        rng = random.Random(3)
        for bet in cfg.BET_LEVELS_CENTS:
            for _ in range(50_000):
                result = game.play(rng, bet, keep_spins=False)
                self.assertLessEqual(result.cents, cfg.MAX_PAYOUT_CENTS)
                self.assertGreaterEqual(result.base_cents, 0)
                self.assertGreaterEqual(result.feature_cents, 0)


class ExactVsMonteCarlo(unittest.TestCase):
    def test_scatter_distribution_sums_to_one(self):
        dist = exact.scatter_distribution(cfg.BASE_STRIPS)
        self.assertAlmostEqual(sum(dist.values()), 1.0, places=12)
        self.assertEqual(max(dist), 5, "never more than one scatter per reel")

    def test_exact_base_line_rtp_matches_simulation(self):
        """Simulate base spins only and compare with the closed-form answer."""
        exact_rtp = exact.base_line_math()["rtp"]
        rng = random.Random(11)
        plays = 300_000
        bet = 100
        won = sum(game.base_spin(rng, bet).line_cents for _ in range(plays))
        sim_rtp = won / (plays * bet)
        # Base-game SD is a few x bet; 300k plays gives ~+-0.5% at 3 sigma.
        self.assertAlmostEqual(sim_rtp, exact_rtp, delta=0.012,
                               msg=f"exact {exact_rtp:.4f} vs sim {sim_rtp:.4f}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
