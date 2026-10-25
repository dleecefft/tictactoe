# tictactoe

Noughts and crosses in the terminal: a small, readable Python package with a
complete test suite and an opponent that never loses.

It is deliberately plain. No dependencies, no framework, four modules of a few
dozen lines each, and every rule of the game in one place.

## Play

```bash
uv run python -m tictactoe
```

Or, without uv:

```bash
python -m tictactoe
```

The free cells are numbered, so you type the number of the cell you want:

```
 1 | 2 | 3
---+---+---
 4 | 5 | 6
---+---+---
 7 | 8 | 9
```

X always opens. Type `q` to give up.

| Option | What it does |
|---|---|
| (none) | You play X against the computer |
| `--mark O` | You play O, the computer opens as X |
| `--two-player` | Two people at the same keyboard, no computer |
| `--player NAME` | The name recorded in the game log (default: `player`) |
| `--log PATH` | Where finished games are appended (default: `~/.tictactoe/games.log`) |

The computer searches the game out to the end rather than guessing, so it will
never lose. A draw against it is a win.

Each finished game, win or draw, appends one line to the log. An abandoned game
is not logged. Cells are numbered as on the board, in the order they were played:

```
player=Ada outcome=X cells=1,4,2,5,3
```

## Tests

```bash
uv run --extra dev pytest
```

Or, with pytest already installed:

```bash
python -m pytest
```

Sixty-one tests, well under a second. They cover the board, every winning line,
the legality of a move, the opponent and the terminal loop.

## Layout

| File | What lives there |
|---|---|
| `tictactoe/board.py` | How a board is represented and drawn, and the eight winning lines |
| `tictactoe/game.py` | The rules: whose turn it is, what a legal move is, who has won |
| `tictactoe/ai.py` | The computer opponent, a full search with the results memoised |
| `tictactoe/cli.py` | The terminal game: the prompt, the loop and the verdict |
| `tests/` | One file per module, plus a fixture that builds a board from a sketch |

A board is a flat list of nine cells read left to right and top to bottom, so a
winning line is a tuple of three indices. `place` returns a new board rather
than editing the one it was given, which is what lets the opponent look ahead
without having to undo anything.

## Using this as a template

Press **Use this template** on GitHub to get your own copy, then rename the
package in `pyproject.toml` and `tictactoe/` if you want it called something
else.

## Licence

MIT. See `LICENSE`.
