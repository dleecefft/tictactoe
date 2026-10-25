# tictactoe

Noughts and crosses in the terminal. Four modules of a few dozen lines each, a complete
test suite, and an opponent that never loses. Small enough to read in one sitting, which
is the point: everything here is meant to stay readable.

## Conventions, already argued about

- **No dependencies.** The standard library only. `pytest` is a development extra and
  nothing else may be added without a decision.
- **A board is a flat list of nine cells**, read left to right and top to bottom, so a
  winning line is a tuple of three indices. Nothing anywhere holds a list of rows.
- **`place()` returns a new board and leaves the one it was given alone.** The copy on
  every call is deliberate, not an oversight: it is what lets the opponent search ahead
  without an undo stack. Do not replace it with a mutate-and-restore.
- **`_score` is cached without a bound on purpose.** The whole game tree fits in memory
  and a process plays a handful of games, so `lru_cache(maxsize=None)` is the cheapest
  correct thing here. It is not a leak.
- **Only `cli.py` talks to the person.** It is the one module that calls `print()` or
  `input()`, and the one module that turns a cell index into the number on screen. Cells
  are zero based everywhere inside the package and one based only where they are shown.
- **Only `cli.py` touches the filesystem**, and only through a path the person chose. The
  rest of the package computes and returns; it does not read, write, or reach outside the
  process.

## Testing

- pytest, from the repository root. Tests live in `tests/`, named for the behaviour they
  pin rather than for the function they call.
- A change to a rule ships with a test at its boundary, not only in its middle. The
  boundary is where the rules disagree: a full board, a drawn game, a cell already taken.
- A test earns its place when it fails if the behaviour changes. One that restates the
  implementation does not.
- Board fixtures live in `tests/conftest.py`. `board_from` builds a position from a
  three line sketch, so reuse it rather than writing a nine element list inline.

## Review

@.claude/rules/review-criteria.md
