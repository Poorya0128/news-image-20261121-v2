# The One-Day World: Saturday 21 November 2026

This is an entry for make.fun's "Sum up 21 November's world news in one image" bounty (`news-image-20261121`). It is a single 1024×1024 front page with **50 stories**, 15 of them illustrated with drawings made for that story. Every story is colour-coded by region, and every card carries its verification status and source.

![entry](entry.png)

## Rules printed on the page
- **Date:** every story took place between 00:00 and 24:00 UTC on Saturday 21 November 2026. The one exception carries a **REPORT** label: an earlier event that was first made public on Saturday (KCNA's report of Kim's factory visit). The date check lists what was left out on each side of the window. The Peru quake at 00:09 UTC is counted.
- **Region:** each story is filed by where it happened, using the UN M49 grouping (Western Asia, including Turkey, counts as Middle East). Stories with no single location, such as crypto markets, an online proof check or a spacecraft at Mercury, are filed as "Global & space". Sport is filed by venue.
- **Labels:**
  - A green check plus the source name means CONFIRMED: two or more independent outlets, or an official source.
  - **CLAIM** (red) marks one side's account.
  - **REPORTED** marks an earlier event first made public on Saturday.

## Layout
Modelled on the strengths of past winning entries:
1. **Light masthead** with the date in 56 px type.
2. **Proportional 00:00–24:00 UTC timeline** with 9 exact times, each tied to its story number.
3. **3 illustrated leads** and **12 illustrated cards** (6 per row). Each one carries a status chip with its source.
4. **Simple world map:** numbered pins for the illustrated stories, region-coloured dots for the briefs.
5. **Date-check table** listing each story left out and its date.
6. **35 one-line briefs**, each with a number, a region colour and a drawn country flag.
7. **Footer** explaining the labels.

The smallest text on the page is 9.5 px, the same as in the winning entries. Small text uses normal-width Noto Sans. `SOURCES.md` lists links for all 50 stories.

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
