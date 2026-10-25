import pytest

from tictactoe.board import LINES, O, X, new_board
from tictactoe.game import (
    InvalidMove,
    available,
    current_mark,
    is_full,
    is_over,
    opponent,
    outcome,
    place,
    winner,
)


def test_x_opens():
    assert current_mark(new_board()) == X


def test_the_turn_alternates(board_from):
    assert current_mark(board_from("X.. ... ...")) == O
    assert current_mark(board_from("XO. ... ...")) == X


def test_opponent_is_the_other_mark():
    assert opponent(X) == O
    assert opponent(O) == X


def test_place_leaves_the_board_it_was_given_alone():
    board = new_board()
    place(board, 0, X)
    assert board == new_board()


def test_place_writes_the_mark(board_from):
    assert place(new_board(), 4, X) == board_from("... .X. ...")


def test_place_rejects_a_taken_cell(board_from):
    with pytest.raises(InvalidMove, match="already taken"):
        place(board_from("X.. ... ..."), 0, O)


@pytest.mark.parametrize("cell", [-1, 9, 99])
def test_place_rejects_a_cell_off_the_board(cell):
    with pytest.raises(InvalidMove, match="outside the board"):
        place(new_board(), cell, X)


def test_place_rejects_a_mark_that_is_not_playable():
    with pytest.raises(InvalidMove, match="not a playable mark"):
        place(new_board(), 0, "Z")


def test_available_lists_the_free_cells_in_order(board_from):
    assert available(board_from("XO. ..X ..O")) == [2, 3, 4, 6, 7]


@pytest.mark.parametrize("line", LINES)
def test_winner_finds_every_line(line):
    board = new_board()
    for cell in line:
        board[cell] = X
    assert winner(board) == X


def test_winner_ignores_a_line_that_is_shared(board_from):
    assert winner(board_from("XOX ... ...")) is None


def test_an_empty_board_has_no_winner():
    assert winner(new_board()) is None


def test_a_full_board_with_no_line_is_a_draw(board_from):
    board = board_from("XOX XOO OXX")
    assert is_full(board)
    assert winner(board) is None
    assert outcome(board) == "draw"


def test_a_game_is_over_once_it_is_won(board_from):
    board = board_from("XXX OO. ...")
    assert not is_full(board)
    assert is_over(board)
    assert outcome(board) == X


def test_a_game_in_play_has_no_outcome(board_from):
    board = board_from("XO. ... ...")
    assert not is_over(board)
    assert outcome(board) is None
