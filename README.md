# The One-Day World: Saturday 21 November 2026

This is an entry for make.fun's "Sum up 21 November's world news in one image" bounty (`news-image-20261121`). It is a single 1024×1024 front page with **42 stories**, 11 of them illustrated with drawings made for that story. Every story is sourced and filed by region and topic.

![entry](entry.png)

## Rules printed on the page
- **Date:** every story took place between 00:00 and 24:00 UTC on Saturday 21 November 2026. The one exception carries a **REPORT** label: an earlier event that was first made public on Saturday (KCNA's report of Kim's factory visit). The date check lists what was left out on each side of the window. The Peru quake at 00:09 UTC is counted.
- **Region:** each story is filed by where it happened, using the UN M49 grouping (Western Asia, including Turkey, counts as Middle East). Stories with no single location, such as crypto markets, an online proof check or a spacecraft at Mercury, are filed as "Global & space". Sport is filed by venue.
- **Labels:**
  - **CLAIM** (the only red on the page) marks one side's word: a party to a conflict, or an unverified accusation, always attributed.
  - **◆** marks an official statement or official data.
- **Counts:** the region bar widths are the true shares of the 42 stories. The topic row shows War 11 · Politics 10 · Economy 3 · Disaster 2 · Climate 1 · Science 3 · Health 1 · Society 2 · Crime 2 · Culture 1 · Sport 6.

## Layout
1. **Masthead** with a "How to read" key.
2. **Proportional region bar** and topic counts.
3. **UTC timeline** with 8 exact times, each linked to its story number.
4. **3 illustrated leads:** Sparta II off Finland, Hormuz, Sinaloa.
5. **8 cards**, each with a picture specific to its story:
   - Kryvyi Rih's skyline and mine headframe
   - the COP31 plenary with the disputed draft text
   - the EU budget plans compared as bars
   - Bitcoin's intraday price path
   - BepiColombo at Mercury
   - the Riemann critical line
   - a map of the Banda Sea quake
   - the Gaza vehicle strike, with each side's account attributed
6. **Two maps:** a world map and a Europe & Middle East zoom. Every located story has a numbered pin, placed automatically so no pins overlap.
7. **25 briefs** under region headings, each with a place, a source and a label where one applies.
8. **6 sport results** by venue, each with its source.
9. **Date check** and **source key**.

`SOURCES.md`, generated from the same data, lists links for all 42 stories.

## Run
```
MAKEFUN_OUTPUT_DIR=./out python3 main.py      # or: MAKEFUN_OUTPUT_DIR=./out node main.ts
```
Without `MAKEFUN_OUTPUT_DIR` the program writes `/output/entry.png`. It uses only the standard library, with no network access, no clock and no randomness, so every run gives byte-identical output.

## Build
1. `python3 tools/sources.py` runs `tools/build.py`, which writes `poster/index.html`, and then writes `SOURCES.md`. Numbering, counts, grouping and pins are asserted.
2. `tools/render.sh` renders the page to `entry.png` with headless Chromium.
3. The page carries a built-in overflow detector. `tools/check.sh` prints any element whose text doesn't fit its box; the final page reports none.

All illustrations are SVG drawn in code (`tools/art.py`). All lettering is real typeset text (Noto Sans, SIL OFL). The page contains no photos.
