# Saturday Finale — 21 November 2026

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Poorya0128/news-image-20261121-v2/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Poorya0128/news-image-20261121-v2/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

One 1024×1024 newspaper front page summing up **Saturday 21 November 2026**: 35 stories from 8 regions, three lead cards (tankers off Oman, COP31 overtime, the 'El Chapo Isidro' seizure), ten small cards, a world-in-time strip, world-in-numbers figures, a world map with story pins, a DATE CHECK box that keeps Friday's news out, and the numbered briefs 14–35. Every illustration is an original Pillow drawing, not a photo.

## Run it

```
python3 main.py
```

That copies the committed `entry.png` to `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR`). Standard library only. It verifies the image (real PNG, 1024×1024, within 1 MiB) before shipping it, and reads the delivered file back to confirm the copy is byte-identical.

## Rebuild the page

```
pip install pillow
python3 build.py
```

`build.py` draws `entry.png` with Pillow. It is deterministic: two runs write identical bytes.

## Files

- `build.py` draws `entry.png` with Pillow: `pip install pillow && python build.py`.
- `main.py` copies `entry.png` to `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR`). Standard library only.
- `entry.png` is the finished front page itself.
- `data/land.json` holds the simplified map outlines.

---

*Entry for the [news-image-20261121 bounty](https://make.fun/bounty/news-image-20261121) — sum up 21 November's world news in one image. Built with [make.fun](https://make.fun/r/yp1rdj4t).*
