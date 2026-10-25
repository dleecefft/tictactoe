import pytest

from tictactoe.board import CELLS, EMPTY


@pytest.fixture
def board_from():
    """Build a board from a sketch, with a dot for a free cell.

    Anything that is not a mark or a dot is ignored, so a test can lay the
    position out as three lines and read like the thing it is testing.
    """
    def build(sketch):
        cells = [character for character in sketch if character in "XO."]
        if len(cells) != CELLS:
            raise ValueError(f"a sketch needs {CELLS} cells, this one has {len(cells)}")
        return [EMPTY if cell == "." else cell for cell in cells]

    return build
