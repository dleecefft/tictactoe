"""The rules: who plays next, what a legal move is, and when it is over."""

from .board import CELLS, EMPTY, LINES, O, X


class InvalidMove(ValueError):
    """Raised when a move cannot be played on the board it was given."""


def opponent(mark):
    """Return the other mark."""
    return O if mark == X else X


def current_mark(board):
    """Return the mark to play next.

    X always opens, so the counts alone decide whose turn it is and a board
    carries no separate turn counter.
    """
    return X if board.count(X) == board.count(O) else O


def available(board):
    """Return the indices of the cells still free, in board order."""
    return [index for index, cell in enumerate(board) if cell == EMPTY]


def place(board, cell, mark):
    """Return a new board with `mark` written into `cell`.

    The board passed in is left alone, which is what lets the computer opponent
    look ahead without having to undo anything.
    """
    if mark not in (X, O):
        raise InvalidMove(f"{mark!r} is not a playable mark")
    if not 0 <= cell < CELLS:
        raise InvalidMove(f"cell {cell} is outside the board")
    if board[cell] != EMPTY:
        raise InvalidMove(f"cell {cell} is already taken by {board[cell]}")
    played = list(board)
    played[cell] = mark
    return played


def winner(board):
    """Return the mark holding a complete line, or None if neither does."""
    for line in LINES:
        first = board[line[0]]
        if first != EMPTY and all(board[cell] == first for cell in line):
            return first
    return None


def is_full(board):
    """Return True when no cell is free."""
    return EMPTY not in board


def is_over(board):
    """Return True when the game has been won or the board has filled up."""
    return winner(board) is not None or is_full(board)


def outcome(board):
    """Return the winning mark, the string "draw", or None while play continues."""
    won = winner(board)
    if won is not None:
        return won
    return "draw" if is_full(board) else None
