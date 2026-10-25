import pytest

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


def test_a_finished_game_is_appended_to_the_log(monkeypatch, tmp_path):
    log = tmp_path / "games.log"
    scripted(monkeypatch, ["1", "4", "2", "5", "3"])
    assert main(["--two-player", "--log", str(log), "--player", "Ada"]) == 0
    assert log.read_text() == "player=Ada outcome=X cells=1,4,2,5,3\n"


def test_a_drawn_game_is_logged_as_a_draw(monkeypatch, tmp_path):
    log = tmp_path / "games.log"
    scripted(monkeypatch, ["1", "2", "3", "5", "4", "6", "8", "7", "9"])
    assert main(["--two-player", "--log", str(log)]) == 0
    assert log.read_text() == "player=player outcome=draw cells=1,2,3,5,4,6,8,7,9\n"


def test_an_abandoned_game_is_not_logged(monkeypatch, tmp_path):
    log = tmp_path / "games.log"
    scripted(monkeypatch, ["1", "q"])
    assert main(["--two-player", "--log", str(log)]) == 1
    assert not log.exists()


def test_each_game_adds_a_line_to_the_log(monkeypatch, tmp_path):
    log = tmp_path / "games.log"
    scripted(monkeypatch, ["1", "4", "2", "5", "3"])
    main(["--two-player", "--log", str(log)])
    scripted(monkeypatch, ["1", "2", "3", "5", "4", "6", "8", "7", "9"])
    main(["--two-player", "--log", str(log)])
    assert len(log.read_text().splitlines()) == 2


def test_the_log_defaults_to_the_games_file_in_the_home_folder(monkeypatch, home):
    scripted(monkeypatch, ["1", "4", "2", "5", "3"])
    main(["--two-player"])
    assert (home / ".tictactoe" / "games.log").exists()


def test_the_computer_moves_are_logged_with_the_players(monkeypatch, tmp_path, capsys):
    log = tmp_path / "games.log"
    scripted(monkeypatch, [str(cell) for cell in range(1, 10)])
    main(["--log", str(log)])
    announced = [
        int(line.split("cell ")[1].rstrip("."))
        for line in capsys.readouterr().out.splitlines()
        if line.startswith("The computer plays")
    ]
    cells = [int(cell) for cell in log.read_text().split("cells=")[1].split(",")]
    assert len(set(cells)) == len(cells)
    assert set(announced) <= set(cells)


def test_a_name_that_would_break_the_log_line_is_refused(monkeypatch, capsys):
    with pytest.raises(SystemExit) as refused:
        main(["--two-player", "--player", "Ada\nouter"])
    assert refused.value.code == 2
    assert "a name must be" in capsys.readouterr().err


def test_a_blank_name_is_refused(monkeypatch, capsys):
    with pytest.raises(SystemExit):
        main(["--two-player", "--player", "   "])
    assert "a name must be" in capsys.readouterr().err


def test_a_log_that_cannot_be_written_does_not_change_the_game(monkeypatch, tmp_path, capsys):
    scripted(monkeypatch, ["1", "4", "2", "5", "3"])
    assert main(["--two-player", "--log", str(tmp_path)]) == 0
    captured = capsys.readouterr()
    assert "X wins." in captured.out
    assert "Could not write the game log" in captured.err
