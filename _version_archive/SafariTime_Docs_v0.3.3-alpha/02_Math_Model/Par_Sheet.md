# Safari Time - Par Sheet

Generated 2026-09-08 by `python -m engine.parsheet --features 1000000`. Every figure below is derived from `engine/config.py`; edit that file and regenerate rather than editing this one.

## Summary

| Metric | Value |
| --- | ---: |
| **Total RTP** | **91.9746%** |
| Base game line RTP (exact) | 66.9786% |
| Scatter RTP (exact) | 6.4964% |
| Free Games RTP (Monte Carlo) | 18.4996% |
| Free Games share of RTP | 20.1% |
| Bonus trigger | 1 in 157.7 spins |
| Lines | 10 fixed |
| Pay direction | left (anchored on reel 1) |
| Bets | $0.50, $1.00, $1.50, $2.00 |
| Max payout per play | $800.00 (Montana VGM cap) |
| Virtual stops | 100 per reel = 10,000,000,000 combinations |
| Sticky wild mode | column |
| Retrigger | no |

## Paytable (multiples of line bet)

| Symbol | 3 | 4 | 5 |
| --- | --: | --: | --: |
| Lions | 110 | 420 | 1400 |
| Elephants | 75 | 325 | 900 |
| Rhinos | 38 | 185 | 560 |
| Zebras | 28 | 130 | 375 |
| Giraffes | 28 | 85 | 280 |
| A | 18 | 65 | 170 |
| K | 18 | 65 | 170 |
| Q | 9 | 32 | 110 |
| J | 9 | 32 | 110 |
| Wild | substitutes for all but Africa; expands the reel | | |
| Africa (scatter) | 10 free games | 15 free games | 20 free games |

Top line award: 1400x line bet = 140x total bet ($280.00 at max bet).

## Scatter (Africa) odds

Exactly one Africa can be visible per reel; the count is Poisson-binomial over five reels.

| Africa on screen | Probability | 1 in | Award |
| --: | --: | --: | --- |
| 0 | 0.624032 | 1.6 | - |
| 1 | 0.308587 | 3.2 | - |
| 2 | 0.061039 | 16.4 | - |
| 3 | 0.006037 | 165.6 | 10 free games |
| 4 | 0.000299 | 3,349.8 | 15 free games |
| 5 | 0.000006 | 169,350.9 | 20 free games |

## Free Games (Monte Carlo)

1,000,000 features simulated per spin count. Awards in multiples of total bet.

| Free games | Mean | Std dev | Max seen | Avg reels locked | Zero-win features |
| --: | --: | --: | --: | --: | --: |
| 10 | 27.15x | 63.03x | 1514x | 0.79 | 6.8% |
| 15 | 68.07x | 138.87x | 2096x | 1.10 | 1.7% |
| 20 | 135.12x | 241.61x | 2721x | 1.37 | 0.4% |

## Base game contribution by combination (exact)

Fraction of total bet returned by each winning combination, summed over all 10 lines.

| Symbol | 3 | 4 | 5 | Total |
| --- | --: | --: | --: | --: |
| Lions | 0.5225% | 0.1029% | 0.0070% | 0.6324% |
| Elephants | 1.0253% | 0.3244% | 0.0278% | 1.3775% |
| Rhinos | 1.7100% | 0.8788% | 0.1400% | 2.7288% |
| Zebras | 3.0751% | 1.7911% | 0.4493% | 5.3155% |
| Giraffes | 4.4837% | 1.9942% | 0.7299% | 7.2078% |
| A | 5.2065% | 2.9889% | 1.2726% | 9.4680% |
| K | 7.4162% | 4.7080% | 2.3454% | 14.4696% |
| Q | 4.6359% | 3.2557% | 2.4567% | 10.3484% |
| J | 6.4207% | 4.7080% | 4.3020% | 15.4307% |
| **All** | | | | **66.9786%** |

## Symbol counts per 100-stop strip

### Base game

