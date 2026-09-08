# Safari Time - Par Sheet

Generated 2026-09-08 by `python -m engine.parsheet --features 1000000`. Every figure below is derived from `engine/config.py`; edit that file and regenerate rather than editing this one.

## Summary

| Metric | Value |
| --- | ---: |
| **Total RTP** | **92.1264%** |
| Base game line RTP (exact) | 71.3535% |
| Scatter RTP (exact) | 6.4964% |
| Free Games RTP (Monte Carlo) | 14.2765% |
| Free Games share of RTP | 15.5% |
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
| Lions | 50 | 200 | 625 |
| Elephants | 30 | 150 | 400 |
| Rhinos | 25 | 100 | 300 |
| Giraffes | 20 | 75 | 200 |
| Zebras | 15 | 50 | 100 |
| A | 10 | 20 | 75 |
| K | 10 | 20 | 75 |
| Q | 5 | 10 | 50 |
| J | 5 | 10 | 50 |
| Wild | substitutes for all but Africa; expands the reel | | |
| Africa (scatter) | 10 free games | 15 free games | 20 free games |

Top line award: 625x line bet = 62x total bet ($125.00 at max bet).

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
| 10 | 20.90x | 46.06x | 839x | 0.99 | 8.6% |
| 15 | 53.52x | 97.61x | 1208x | 1.34 | 2.4% |
| 20 | 106.18x | 164.45x | 1545x | 1.62 | 0.7% |

## Base game contribution by combination (exact)

Fraction of total bet returned by each winning combination, summed over all 10 lines.

| Symbol | 3 | 4 | 5 | Total |
| --- | --: | --: | --: | --: |
| Lions | 5.0568% | 3.0952% | 0.6174% | 8.7694% |
| Elephants | 2.9750% | 2.5555% | 0.3587% | 5.8892% |
| Rhinos | 5.3136% | 4.2924% | 1.1197% | 10.7257% |
| Giraffes | 4.2509% | 3.2193% | 0.7465% | 8.2166% |
| Zebras | 4.7482% | 3.2225% | 0.7966% | 8.7673% |
| A | 4.6362% | 1.9973% | 1.2193% | 7.8528% |
| K | 6.3945% | 3.0333% | 2.1666% | 11.5944% |
| Q | 3.0120% | 1.5657% | 1.3815% | 5.9592% |
| J | 2.0267% | 0.8558% | 0.6965% | 3.5790% |
| **All** | | | | **71.3535%** |

## Symbol counts per 100-stop strip

### Base game

| ID | Symbol | R1 | R2 | R3 | R4 | R5 |
| --: | --- | --: | --: | --: | --: | --: |
| 1 | J | 14 | 11 | 10 | 11 | 14 |
| 2 | Q | 15 | 15 | 14 | 15 | 15 |
| 3 | K | 16 | 14 | 15 | 14 | 16 |
| 4 | A | 14 | 13 | 13 | 13 | 14 |
| 6 | Zebras | 11 | 11 | 11 | 11 | 11 |
| 5 | Giraffes | 8 | 9 | 10 | 9 | 8 |
| 7 | Rhinos | 8 | 9 | 9 | 9 | 8 |
| 8 | Elephants | 5 | 7 | 7 | 7 | 5 |
| 9 | Lions | 6 | 5 | 5 | 5 | 6 |
| 10 | Wild | 0 | 3 | 3 | 3 | 0 |
| 11 | Africa | 3 | 3 | 3 | 3 | 3 |

### Free Games (no Wild on reels 1 and 5)

