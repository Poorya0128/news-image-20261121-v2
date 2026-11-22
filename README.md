[![make.fun bounty](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Poorya0128/news-image-20261121-v2/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Poorya0128/news-image-20261121-v2/reward.svg)](https://make.fun/bounty/news-image-20261121)

# The One-Day World: Saturday 21 November 2026

This is an entry for make.fun's "Sum up 21 November's world news in one image" bounty ([`news-image-20261121`](https://make.fun/bounty/news-image-20261121)). It is a single 1024×1024 front page with **35 stories**, 13 of them illustrated with drawings made for that story. Every story is colour-coded by region, and every illustrated story carries its verification status and source.

![entry](entry.png)

## Rules printed on the page
- **Date:** every story took place between 00:00 and 24:00 UTC on Saturday 21 November 2026. The one exception carries a **REPORT** label: an earlier event that was first made public on Saturday (KCNA's report of Kim's factory visit). The date check lists what was left out on each side of the window. The Peru quake at 00:09 UTC is counted.
- **Region:** each story is filed by where it happened, using the UN M49 grouping (Western Asia, including Turkey, counts as Middle East). Stories with no single location, such as crypto markets, an online proof check or a spacecraft at Mercury, are filed as "Global & space". Sport is filed by venue.
- **Labels:**
  - A green check plus the source name means CONFIRMED: two or more independent outlets, or an official source.
  - **CLAIM** (red) marks one side's account.
  - **REPORTED** marks an earlier event first made public on Saturday.

## Layout
Modelled on the top three entries of the 20 November bounty:
1. **Light masthead:** the date in 54 px type, with a one-line summary of the day's four biggest stories.
2. **"The day in UTC":** 8 exact times, each tied to its story number.
3. **"The day in numbers":** 8 key figures, each tied to its story.
4. **Region bar** with counts.
5. **3 leads** on the day's biggest stories (the Baltic strike, Bitcoin's slump, the Riemann proof), each with a banner label on its drawing and a status chip.
6. **10 cards**, 5 per row. Each card has a header band in its region colour carrying the story number, a label and the confirmed source.
7. **Simple world map** and **22 one-line briefs** with flags, numbers and labels.
8. **Date check** listing earlier news and items not yet due ("Not yet").
9. **Footer** explaining the labels and naming the sources.

The smallest text on the page is 9.5 px. `SOURCES.md` lists links for all 35 stories.

## Run
```
MAKEFUN_OUTPUT_DIR=./out python3 main.py
```
Without `MAKEFUN_OUTPUT_DIR` the program writes `/output/entry.png`. It uses only the standard library, with no network access, no clock and no randomness, so every run gives byte-identical output.

## Build
1. `python3 tools/sources.py` runs `tools/build.py`, which writes `poster/index.html`, and then writes `SOURCES.md`. Numbering, counts, grouping and pins are asserted.
2. `tools/render.sh` renders the page to `entry.png` with headless Chromium.
3. The page carries a built-in overflow detector. `tools/check.sh` prints any element whose text doesn't fit its box; the final page reports none.

All illustrations are SVG drawn in code (`tools/art.py`). All lettering is real typeset text (Noto Sans, SIL OFL). The page contains no photos.