| ID | Symbol | R1 | R2 | R3 | R4 | R5 |
| --: | --- | --: | --: | --: | --: | --: |
| 1 | J | 21 | 18 | 18 | 18 | 21 |
| 2 | Q | 18 | 17 | 16 | 17 | 18 |
| 3 | K | 16 | 15 | 15 | 15 | 16 |
| 4 | A | 14 | 13 | 13 | 13 | 14 |
| 5 | Giraffes | 10 | 11 | 11 | 11 | 10 |
| 6 | Zebras | 8 | 9 | 10 | 9 | 8 |
| 7 | Rhinos | 5 | 7 | 7 | 7 | 5 |
| 8 | Elephants | 3 | 4 | 4 | 4 | 3 |
| 9 | Lions | 2 | 2 | 2 | 2 | 2 |
| 10 | Wild | 0 | 1 | 1 | 1 | 0 |
| 11 | Africa | 3 | 3 | 3 | 3 | 3 |

### Free Games (no Wild on reels 1 and 5)

| ID | Symbol | R1 | R2 | R3 | R4 | R5 |
| --: | --- | --: | --: | --: | --: | --: |
| 1 | J | 21 | 18 | 18 | 18 | 21 |
| 2 | Q | 18 | 17 | 16 | 17 | 18 |
| 3 | K | 16 | 15 | 15 | 15 | 16 |
| 4 | A | 14 | 13 | 13 | 13 | 14 |
| 5 | Giraffes | 10 | 11 | 11 | 11 | 10 |
| 6 | Zebras | 8 | 9 | 10 | 9 | 8 |
| 7 | Rhinos | 5 | 7 | 7 | 7 | 5 |
| 8 | Elephants | 3 | 4 | 4 | 4 | 3 |
| 9 | Lions | 2 | 2 | 2 | 2 | 2 |
| 10 | Wild | 0 | 1 | 1 | 1 | 0 |
| 11 | Africa | 3 | 3 | 3 | 3 | 3 |

## Paylines

Rows: 0 = top, 1 = middle, 2 = bottom. Each entry is the row used on reels 1-5.

| Line | R1 | R2 | R3 | R4 | R5 |
| --: | :-: | :-: | :-: | :-: | :-: |
| 1 | 1 | 1 | 1 | 1 | 1 |
| 2 | 0 | 0 | 0 | 0 | 0 |
| 3 | 2 | 2 | 2 | 2 | 2 |
| 4 | 0 | 1 | 2 | 1 | 0 |
| 5 | 2 | 1 | 0 | 1 | 2 |
| 6 | 1 | 0 | 0 | 0 | 1 |
| 7 | 1 | 2 | 2 | 2 | 1 |
| 8 | 0 | 0 | 1 | 2 | 2 |
| 9 | 2 | 2 | 1 | 0 | 0 |
| 10 | 1 | 0 | 1 | 0 | 1 |

## Base game reel strips

