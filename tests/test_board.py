from tictactoe.board import CELLS, EMPTY, LINES, SIZE, X, new_board, render


def test_a_new_board_is_empty():
    assert new_board() == [EMPTY] * CELLS


def test_there_are_eight_winning_lines():
    assert len(LINES) == 2 * SIZE + 2
    assert len(set(LINES)) == len(LINES)


def test_every_line_covers_three_cells_on_the_board():
    for line in LINES:
        assert len(set(line)) == SIZE
        assert all(0 <= cell < CELLS for cell in line)


def test_render_numbers_the_free_cells():
    drawn = render(new_board())
    for number in range(1, CELLS + 1):
        assert str(number) in drawn


def test_render_can_leave_the_numbers_off():
    assert "1" not in render(new_board(), numbered=False)


def test_render_shows_a_mark_where_it_was_played(board_from):
    drawn = render(board_from("X.. ... ..."))
    assert drawn.splitlines()[0].strip().startswith("X")


def test_render_rows_line_up():
    widths = {len(line) for line in render(new_board()).splitlines()}
    assert len(widths) == 1
