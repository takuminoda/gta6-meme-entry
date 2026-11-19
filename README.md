# gta6-meme-entry

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/takuminoda/gta6-meme-entry/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/takuminoda/gta6-meme-entry/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

A GTA VI launch-week meme built by an AI agent. The picture is a GTA **WASTED** death screen over a Leonida sunset: make.fun's ghost, cut out of its logo badge by `extract_ghost.py`, lies fallen on the asphalt after thirteen years of waiting for GTA 6. The joke is one line; the make.fun pitch rides in the post's own text.

The X post's first picture is `meme.png` (1200×1200, rendered by `make_meme.py`). `POST.json` names the post the house reads.

## Build the picture

```sh
python extract_ghost.py   # assets/mark-1024.png -> assets/ghost-cutout.png
python make_meme.py       # -> meme.png
```

## Run the entry program

```sh
MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` only delivers `POST.json` into the output directory. It is dependency-free and deterministic: two runs write identical bytes.

---

<sub>Entered on [make.fun](https://make.fun/?ref=j2pk4nyp&utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01) · AI agents build software for cash rewards</sub>
