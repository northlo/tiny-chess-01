# tiny-chess-01

A chess engine in 4 KB of Python: negamax alpha-beta with a transposition
table, killer moves, quiescence search and piece-square evaluation, playing
the house gauntlet through the env at MAKEFUN_ENV_URL.

`main.py` is the entrypoint, packed from the readable `engine.py` with
`node cli/makefun.mjs compress` (see the kit). It uses only the Python
standard library, searches under a wall-clock budget (hard cap 6s a move,
no new depth after 1.2s), and makes no model calls.

License: MIT. See LICENSE.
