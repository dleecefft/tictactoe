"""A computer opponent that plays the game out to the end.

Noughts and crosses is small enough to search exhaustively, so there is no
heuristic here and nothing to tune. Perfect play draws against perfect play,
which means this opponent never loses: the best a player can do is hold it.
"""

from functools import lru_cache

from .board import EMPTY
from .game import InvalidMove, available, opponent, place, winner


def best_move(board, mark):
    """Return the cell `mark` should take.

    Ties are broken by board order, so the choice is the same every run.
    """
    moves = available(board)
    if not moves:
        raise InvalidMove("there is no move to make on a full board")
    return max(moves, key=lambda cell: _score(tuple(place(board, cell, mark)), mark, opponent(mark)))


@lru_cache(maxsize=None)
def _score(board, mark, to_play):
    """Score a finished or unfinished position from `mark`'s point of view.

    A win scores higher the sooner it arrives and a loss scores higher the
    longer it is put off, so the opponent takes a win on offer now rather than
    an equally certain one three moves later.
    """
    won = winner(board)
    if won is not None:
        margin = board.count(EMPTY) + 1
        return margin if won == mark else -margin

    moves = available(board)
    if not moves:
        return 0

    scores = [
        _score(tuple(place(board, cell, to_play)), mark, opponent(to_play))
        for cell in moves
    ]
    return max(scores) if to_play == mark else min(scores)
