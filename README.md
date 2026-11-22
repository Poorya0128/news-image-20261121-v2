# The One-Day World: Saturday 21 November 2026

This is an entry for make.fun's "Sum up 21 November's world news in one image" bounty (`news-image-20261121`). It is one 1024×1024 newspaper front page covering 10 numbered stories, plus 4 briefs, from Saturday 21 November 2026.

![entry](entry.png)

## What is on the page
- **Lead (1):** Drones set the Russian cargo ship Sparta II ablaze off Finland, with an illustration drawn in code.
- **World map:** numbered pins 1–10 that match the numbered story cards. Mercury (story 6) gets its own inset.
- **Nine story cards:** Sinaloa, Hormuz, Geneva, COP31, BepiColombo, Banda Sea quake, France, Gaza, FBI hack. Each card has a region tag, an icon, a headline, a short summary and its sources.
- **"Also on Saturday" strip:** Kyiv, the Premier League, the F1 Las Vegas GP, and Egypt's Aswan Forum.

All facts and the source for each story are listed in [SOURCES.md](SOURCES.md). Stories that happened on Friday 20 November were left out on purpose.

## Run it
```
MAKEFUN_OUTPUT_DIR=./out python3 main.py      # or: MAKEFUN_OUTPUT_DIR=./out node main.ts
```
Without `MAKEFUN_OUTPUT_DIR` it writes `/output/entry.png`. The program uses only the standard library. It has no network access, no clock and no randomness, so two runs give byte-identical output.

## How the image is built
`poster/index.html` (HTML, CSS and hand-written SVG, using the bundled Noto Sans fonts under the SIL OFL) is rendered with headless Chromium by `tools/render.sh` into `entry.png`. All lettering is real typeset text, so nothing is garbled. The page contains no photos or copied images.
