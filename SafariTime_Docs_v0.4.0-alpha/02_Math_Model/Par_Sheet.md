# Safari Time - Par Sheet

Generated 2026-09-08 by `python -m engine.parsheet --features 1000000`. Every figure below is derived from `engine/config.py`; edit that file and regenerate rather than editing this one.

## Summary

| Metric | Value |
| --- | ---: |
| **Total RTP** | **92.3119%** |
| Base game line RTP (exact) | 72.3536% |
| Scatter RTP (exact) | 6.4964% |
| Free Games RTP (Monte Carlo) | 13.4618% |
| Free Games share of RTP | 14.6% |
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
| 10 | 19.73x | 41.85x | 867x | 0.99 | 6.7% |
| 15 | 50.07x | 88.81x | 1134x | 1.34 | 1.7% |
| 20 | 98.33x | 149.18x | 1338x | 1.62 | 0.4% |

## Base game contribution by combination (exact)

Fraction of total bet returned by each winning combination, summed over all 10 lines.

| Symbol | 3 | 4 | 5 | Total |
| --- | --: | --: | --: | --: |
| Lions | 1.4685% | 0.7115% | 0.0454% | 2.2254% |
| Elephants | 1.8421% | 1.4544% | 0.1200% | 3.4165% |
| Rhinos | 3.9486% | 2.7501% | 0.5266% | 7.2253% |
| Giraffes | 5.0575% | 3.6821% | 0.8538% | 9.5934% |
| Zebras | 5.2800% | 3.9600% | 0.8800% | 10.1200% |
| A | 5.5950% | 2.6526% | 1.6193% | 9.8669% |
| K | 6.9524% | 3.3728% | 2.4091% | 12.7343% |
| Q | 4.4550% | 2.4354% | 2.6730% | 9.5634% |
| J | 3.7752% | 1.7037% | 2.1296% | 7.6085% |
| **All** | | | | **72.3536%** |

## Symbol counts per 100-stop strip

### Base game

| ID | Symbol | R1 | R2 | R3 | R4 | R5 |
| --: | --- | --: | --: | --: | --: | --: |
| 1 | J | 20 | 13 | 12 | 13 | 20 |
| 2 | Q | 18 | 17 | 16 | 17 | 18 |
| 3 | K | 16 | 15 | 15 | 15 | 16 |
| 4 | A | 14 | 13 | 13 | 13 | 14 |
| 6 | Zebras | 10 | 11 | 11 | 11 | 10 |
| 5 | Giraffes | 8 | 9 | 10 | 9 | 8 |
| 7 | Rhinos | 6 | 8 | 8 | 8 | 6 |
| 8 | Elephants | 3 | 5 | 5 | 5 | 3 |
| 9 | Lions | 2 | 3 | 3 | 3 | 2 |
| 10 | Wild | 0 | 3 | 4 | 3 | 0 |
| 11 | Africa | 3 | 3 | 3 | 3 | 3 |

### Free Games (no Wild on reels 1 and 5)