| ID | Symbol | R1 | R2 | R3 | R4 | R5 |
| --: | --- | --: | --: | --: | --: | --: |
| 1 | J | 16 | 15 | 14 | 15 | 16 |
| 2 | Q | 17 | 15 | 15 | 15 | 17 |
| 3 | K | 16 | 14 | 13 | 14 | 16 |
| 4 | A | 14 | 13 | 13 | 13 | 14 |
| 6 | Zebras | 10 | 11 | 11 | 11 | 10 |
| 5 | Giraffes | 8 | 9 | 10 | 9 | 8 |
| 7 | Rhinos | 7 | 9 | 9 | 9 | 7 |
| 8 | Elephants | 5 | 6 | 6 | 6 | 5 |
| 9 | Lions | 4 | 4 | 4 | 4 | 4 |
| 10 | Wild | 0 | 1 | 2 | 1 | 0 |
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
| 0 | K | Q | K | Q | K |
| 1 | Q | K | Q | K | Q |
| 2 | J | A | A | A | J |
| 3 | A | J | Ze | J | A |
| 4 | Ze | Ze | J | Ze | Ze |
| 5 | Gi | Gi | Gi | Gi | Gi |
| 6 | Rh | Rh | Rh | Rh | Rh |
| 7 | Li | El | El | El | Li |
| 8 | El | Li | Li | Li | El |
| 9 | K | Q | K | Q | K |
| 10 | Q | K | Q | K | Q |
| 11 | J | A | A | A | J |
| 12 | A | **W** | Ze | **W** | A |
| 13 | Ze | Ze | **W** | Ze | Ze |
| 14 | **AF** | J | J | J | **AF** |
| 15 | K | **AF** | Gi | **AF** | K |
| 16 | Q | Q | K | Q | Q |
| 17 | J | Gi | Rh | Gi | J |
| 18 | A | Rh | Q | Rh | A |
| 19 | Gi | K | A | K | Gi |
| 20 | Rh | A | **AF** | A | Rh |
| 21 | K | El | El | El | K |
| 22 | Ze | J | Ze | J | Ze |
| 23 | Q | Ze | K | Ze | Q |
| 24 | J | Q | J | Q | J |
| 25 | A | K | Q | K | A |
| 26 | Li | A | Gi | A | Li |
| 27 | K | Gi | A | Gi | K |
| 28 | El | Rh | Rh | Rh | El |
| 29 | Q | Q | K | Q | Q |
| 30 | Gi | Li | Li | Li | Gi |
| 31 | Rh | J | Ze | J | Rh |
| 32 | Ze | Ze | Q | Ze | Ze |
| 33 | J | K | A | K | J |
| 34 | A | A | J | A | A |
| 35 | K | El | Gi | El | K |
| 36 | Q | Q | El | Q | Q |
| 37 | J | Gi | K | Gi | J |
| 38 | A | Rh | Rh | Rh | A |
| 39 | K | K | Q | K | K |
| 40 | Ze | J | Ze | J | Ze |
| 41 | Li | Ze | A | Ze | Li |
| 42 | Q | A | K | A | Q |
| 43 | Gi | **W** | **W** | **W** | Gi |
| 44 | Rh | Q | Gi | Q | Rh |
| 45 | J | K | Q | K | J |
| 46 | A | **AF** | J | **AF** | A |
| 47 | K | Li | **AF** | Li | K |
| 48 | **AF** | El | Li | El | **AF** |
| 49 | Q | J | K | J | Q |
| 50 | Ze | Q | A | Q | Ze |
| 51 | El | A | Ze | A | El |
| 52 | K | Ze | Rh | Ze | K |
| 53 | J | Gi | El | Gi | J |
| 54 | A | Rh | Q | Rh | A |
| 55 | Gi | K | J | K | Gi |
| 56 | Rh | Q | Gi | Q | Rh |
| 57 | Q | A | K | A | Q |
| 58 | Li | J | A | J | Li |
| 59 | K | Ze | Ze | Ze | K |
| 60 | Ze | K | Q | K | Ze |
| 61 | J | Gi | Rh | Gi | J |
| 62 | A | Rh | K | Rh | A |
| 63 | Q | Q | El | Q | Q |
| 64 | K | El | J | El | K |
| 65 | El | A | Gi | A | El |
| 66 | J | K | A | K | J |
| 67 | A | J | Q | J | A |
| 68 | Ze | Ze | Ze | Ze | Ze |
| 69 | Gi | Q | K | Q | Gi |
| 70 | Rh | Li | Li | Li | Rh |
| 71 | Q | Gi | Rh | Gi | Q |
| 72 | K | Rh | A | Rh | K |
| 73 | Li | A | J | A | Li |
| 74 | J | K | Q | K | J |
| 75 | A | Q | Gi | Q | A |
| 76 | Q | J | K | J | Q |
| 77 | Ze | Ze | Ze | Ze | Ze |
| 78 | K | El | El | El | K |
| 79 | Gi | **W** | **W** | **W** | Gi |
| 80 | Rh | A | A | A | Rh |
| 81 | J | K | Q | K | J |
| 82 | A | **AF** | **AF** | **AF** | A |
| 83 | Q | Q | K | Q | Q |
| 84 | K | Gi | Rh | Gi | K |
| 85 | **AF** | Rh | J | Rh | **AF** |
| 86 | Ze | J | Gi | J | Ze |
| 87 | El | Ze | Ze | Ze | El |
| 88 | J | A | A | A | J |
| 89 | A | K | Q | K | A |
| 90 | Q | Q | K | Q | Q |
| 91 | K | Li | Li | Li | K |
| 92 | Li | El | El | El | Li |
| 93 | Gi | Gi | Rh | Gi | Gi |
| 94 | Rh | Rh | J | Rh | Rh |
| 95 | Ze | J | Gi | J | Ze |
| 96 | J | Ze | Ze | Ze | J |
| 97 | A | A | A | A | A |
| 98 | Q | K | Q | K | Q |
| 99 | K | Q | K | Q | K |

## Free Games reel strips