| Stop | R1 | R2 | R3 | R4 | R5 |
| ---: | :-: | :-: | :-: | :-: | :-: |
| 0 | J | J | J | J | J |
| 1 | Q | Q | Q | Q | Q |
| 2 | K | K | K | K | K |
| 3 | A | A | A | A | A |
| 4 | Gi | Gi | Gi | Gi | Gi |
| 5 | Ze | Ze | Ze | Ze | Ze |
| 6 | J | Rh | Rh | Rh | J |
| 7 | Q | J | J | J | Q |
| 8 | Rh | Q | Q | Q | Rh |
| 9 | K | K | K | K | K |
| 10 | A | El | El | El | A |
| 11 | J | A | A | A | J |
| 12 | El | Gi | Gi | Gi | El |
| 13 | Q | J | J | J | Q |
| 14 | Gi | Q | Ze | Q | Gi |
| 15 | K | **AF** | Q | **AF** | K |
| 16 | J | K | K | K | J |
| 17 | **AF** | Ze | **AF** | Ze | **AF** |
| 18 | A | A | A | A | A |
| 19 | Q | J | J | J | Q |
| 20 | Ze | Q | Rh | Q | Ze |
| 21 | J | Rh | Q | Rh | J |
| 22 | K | Gi | Gi | Gi | K |
| 23 | Li | K | K | K | Li |
| 24 | Q | J | J | J | Q |
| 25 | A | Li | Ze | Li | A |
| 26 | Gi | Q | Li | Q | Gi |
| 27 | J | A | A | A | J |
| 28 | K | Ze | Q | Ze | K |
| 29 | Rh | K | K | K | Rh |
| 30 | Q | J | J | J | Q |
| 31 | J | Gi | Gi | Gi | J |
| 32 | Ze | Q | **W** | Q | Ze |
| 33 | A | A | Q | A | A |
| 34 | K | Rh | A | Rh | K |
| 35 | Gi | J | Ze | J | Gi |
| 36 | J | K | J | K | J |
| 37 | Q | El | K | El | Q |
| 38 | A | Q | Rh | Q | A |
| 39 | J | Ze | El | Ze | J |
| 40 | K | Gi | Q | Gi | K |
| 41 | Q | J | Gi | J | Q |
| 42 | Ze | A | J | A | Ze |
| 43 | Gi | K | A | K | Gi |
| 44 | J | **W** | K | **W** | J |
| 45 | A | Q | Ze | Q | A |
| 46 | K | J | Q | J | K |
| 47 | Q | **AF** | J | **AF** | Q |
| 48 | El | Rh | **AF** | Rh | El |
| 49 | J | Q | K | Q | J |
| 50 | Rh | K | A | K | Rh |
| 51 | **AF** | A | Gi | A | **AF** |
| 52 | Q | Gi | Rh | Gi | Q |
| 53 | K | Ze | J | Ze | K |
| 54 | A | J | Q | J | A |
| 55 | J | Q | Ze | Q | J |
| 56 | Gi | K | K | K | Gi |
| 57 | Ze | A | A | A | Ze |
| 58 | Q | J | J | J | Q |
| 59 | J | Gi | Q | Gi | J |
| 60 | K | Ze | Gi | Ze | K |
| 61 | A | Q | El | Q | A |
| 62 | Q | El | K | El | Q |
| 63 | J | K | J | K | J |
| 64 | Gi | J | Rh | J | Gi |
| 65 | K | Rh | Ze | Rh | K |
| 66 | A | A | Q | A | A |
| 67 | Ze | Q | A | Q | Ze |
| 68 | J | Gi | Gi | Gi | J |
| 69 | Q | J | J | J | Q |
| 70 | Rh | K | K | K | Rh |
| 71 | K | Ze | Q | Ze | K |
| 72 | Li | A | A | A | Li |
| 73 | J | Q | Li | Q | J |
| 74 | Q | J | J | J | Q |
| 75 | A | Li | Ze | Li | A |
| 76 | Gi | K | K | K | Gi |
| 77 | K | Gi | Gi | Gi | K |
| 78 | J | Rh | Q | Rh | J |
| 79 | Q | Q | Rh | Q | Q |
| 80 | Ze | J | J | J | Ze |
| 81 | A | A | A | A | A |
| 82 | El | **AF** | **AF** | **AF** | El |
| 83 | J | K | K | K | J |
| 84 | K | Ze | Q | Ze | K |
| 85 | Gi | Q | Ze | Q | Gi |
| 86 | Q | J | J | J | Q |
| 87 | **AF** | Gi | Gi | Gi | **AF** |
| 88 | J | A | A | A | J |
| 89 | A | El | El | El | A |
| 90 | K | K | K | K | K |
| 91 | Rh | Q | Q | Q | Rh |
| 92 | Q | J | J | J | Q |
| 93 | J | Rh | Rh | Rh | J |
| 94 | Ze | Ze | Ze | Ze | Ze |
| 95 | Gi | Gi | Gi | Gi | Gi |
| 96 | A | A | A | A | A |
| 97 | K | K | K | K | K |
| 98 | Q | Q | Q | Q | Q |
| 99 | J | J | J | J | J |

## Free Games reel strips

