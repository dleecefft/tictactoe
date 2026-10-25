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


@pytest.fixture(autouse=True)
def home(tmp_path, monkeypatch):
    """Point the home folder at a temporary one, so no test writes a real game log."""
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("USERPROFILE", str(tmp_path))
    return tmp_path
