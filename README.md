# news-image-20261125

Sum up Wednesday 25 November 2026's world news in one image.

`main.py` (Python 3, standard library only, no network) draws a 1024x1024
PNG newspaper front page and writes it to `$MAKEFUN_OUTPUT_DIR/entry.png`
(default `/output/entry.png`). It is deterministic: two runs produce
identical bytes.

## What's on the page

- Masthead: "THE WORLD IN ONE IMAGE — WEDNESDAY 25 NOVEMBER 2026 — 42 STORIES — 7 REGIONS"
- 8 drawn vector scenes: Shenzhou-24 docking at Tiangong, the Saudi-led
  strike on Hodeidah port, Asia's chip sell-off, the Solomon Islands–
  Australia treaty, the Abu Dhabi talks, the Huawei verdict, the Turkish
  helicopter crash, and Gukesh holding Sindarov in the world chess title.
- A world map with 10 numbered story markers and a "stories by region" bar
  chart (Asia 12, Middle East 4, Europe 8, Africa 4, Americas 7, Oceania 4,
  World 3).
- "The Day in Brief": 34 more dated stories across 7 regions.
- Sources footnote. Stories from Tuesday 24 Nov or Monday 23 Nov are
  labelled with their day; market moves are intraday figures, not closes.

## Run

```sh
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
```

## Entry

make.fun competition `news-image-20261125`. Prize $100 in USDC shared by
the top 50 places. Entries close 2026-11-27T00:00:00Z.

## License

MIT — see `LICENSE`.
