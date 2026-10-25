from tictactoe.cli import main, verdict


def scripted(monkeypatch, answers):
    """Answer every input() prompt from `answers`, in order."""
    replies = iter(answers)
    monkeypatch.setattr("builtins.input", lambda _prompt="": next(replies))


def test_a_two_player_game_runs_to_a_win(monkeypatch, capsys):
    scripted(monkeypatch, ["1", "4", "2", "5", "3"])
    assert main(["--two-player"]) == 0
    assert "X wins." in capsys.readouterr().out


def test_a_game_against_the_computer_finishes(monkeypatch, capsys):
    scripted(monkeypatch, [str(cell) for cell in range(1, 10)])
    assert main([]) == 0
    printed = capsys.readouterr().out
    assert "The computer plays" in printed
    assert "X wins." in printed or "O wins." in printed or "A draw." in printed


def test_quitting_abandons_the_game(monkeypatch, capsys):
    scripted(monkeypatch, ["q"])
    assert main(["--two-player"]) == 1
    assert "abandoned" in capsys.readouterr().out


def test_the_end_of_the_input_abandons_the_game(monkeypatch, capsys):
    def stop(_prompt=""):
        raise EOFError

    monkeypatch.setattr("builtins.input", stop)
    assert main(["--two-player"]) == 1
    assert "abandoned" in capsys.readouterr().out


def test_a_cell_that_is_not_a_number_is_asked_again(monkeypatch, capsys):
    scripted(monkeypatch, ["middle", "1", "4", "2", "5", "3"])
    assert main(["--two-player"]) == 0
    printed = capsys.readouterr().out
    assert "Type a cell number" in printed
    assert "X wins." in printed


def test_a_cell_that_is_taken_is_asked_again(monkeypatch, capsys):
    scripted(monkeypatch, ["1", "1", "4", "2", "5", "3"])
    assert main(["--two-player"]) == 0
    printed = capsys.readouterr().out
    assert "is not free" in printed
    assert "X wins." in printed


def test_the_verdict_reads_as_a_draw(board_from):
    assert verdict(board_from("XOX XOO OXX")) == "A draw."
