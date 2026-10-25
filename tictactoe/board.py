"""The board: how a game is represented, and how it is drawn.

A board is a flat sequence of nine cells, read left to right and top to bottom,
so cell 0 is the top left corner and cell 8 is the bottom right. Keeping it flat
means a winning line is just a tuple of three indices.
"""

EMPTY = " "
X = "X"
O = "O"

SIZE = 3
CELLS = SIZE * SIZE

ROWS = tuple(tuple(row * SIZE + column for column in range(SIZE)) for row in range(SIZE))
COLUMNS = tuple(tuple(row * SIZE + column for row in range(SIZE)) for column in range(SIZE))
DIAGONALS = (
    tuple(step * SIZE + step for step in range(SIZE)),
    tuple(step * SIZE + (SIZE - 1 - step) for step in range(SIZE)),
)

#: Every line that wins the game: three rows, three columns, two diagonals.
LINES = ROWS + COLUMNS + DIAGONALS


def new_board():
    """Return an empty board."""
    return [EMPTY] * CELLS


def render(board, numbered=True):
    """Return the board as printable text.

    With `numbered` left on, an empty cell shows the number a player types to
    claim it, counting from 1 so the keypad matches the grid. Turn it off for a
    plain picture of the position.
    """
    cells = [
        cell if cell != EMPTY else (str(index + 1) if numbered else EMPTY)
        for index, cell in enumerate(board)
    ]
    rows = [
        " " + " | ".join(cells[row * SIZE:(row + 1) * SIZE]) + " "
        for row in range(SIZE)
    ]
    separator = "\n" + "+".join(["---"] * SIZE) + "\n"
    return separator.join(rows)
