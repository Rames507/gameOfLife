import random

import numpy as np


class GameBoard:
    def __init__(self, width: int, height: int, random_: float = 0.0):
        self.width = width
        self.height = height

        self.grid = np.array(
            [random.random() < random_ for _ in range(self.width * self.height)],
            dtype=bool,
        )
        self.grid = self.grid.reshape((self.width, self.height))
        pass

    def __str__(self):
        vect = np.vectorize(lambda cell: "■" if cell else "□")
        return str(vect(self.grid))

    def get_neighbors(self, x_cord, y_cord) -> list[bool]:
        for x in range(x_cord - 1, x_cord + 2):
            for y in range(y_cord - 1, y_cord + 2):
                if x == x_cord and y == y_cord:
                    continue
                yield self.grid[x % self.width, y % self.height]

    def get_alive_neighbors(self, x_cord, y_cord) -> int:
        neighbors = self.get_neighbors(x_cord, y_cord)
        return sum(neighbors)

    def update(self) -> None:
        """
        Advances the board state by 1 tick
        :return: None
        """
        new_grid = self.grid.copy()
        it = np.nditer(new_grid, flags=["multi_index"])
        for cell in it:
            cell_x, cell_y = it.multi_index
            neighbors = self.get_alive_neighbors(cell_x, cell_y)
            if cell:  # cell is alive
                if neighbors < 2 or neighbors > 3:
                    new_grid[cell_x, cell_y] = False
            else:  # cell is dead
                if neighbors == 3:
                    new_grid[cell_x, cell_y] = True

        self.grid = new_grid


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

    while True:
        print(g)
        g.update()
        sleep(0.5)
