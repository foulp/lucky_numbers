from queue_tiles import QueueTiles
from tile import Tile
import numpy as np


class Board:
    def __init__(self, board_size: int, default_value: int = -1):
        self.board: np.ndarray = default_value * np.ones((board_size, board_size), dtype=int)
        self.default_value = default_value

    def place_tile(self, tile: Tile, x: int, y: int):
        try:
            assert 0 <= x < self.board.shape[0]
            assert 0 <= y < self.board.shape[1]
        except AssertionError:
            print(f"X and Y must be respectively between 0 and {self.board.shape} excluded")
            return False, None

        previous_tile: int = self.board[x, y]
        self.board[x, y] = tile.value
        if self.is_valid():
            if previous_tile == -1:
                return True, None
            return True, previous_tile
        self.board[x, y] = previous_tile
        print(f"Location is not valid, rows and/or columns are not stricly increasing")
        return False, None

    def is_valid(self):
        for i in range(self.board.shape[0]):
            if any(np.diff(self.board[i][self.board[i] != self.default_value]) <= 0):
                return False
            if any(np.diff(self.board[:, i][self.board[:, i] != self.default_value]) <= 0):
                return False
        return True

    def is_ended(self):
        if (self.board == self.default_value).sum() == 0:
            return True
        return False

    def init_diagonal(self, queue_tiles: QueueTiles):
        diag_tiles: list[Tile] = [queue_tiles.draw_tile().value for _ in range(self.board.shape[0])]
        diag_tiles.sort()
        np.fill_diagonal(self.board, diag_tiles)