| Stop | R1 | R2 | R3 | R4 | R5 |
| ---: | :-: | :-: | :-: | :-: | :-: |
| 0 | Q | J | Q | J | Q |
| 1 | J | Q | J | Q | J |
| 2 | K | K | K | K | K |
| 3 | A | A | A | A | A |
| 4 | Ze | Ze | Ze | Ze | Ze |
| 5 | Gi | Gi | Gi | Gi | Gi |
| 6 | Rh | Rh | Rh | Rh | Rh |
| 7 | El | El | El | El | El |
| 8 | Q | Li | Li | Li | Q |
| 9 | J | J | Q | J | J |
| 10 | K | Q | J | Q | K |
| 11 | A | K | K | K | A |
| 12 | Li | A | A | A | Li |
| 13 | **AF** | Ze | Ze | Ze | **AF** |
| 14 | Q | **AF** | Gi | **AF** | Q |
| 15 | Ze | Gi | **AF** | Gi | Ze |
| 16 | J | J | Q | J | J |
| 17 | K | Q | Rh | Q | K |
| 18 | A | Rh | J | Rh | A |
| 19 | Gi | K | K | K | Gi |
| 20 | Q | A | A | A | Q |
| 21 | Rh | Ze | **W** | Ze | Rh |
| 22 | J | J | Ze | J | J |
| 23 | K | Q | Q | Q | K |
| 24 | A | K | J | K | A |
| 25 | Ze | El | Gi | El | Ze |
| 26 | Q | A | El | A | Q |
| 27 | J | Gi | K | Gi | J |
| 28 | K | Rh | A | Rh | K |
| 29 | El | J | Rh | J | El |
| 30 | Gi | Q | Q | Q | Gi |
| 31 | A | Ze | Ze | Ze | A |
| 32 | Q | K | J | K | Q |
| 33 | J | A | K | A | J |
| 34 | K | Li | A | Li | K |
| 35 | Ze | J | Gi | J | Ze |
| 36 | Rh | Q | Q | Q | Rh |
| 37 | Li | Gi | Li | Gi | Li |
| 38 | Q | Rh | Rh | Rh | Q |
| 39 | A | K | J | K | A |
| 40 | J | Ze | Ze | Ze | J |
| 41 | K | El | El | El | K |
| 42 | Gi | A | K | A | Gi |
| 43 | Q | J | A | J | Q |
| 44 | Ze | **W** | Q | **W** | Ze |
| 45 | A | Q | Gi | Q | A |
| 46 | J | K | J | K | J |
| 47 | K | **AF** | **AF** | **AF** | K |
| 48 | **AF** | Gi | Rh | Gi | **AF** |
| 49 | Q | J | Q | J | Q |
| 50 | Rh | Q | K | Q | Rh |
| 51 | El | A | A | A | El |
| 52 | J | Ze | Ze | Ze | J |
| 53 | K | Rh | J | Rh | K |
| 54 | A | K | Gi | K | A |
| 55 | Ze | J | Q | J | Ze |
| 56 | Q | Q | El | Q | Q |
| 57 | Gi | A | K | A | Gi |
| 58 | J | El | A | El | J |
| 59 | K | Ze | Ze | Ze | K |
| 60 | A | K | J | K | A |
| 61 | Q | Gi | Rh | Gi | Q |
| 62 | Li | Rh | Li | Rh | Li |
| 63 | Rh | J | Q | J | Rh |
| 64 | Ze | Q | Gi | Q | Ze |
| 65 | J | Li | K | Li | J |
| 66 | K | A | A | A | K |
| 67 | Q | K | J | K | Q |
| 68 | A | Ze | Ze | Ze | A |
| 69 | Gi | J | Q | J | Gi |
| 70 | El | Q | **W** | Q | El |
| 71 | J | Gi | Rh | Gi | J |
| 72 | K | Rh | K | Rh | K |
| 73 | Q | A | A | A | Q |
| 74 | A | K | J | K | A |
| 75 | Ze | El | Gi | El | Ze |
| 76 | Rh | J | El | J | Rh |
| 77 | J | Q | Q | Q | J |
| 78 | K | Ze | Ze | Ze | K |
| 79 | Q | A | K | A | Q |
| 80 | Gi | **AF** | A | **AF** | Gi |
| 81 | A | K | J | K | A |
| 82 | **AF** | Gi | **AF** | Gi | **AF** |
| 83 | J | J | Q | J | J |
| 84 | K | Q | Rh | Q | K |
| 85 | Q | Rh | Gi | Rh | Q |
| 86 | Ze | Ze | Ze | Ze | Ze |
| 87 | Li | Li | Li | Li | Li |
| 88 | A | A | K | A | A |
| 89 | El | K | A | K | El |
| 90 | J | J | J | J | J |
| 91 | K | Q | Q | Q | K |
| 92 | Q | El | El | El | Q |
| 93 | Rh | Gi | Rh | Gi | Rh |
| 94 | Gi | Rh | Gi | Rh | Gi |
| 95 | Ze | Ze | Ze | Ze | Ze |
| 96 | A | A | K | A | A |
| 97 | J | K | A | K | J |
| 98 | K | J | J | J | K |
| 99 | Q | Q | Q | Q | Q |
