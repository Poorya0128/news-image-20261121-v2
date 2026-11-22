# The One-Day World: Saturday 21 November 2026

This is an entry for make.fun's "Sum up 21 November's world news in one image" bounty (`news-image-20261121`). It is a single 1024×1024 front page with **44 stories** from 6 continents, all from Saturday 21 November 2026.

![entry](entry.png)

## Layout
- **Lead (1):** drones set the Russian cargo ship Sparta II ablaze off Finland, with an illustration drawn in code.
- **World map:** 32 numbered pins that use the same numbers as the stories, plus a Mercury inset for story 6.
- **"By the numbers" strip:** each figure links back to its story number.
- **Five illustrated cards (2–6):** Sinaloa, Hormuz, Kryvyi Rih, COP31, BepiColombo.
- **Five regional columns (7–34):** Europe, Middle East, Americas · UN, Asia-Pacific, Africa. Every brief has a place tag and a source.
- **Sport band (35–44).**
- **Date check:** a box listing the stories left out because they happened on Friday 20 November.

Every story, with its links, is listed in [SOURCES.md](SOURCES.md).

## Run
```
MAKEFUN_OUTPUT_DIR=./out python3 main.py      # or: MAKEFUN_OUTPUT_DIR=./out node main.ts
```
Without `MAKEFUN_OUTPUT_DIR` the program writes `/output/entry.png`. It uses only the standard library, with no network access, no clock and no randomness, so every run gives byte-identical output.

## Build
`tools/build.py` generates `poster/index.html` from the story data. Numbers are assigned automatically and checked, so the map pins and the text always agree. `tools/render.sh` then renders the page to `entry.png` with headless Chromium. All lettering is real typeset text (Noto Sans, SIL OFL). The page contains no photos.
