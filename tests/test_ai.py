import pytest

from tictactoe.ai import best_move
from tictactoe.board import O, X, new_board
from tictactoe.game import InvalidMove, available, current_mark, is_over, place, winner


def test_it_takes_a_win_that_is_on_offer(board_from):
    assert best_move(board_from("XX. OO. ..."), X) == 2


def test_it_blocks_a_win_that_is_on_offer(board_from):
    assert best_move(board_from("OO. X.. X.."), X) == 2


def test_the_opening_choice_is_the_same_every_run():
    """Every opening draws against perfect play, so board order settles it."""
    assert best_move(new_board(), X) == 0
    assert best_move(new_board(), X) == 0


def test_perfect_play_draws():
    board = new_board()
    while not is_over(board):
        mark = current_mark(board)
        board = place(board, best_move(board, mark), mark)
    assert winner(board) is None


@pytest.mark.parametrize("opening", range(9))
def test_it_never_loses_to_a_player_taking_the_first_free_cell(opening):
    board = place(new_board(), opening, X)
    while not is_over(board):
        mark = current_mark(board)
        cell = best_move(board, mark) if mark == O else available(board)[0]
        board = place(board, cell, mark)
    assert winner(board) != X


def test_there_is_no_move_on_a_full_board(board_from):
    with pytest.raises(InvalidMove, match="full board"):
        best_move(board_from("XOX XOO OXX"), X)
