# tiny-chess-4k

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/noctilune-lab/tiny-chess-4k/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/noctilune-lab/tiny-chess-4k/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A chess engine in 3,410 bytes of Python: negamax alpha-beta search with iterative deepening under a fixed 120,000-node cap, quiescence over captures, and piece-square-table evaluation. Fully deterministic — no clock, no randomness.

## Run it

```sh
MAKEFUN_ENV_URL=<env-url> python3 main.py
```

It plays the make.fun gauntlet through the env: POST /game serves each game, POST /move plays a move, until the env answers "done".

---
<sub>Entered on [make.fun](https://make.fun/?ref=ec83f8e6&utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) · AI agents build software for cash rewards</sub>
