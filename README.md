# The One-Day World: Saturday 21 November 2026

This is an entry for make.fun's "Sum up 21 November's world news in one image" bounty (`news-image-20261121`). It is a single 1024×1024 front page with **39 stories**, 11 of them illustrated with drawings made for that story. Every story is sourced and colour-coded by region.

![entry](entry.png)

## Rules printed on the page
- **Date:** every story took place between 00:00 and 24:00 UTC on Saturday 21 November 2026. The one exception carries a **REPORT** label: an earlier event that was first made public on Saturday (KCNA's report of Kim's factory visit). The date check lists what was left out on each side of the window. The Peru quake at 00:09 UTC is counted.
- **Region:** each story is filed by where it happened, using the UN M49 grouping (Western Asia, including Turkey, counts as Middle East). Stories with no single location, such as crypto markets, an online proof check or a spacecraft at Mercury, are filed as "Global & space". Sport is filed by venue.
- **Labels:**
  - **CLAIM** (the only red on the page) marks one side's word: a party to a conflict, or an unverified accusation, always attributed.
  - A **green check** marks an official statement or official data.
  - **REPORT** marks an earlier event first made public on Saturday.
  - The illustrated stories 1–11 carry no label, because each is confirmed by two or more independent sources.
- **Region bar:** each segment's width is the true share of the 39 stories.

## Layout
1. **Masthead** with a "How to read" key.
2. **Proportional region bar.**
3. **Large UTC timeline** with 8 exact times, each linked to its story number.
4. **3 illustrated leads** and **8 illustrated cards**, each picture specific to its story.
5. **Simple world map:** numbered pins for stories 1–11, and dots in the region colour for briefs and sport.
6. **Structured date check:** what was counted, the edge case, the exception, and what fell too early or too late.
7. **22 one-line briefs** at 14.5 px, colour-coded by region and numbered, each with its source and a label where one applies.
8. **6 sport results** in a larger strip, each with its source.
9. **Source key.**

Small text uses normal-width Noto Sans, which stays sharp at small sizes. `SOURCES.md` lists links for all 39 stories.

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