| ID | Symbol | R1 | R2 | R3 | R4 | R5 |
| --: | --- | --: | --: | --: | --: | --: |
| 1 | J | 18 | 15 | 14 | 15 | 18 |
| 2 | Q | 18 | 17 | 16 | 17 | 18 |
| 3 | K | 16 | 15 | 15 | 15 | 16 |
| 4 | A | 14 | 13 | 13 | 13 | 14 |
| 6 | Zebras | 10 | 11 | 11 | 11 | 10 |
| 5 | Giraffes | 8 | 9 | 10 | 9 | 8 |
| 7 | Rhinos | 6 | 8 | 8 | 8 | 6 |
| 8 | Elephants | 4 | 5 | 5 | 5 | 4 |
| 9 | Lions | 3 | 3 | 3 | 3 | 3 |
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
| 0 | J | Q | Q | Q | J |
| 1 | Q | K | K | K | Q |
| 2 | K | J | A | J | K |
| 3 | A | A | J | A | A |
| 4 | Ze | Ze | Ze | Ze | Ze |
| 5 | Gi | Gi | Gi | Gi | Gi |
| 6 | Rh | Rh | Rh | Rh | Rh |
| 7 | J | El | El | El | J |
| 8 | Q | Q | Q | Q | Q |
| 9 | K | K | K | K | K |
| 10 | A | J | **W** | J | A |
| 11 | J | A | A | A | J |
| 12 | El | Ze | J | Ze | El |
| 13 | Q | Li | Ze | Li | Q |
| 14 | Ze | Q | Gi | Q | Ze |
| 15 | K | **W** | Q | **W** | K |
| 16 | **AF** | K | K | K | **AF** |
| 17 | J | Gi | Li | Gi | J |
| 18 | A | **AF** | **AF** | **AF** | A |
| 19 | Q | J | A | J | Q |
| 20 | Gi | A | Rh | A | Gi |
| 21 | K | Rh | J | Rh | K |
| 22 | J | Q | Q | Q | J |
| 23 | Li | Ze | Ze | Ze | Li |
| 24 | Q | K | K | K | Q |
| 25 | A | Q | Gi | Q | A |
| 26 | Ze | J | A | J | Ze |
| 27 | Rh | A | Q | A | Rh |
| 28 | J | Gi | J | Gi | J |
| 29 | K | K | K | K | K |
| 30 | Q | El | El | El | Q |
| 31 | Gi | Rh | Rh | Rh | Gi |
| 32 | A | Ze | Ze | Ze | A |
| 33 | J | Q | Q | Q | J |
| 34 | K | J | A | J | K |
| 35 | Ze | A | Gi | A | Ze |
| 36 | Q | K | K | K | Q |
| 37 | J | Q | J | Q | J |
| 38 | A | Gi | **W** | Gi | A |
| 39 | K | Ze | Q | Ze | K |
| 40 | Rh | J | Ze | J | Rh |
| 41 | Q | A | A | A | Q |
| 42 | J | K | K | K | J |
| 43 | Gi | Rh | Rh | Rh | Gi |
| 44 | Ze | **W** | Gi | **W** | Ze |
| 45 | A | Li | J | Li | A |
| 46 | K | Q | Q | Q | K |
| 47 | Q | **AF** | Li | **AF** | Q |
| 48 | J | El | **AF** | El | J |
| 49 | El | J | K | J | El |
| 50 | **AF** | Q | A | Q | **AF** |
| 51 | J | K | Ze | K | J |
| 52 | Q | A | El | A | Q |
| 53 | K | Ze | Q | Ze | K |
| 54 | A | Gi | J | Gi | A |
| 55 | Ze | Q | Gi | Q | Ze |
| 56 | Gi | Rh | Rh | Rh | Gi |
| 57 | J | K | K | K | J |
| 58 | Q | J | A | J | Q |
| 59 | K | A | Q | A | K |
| 60 | Rh | Ze | Ze | Ze | Rh |
| 61 | A | Gi | **W** | Gi | A |
| 62 | J | Q | J | Q | J |
| 63 | Q | K | K | K | Q |
| 64 | Ze | J | Gi | J | Ze |
| 65 | K | A | A | A | K |
| 66 | J | Q | Q | Q | J |
| 67 | A | Ze | Ze | Ze | A |
| 68 | Gi | Rh | Rh | Rh | Gi |
| 69 | Q | K | K | K | Q |
| 70 | Li | El | El | El | Li |
| 71 | K | Gi | J | Gi | K |
| 72 | J | J | Q | J | J |
| 73 | Rh | A | A | A | Rh |
| 74 | Q | Q | Gi | Q | Q |
| 75 | A | K | K | K | A |
| 76 | Ze | Ze | Ze | Ze | Ze |
| 77 | J | Li | Q | Li | J |
| 78 | K | Q | J | Q | K |
| 79 | Q | J | A | J | Q |
| 80 | Gi | A | Rh | A | Gi |
| 81 | A | Rh | Li | Rh | A |
| 82 | J | **W** | **AF** | **W** | J |
| 83 | El | K | K | K | El |
| 84 | K | Gi | Q | Gi | K |
| 85 | Ze | Q | Gi | Q | Ze |
| 86 | Q | **AF** | Ze | **AF** | Q |
| 87 | **AF** | Ze | J | Ze | **AF** |
| 88 | J | J | A | J | J |
| 89 | A | A | **W** | A | A |
| 90 | K | K | K | K | K |
| 91 | Q | Q | Q | Q | Q |
| 92 | J | El | El | El | J |
| 93 | Rh | Rh | Rh | Rh | Rh |
| 94 | Gi | Gi | Gi | Gi | Gi |
| 95 | Ze | Ze | Ze | Ze | Ze |
| 96 | A | J | J | J | A |
| 97 | K | A | A | A | K |
| 98 | Q | K | K | K | Q |
| 99 | J | Q | Q | Q | J |

## Free Games reel strips

