import ctypes
import os
import shutil

import numpy as np

from src.board import GameBoard


class TerminalInterface:
    previous_line = "\033[F"
    clear_line = "\033[K"

    def __init__(self):
        self.columns, self.lines = shutil.get_terminal_size(fallback=(80, 12))
        self.clear_terminal()
        self.padding = "  "

        if os.name == "nt":  # 'nt' is the value for Windows
            # enables use of ANSI escape characters in Windows terminal
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

    def clear_terminal(self):
        for i in range(self.lines):
            print(self.previous_line, flush=True, end="")
            print(self.clear_line, flush=True, end="")

    def print_game_board(self, board: GameBoard):
        if board.width * (1 + len(self.padding)) - len(self.padding) > self.columns or board.height > self.lines:
            raise ValueError(
                "The board is too big to be displayed on the current terminal session."
            )
        grid = board.grid
        # the alternative was originally '□', but this looks considerably cleaner
        vect = np.vectorize(lambda cell: "■" if cell else " ")

        print(self.previous_line * self.lines, flush=True, end="")

        grid = vect(grid)
        for r in grid.T:
            print(self.padding.join(r))

    @property
    def max_board_size(self) -> tuple[int, int]:
        pad = len(self.padding)
        columns = (self.columns + pad) // (1 + pad)  # adjust for padding between cells
        rows = self.lines - 1  # last line is reserved for the cursor
        return columns, rows


if __name__ == "__main__":
    from time import sleep

    g = GameBoard(5, 5)
    g.grid = np.array(
        [
            [False, False, False, False, False],
            [False, False, True, False, False],
            [False, False, True, False, False],
            [False, False, True, False, False],
            [False, False, False, False, False],
        ]
    )

    t = TerminalInterface()
    for _ in range(5):
        t.print_game_board(g)
        g.update()
        sleep(0.5)
