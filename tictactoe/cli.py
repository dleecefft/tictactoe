"""The terminal game."""

import argparse

from .ai import best_move
from .board import CELLS, O, X, new_board, render
from .game import available, current_mark, is_over, place, winner


def main(argv=None):
    """Play a game and return the exit status."""
    parser = argparse.ArgumentParser(
        prog="tictactoe",
        description="Play noughts and crosses in the terminal.",
    )
    parser.add_argument(
        "--two-player",
        action="store_true",
        help="play against another person rather than the computer",
    )
    parser.add_argument(
        "--mark",
        choices=[X, O],
        default=X,
        help="the mark you play against the computer, X opening (default: X)",
    )
    args = parser.parse_args(argv)

    board = new_board()
    print(render(board), end="\n\n")

    while not is_over(board):
        mark = current_mark(board)
        if args.two_player or mark == args.mark:
            cell = ask(board, mark)
            if cell is None:
                print("\nGame abandoned.")
                return 1
        else:
            cell = best_move(board, mark)
            print(f"The computer plays {mark} in cell {cell + 1}.")
        board = place(board, cell, mark)
        print(render(board), end="\n\n")

    print(verdict(board))
    return 0


def ask(board, mark):
    """Read a legal cell from the player, or None if they are done.

    Anything that is not a free cell is answered and asked again, so a typo
    costs a line rather than the game.
    """
    free = ", ".join(str(cell + 1) for cell in available(board))
    while True:
        try:
            answer = input(f"{mark} plays which cell? ").strip()
        except (EOFError, KeyboardInterrupt):
            return None

        if answer.lower() in ("q", "quit"):
            return None

        try:
            cell = int(answer) - 1
        except ValueError:
            print(f"Type a cell number from 1 to {CELLS}, or q to give up.")
            continue

        if cell not in available(board):
            print(f"Cell {answer} is not free. Free cells: {free}.")
            continue

        return cell


def verdict(board):
    """Return the closing line for a finished game."""
    won = winner(board)
    return f"{won} wins." if won is not None else "A draw."
