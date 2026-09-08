# Safari Time

A 5-reel, 3-row, 10-line video slot built to Montana VGM limits ($2.00 max bet,
$800 max payout), with expanding wilds in the base game and sticky expanding
wilds in a Free Games feature.

The whole game is defined once, in `engine/config.py`. The exact solver, the
Monte Carlo simulator and the browser game all read from it, so the game you
play is the game that was modelled.

## Layout

```
engine/            Python maths engine
  config.py        THE par sheet: symbols, strips, paytable, paylines, rules
  game.py          spin -> expanding wilds -> line/scatter evaluation -> feature
  exact.py         closed-form base game RTP (no simulation needed)
  simulate.py      Monte Carlo: Free Games EV, full-game validation, volatility
  tune.py          solves the paytable scale for a target RTP
  parsheet.py      writes the Markdown par sheet into the docs folder
  export.py        writes web/gamedata.js (rules, strips, art + audio manifests)
  slice_art.py     cuts the symbol contact sheet into per-symbol WebP tiles
  encode_audio.js  encodes the source WAVs to MP3 for the web build (Node + lamejs)
tests/             engine tests incl. exact-vs-simulation cross-checks
web/               the playable game (static HTML, no build step)
  assets/symbols/  symbol art (see README inside)
  assets/audio/    MP3s generated from the docs folder's source WAVs
SafariTime_Docs_v0.2.0-alpha/   design + maths documentation, source audio (versioned)
_version_archive/               frozen copies of superseded doc versions
```

## Rebuild the assets

```bash
python -m engine.slice_art SHEET.jpg AFRICA.jpg
npm install lamejs@1.2.1
node engine/encode_audio.js SafariTime_Docs_v0.3.1-alpha/03_Assets_Audio web/assets/audio --lamejs node_modules/lamejs/lame.all.js
python -m engine.export
```

## Run the maths

```bash
python -m engine.simulate                       # RTP breakdown, 200k features
python -m engine.simulate --plays 200000        # + full-game validation with cap
python -m engine.tune --target 0.92             # propose a paytable for 92%
python -m engine.parsheet --features 1000000    # regenerate the par sheet
python -m unittest tests.test_engine            # ~20s
```

## Run the game

```bash
python -m engine.export      # regenerate web/gamedata.js after any config change
```

Then open `web/index.html` in a browser, or serve the `web/` folder. Deployed
with Firebase Hosting: `firebase deploy`.

## Rules in one breath

10 lines always on. Wins are 3+ adjacent from **reel 1 rightwards**, highest win
per line. A WILD anywhere on a reel expands to fill it before pays. 3/4/5
AFRICA anywhere award 10/15/20 Free Games; in Free Games WILDs land only on
reels 2-4, expand, and stay for the rest of the feature. $800 cap per play.

Design decisions and the maths are in the `SafariTime_Docs_v*/` folder.
