# news-image-20261125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/BrianChen33/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/BrianChen33/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

Sum up Wednesday 25 November 2026's world news in one image: a 1024x1024 newspaper front page with 42 dated, verified stories — 6 illustrated leads, 2 strip scenes, a world map with 11 numbered markers, a stories-by-region bar chart, and 34 briefs.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
```

`main.py` (Python 3; standard library plus Pillow when available for TrueType headlines, with a built-in pixel-font fallback) draws the page and writes it to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output/entry.png`). It is deterministic: two runs produce identical bytes.

## What's on the page

- Masthead: "THE WORLD IN ONE IMAGE — WEDNESDAY 25 NOVEMBER 2026 — 42 STORIES — 7 NEWS REGIONS"
- 6 illustrated leads: Shenzhou-24 docking at Tiangong (first Pakistani astronaut to visit the station), the Saudi-led coalition strike on Hodeidah port, Asia's chip sell-off (Taiwan −8.6% intraday, SoftBank −16%), the Solomon Islands–Australia security treaty, Australia's CPI jumping to 4.9%, and North Korea expelling the Swiss envoy (48 hours to leave).
- 2 strip scenes: the Turkish AS-532 helicopter crash near Eskisehir (24 Nov) and Gukesh drawing game one of the world chess title in Geneva (24 Nov).
- A world map with 11 numbered story markers (Jiuquan, Hodeidah, Taipei, Honiara, Canberra, Pyongyang, Eskisehir, Madrid, Cartagena, Geneva, Borno) and a "stories by region" bar chart (Asia 13, Middle East 3, Europe 8, Africa 3, Americas 8, Oceania 6, World 1).
- "The Day in Brief": 34 more dated stories across 7 regions, each classified by event location.
- A date key (24 Nov = Tuesday, 23 Nov = Monday, 29 Nov = election day) and a sources footnote. Stories from Tuesday 24 Nov or Monday 23 Nov are labelled with their day; market moves are intraday figures, not closes.

## Entry

make.fun competition `news-image-20261125`. Prize $100 in USDC shared by the top 50 places. Entries close 2026-11-27T00:00:00Z.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>

## License

MIT — see `LICENSE`.
