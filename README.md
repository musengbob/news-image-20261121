# THE WORLD TODAY — Saturday 21 November 2026

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/musengbob/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/musengbob/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A dense newspaper front page that sums up Saturday 21 November 2026's world
news in a single 1024×1024 image: Russian missiles landing in Poland, the
COP31 climate talks slipping into overtime in Antalya with fossil fuels
struck from the draft, and Wall Street falling into correction as the AI
sell-off deepens — plus 33 more stories from every region, a stat strip, a
world map of where it happened, and a date-check box that names the
near-miss stories from earlier in the week and leaves them out on purpose.
The image is drawn from scratch in code by `compose.py` (Pillow, flat
vector-style art, no copied images) and shipped as `entry.png`; `main.ts`
copies it to the output directory.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Files

- `entry.png` — the front page (1024×1024, ≤ 1 MiB)
- `compose.py` — draws `entry.png` from scratch (Python 3 + Pillow)
- `main.ts` — copies `entry.png` to `$MAKEFUN_OUTPUT_DIR` (defaults to `./out`)

---

<sub>Entered on [make.fun](https://make.fun/?ref=t2hmjdyt&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