| Stop | R1 | R2 | R3 | R4 | R5 |
| ---: | :-: | :-: | :-: | :-: | :-: |
| 0 | J | J | J | J | J |
| 1 | Q | Q | Q | Q | Q |
| 2 | K | K | K | K | K |
| 3 | A | A | A | A | A |
| 4 | Gi | Gi | Gi | Gi | Gi |
| 5 | Ze | Ze | Ze | Ze | Ze |
| 6 | J | Rh | Rh | Rh | J |
| 7 | Q | J | J | J | Q |
| 8 | Rh | Q | Q | Q | Rh |
| 9 | K | K | K | K | K |
| 10 | A | El | El | El | A |
| 11 | J | A | A | A | J |
| 12 | El | Gi | Gi | Gi | El |
| 13 | Q | J | J | J | Q |
| 14 | Gi | Q | Ze | Q | Gi |
| 15 | K | **AF** | Q | **AF** | K |
| 16 | J | K | K | K | J |
| 17 | **AF** | Ze | **AF** | Ze | **AF** |
| 18 | A | A | A | A | A |
| 19 | Q | J | J | J | Q |
| 20 | Ze | Q | Rh | Q | Ze |
| 21 | J | Rh | Q | Rh | J |
| 22 | K | Gi | Gi | Gi | K |
| 23 | Li | K | K | K | Li |
| 24 | Q | J | J | J | Q |
| 25 | A | Li | Ze | Li | A |
| 26 | Gi | Q | Li | Q | Gi |
| 27 | J | A | A | A | J |
| 28 | K | Ze | Q | Ze | K |
| 29 | Rh | K | K | K | Rh |
| 30 | Q | J | J | J | Q |
| 31 | J | Gi | Gi | Gi | J |
| 32 | Ze | Q | **W** | Q | Ze |
| 33 | A | A | Q | A | A |
| 34 | K | Rh | A | Rh | K |
| 35 | Gi | J | Ze | J | Gi |
| 36 | J | K | J | K | J |
| 37 | Q | El | K | El | Q |
| 38 | A | Q | Rh | Q | A |
| 39 | J | Ze | El | Ze | J |
| 40 | K | Gi | Q | Gi | K |
| 41 | Q | J | Gi | J | Q |
| 42 | Ze | A | J | A | Ze |
| 43 | Gi | K | A | K | Gi |
| 44 | J | **W** | K | **W** | J |
| 45 | A | Q | Ze | Q | A |
| 46 | K | J | Q | J | K |
| 47 | Q | **AF** | J | **AF** | Q |
| 48 | El | Rh | **AF** | Rh | El |
| 49 | J | Q | K | Q | J |
| 50 | Rh | K | A | K | Rh |
| 51 | **AF** | A | Gi | A | **AF** |
| 52 | Q | Gi | Rh | Gi | Q |
| 53 | K | Ze | J | Ze | K |
| 54 | A | J | Q | J | A |
| 55 | J | Q | Ze | Q | J |
| 56 | Gi | K | K | K | Gi |
| 57 | Ze | A | A | A | Ze |
| 58 | Q | J | J | J | Q |
| 59 | J | Gi | Q | Gi | J |
| 60 | K | Ze | Gi | Ze | K |
| 61 | A | Q | El | Q | A |
| 62 | Q | El | K | El | Q |
| 63 | J | K | J | K | J |
| 64 | Gi | J | Rh | J | Gi |
| 65 | K | Rh | Ze | Rh | K |
| 66 | A | A | Q | A | A |
| 67 | Ze | Q | A | Q | Ze |
| 68 | J | Gi | Gi | Gi | J |
| 69 | Q | J | J | J | Q |
| 70 | Rh | K | K | K | Rh |
| 71 | K | Ze | Q | Ze | K |
| 72 | Li | A | A | A | Li |
| 73 | J | Q | Li | Q | J |
| 74 | Q | J | J | J | Q |
| 75 | A | Li | Ze | Li | A |
| 76 | Gi | K | K | K | Gi |
| 77 | K | Gi | Gi | Gi | K |
| 78 | J | Rh | Q | Rh | J |
| 79 | Q | Q | Rh | Q | Q |
| 80 | Ze | J | J | J | Ze |
| 81 | A | A | A | A | A |
| 82 | El | **AF** | **AF** | **AF** | El |
| 83 | J | K | K | K | J |
| 84 | K | Ze | Q | Ze | K |
| 85 | Gi | Q | Ze | Q | Gi |
| 86 | Q | J | J | J | Q |
| 87 | **AF** | Gi | Gi | Gi | **AF** |
| 88 | J | A | A | A | J |
| 89 | A | El | El | El | A |
| 90 | K | K | K | K | K |
| 91 | Rh | Q | Q | Q | Rh |
| 92 | Q | J | J | J | Q |
| 93 | J | Rh | Rh | Rh | J |
| 94 | Ze | Ze | Ze | Ze | Ze |
| 95 | Gi | Gi | Gi | Gi | Gi |
| 96 | A | A | A | A | A |
| 97 | K | K | K | K | K |
| 98 | Q | Q | Q | Q | Q |
| 99 | J | J | J | J | J |