| Stop | R1 | R2 | R3 | R4 | R5 |
| ---: | :-: | :-: | :-: | :-: | :-: |
| 0 | J | Q | Q | Q | J |
| 1 | Q | J | K | J | Q |
| 2 | K | K | J | K | K |
| 3 | A | A | A | A | A |
| 4 | Ze | Ze | Ze | Ze | Ze |
| 5 | Gi | Gi | Gi | Gi | Gi |
| 6 | Rh | Rh | Rh | Rh | Rh |
| 7 | J | El | El | El | J |
| 8 | Q | Q | Q | Q | Q |
| 9 | K | J | K | J | K |
| 10 | A | K | J | K | A |
| 11 | El | A | A | A | El |
| 12 | Li | Ze | Ze | Ze | Li |
| 13 | J | Li | Li | Li | J |
| 14 | Q | Q | Gi | Q | Q |
| 15 | Ze | **AF** | Q | **AF** | Ze |
| 16 | K | J | K | J | K |
| 17 | **AF** | K | **AF** | K | **AF** |
| 18 | A | Gi | J | Gi | A |
| 19 | J | A | A | A | J |
| 20 | Q | Rh | Rh | Rh | Q |
| 21 | Gi | Q | Q | Q | Gi |
| 22 | K | Ze | Ze | Ze | K |
| 23 | Rh | J | K | J | Rh |
| 24 | J | K | J | K | J |
| 25 | Q | Q | Gi | Q | Q |
| 26 | A | A | **W** | A | A |
| 27 | Ze | Gi | A | Gi | Ze |
| 28 | K | El | Q | El | K |
| 29 | Gi | J | K | J | Gi |
| 30 | J | K | El | K | J |
| 31 | Q | Rh | Rh | Rh | Q |
| 32 | A | Ze | Ze | Ze | A |
| 33 | K | Q | J | Q | K |
| 34 | Ze | A | Q | A | Ze |
| 35 | J | J | A | J | J |
| 36 | Q | K | Gi | K | Q |
| 37 | El | Q | K | Q | El |
| 38 | A | Gi | J | Gi | A |
| 39 | K | Ze | Q | Ze | K |
| 40 | Rh | **W** | Ze | **W** | Rh |
| 41 | J | A | A | A | J |
| 42 | Q | J | K | J | Q |
| 43 | Gi | K | Rh | K | Gi |
| 44 | Ze | Q | Gi | Q | Ze |
| 45 | A | Rh | J | Rh | A |
| 46 | K | Li | Q | Li | K |
| 47 | J | **AF** | Li | **AF** | J |
| 48 | Q | El | **AF** | El | Q |
| 49 | Li | J | K | J | Li |
| 50 | **AF** | Q | A | Q | **AF** |
| 51 | J | K | Ze | K | J |
| 52 | Q | A | El | A | Q |
| 53 | K | Ze | Q | Ze | K |
| 54 | A | Gi | J | Gi | A |
| 55 | Ze | Q | Gi | Q | Ze |
| 56 | Gi | Rh | Rh | Rh | Gi |
| 57 | Rh | J | K | J | Rh |
| 58 | J | K | A | K | J |
| 59 | Q | A | Q | A | Q |
| 60 | K | Ze | Ze | Ze | K |
| 61 | A | Gi | J | Gi | A |
| 62 | El | Q | K | Q | El |
| 63 | J | J | Gi | J | J |
| 64 | Q | K | A | K | Q |
| 65 | Ze | A | Q | A | Ze |
| 66 | K | Q | J | Q | K |
| 67 | A | Ze | Ze | Ze | A |
| 68 | Gi | Rh | Rh | Rh | Gi |
| 69 | J | J | K | J | J |
| 70 | Q | K | El | K | Q |
| 71 | K | El | Q | El | K |
| 72 | Rh | Gi | A | Gi | Rh |
| 73 | Ze | A | **W** | A | Ze |
| 74 | J | Q | J | Q | J |
| 75 | Q | J | Gi | J | Q |
| 76 | A | K | K | K | A |
| 77 | K | Ze | Ze | Ze | K |
| 78 | Li | Q | Q | Q | Li |
| 79 | J | A | A | A | J |
| 80 | Q | Rh | Rh | Rh | Q |
| 81 | Gi | Li | J | Li | Gi |
| 82 | A | **AF** | Li | **AF** | A |
| 83 | **AF** | J | K | J | **AF** |
| 84 | K | K | Q | K | K |
| 85 | Ze | Gi | Gi | Gi | Ze |
| 86 | J | Q | **AF** | Q | J |
| 87 | Q | Ze | Ze | Ze | Q |
| 88 | El | A | A | A | El |
| 89 | A | J | J | J | A |
| 90 | K | K | K | K | K |
| 91 | J | Q | Q | Q | J |
| 92 | Q | El | El | El | Q |
| 93 | Rh | Rh | Rh | Rh | Rh |
| 94 | Gi | Gi | Gi | Gi | Gi |
| 95 | Ze | Ze | Ze | Ze | Ze |
| 96 | A | A | A | A | A |
| 97 | K | J | J | J | K |
| 98 | J | K | K | K | J |
| 99 | Q | Q | Q | Q | Q |
