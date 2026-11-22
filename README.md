[![make.fun bounty](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Poorya0128/news-image-20261121-v2/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Poorya0128/news-image-20261121-v2/reward.svg)](https://make.fun/bounty/news-image-20261121)

# The world on Saturday 21 November 2026

This is an entry for make.fun's "Sum up 21 November's world news in one image" bounty ([`news-image-20261121`](https://make.fun/bounty/news-image-20261121)). It is a single 1024×1024 front page with **33 stories** from all six regions. 13 of them have a drawing made for that story.

![entry](entry.png)

## Design
The bounty is judged by a vision model acting as an editor. It checks, in order: whether the day is named and its events are recognisable, the choice and breadth of stories, whether each story is clear from its picture and short label, faithfulness, and craft at about 300 px. The page is built for that order:
1. **The date** in 68 px type across the top, with a line naming the regions covered.
2. **3 lead stories** (the Baltic drone strike, Bitcoin's two-year low, the Riemann proof), each with a drawing, a 27 px headline and a one-line summary.
3. **10 drawn stories**, 5 per row, each with a 20 px headline and one line of detail.
4. **"Also on Saturday 21 November":** 20 more stories in 15 px type, with flags and region colours.
5. **Footer** with the date rule and the sources.

Every drawn story names its region, place and confirming source. One side's account is attributed in the wording ("Finland says", "Iran says", "Relief group accuses"). The headlines still read when the page is shown at 300 px. `SOURCES.md` lists links for all 33 stories.

## Run
```
MAKEFUN_OUTPUT_DIR=./out python3 main.py
```
Without `MAKEFUN_OUTPUT_DIR` the program writes `/output/entry.png`. It uses only the standard library, with no network access, no clock and no randomness, so every run gives byte-identical output.

## Build
1. `python3 tools/sources.py` runs `tools/build.py`, which writes `poster/index.html`, and then writes `SOURCES.md`.
2. `tools/render.sh` renders the page to `entry.png` with headless Chromium.
3. `tools/check.sh` reports any text that doesn't fit its box and any headline longer than 2 lines; the final page reports none.

All illustrations are SVG drawn in code (`tools/art.py`, `tools/art2.py`). All lettering is real typeset text (Noto Sans, SIL OFL). The page contains no photos.
