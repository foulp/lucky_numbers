from queue_tiles import QueueTiles
from tile import Tile
import numpy as np


class Board:
    def __init__(self, board_size: int, default_value: int = -1):
        self.board = np.array([[Tile(default_value) for _ in range(board_size)] for _ in range(board_size)])
        self.default_value = Tile(default_value)

    def init_diagonal(self, queue_tiles: QueueTiles) -> None:
        diag_tiles = [queue_tiles.draw_tile() for _ in range(self.board.shape[0])]
        diag_tiles.sort()
        np.fill_diagonal(self.board, diag_tiles)
        return

    def place_tile(self, tile: Tile, x: int, y: int) -> Tile:
        previous_tile = self.board[x, y]
        self.board[x, y] = tile
        return previous_tile

    def is_valid(self) -> bool:
        """
        Function to check of the board is correct : all rows and columns are strictly increasing
        :return: bool
        """
        for i in range(self.board.shape[0]):
            if any(np.diff(self.board[i][self.board[i] != self.default_value]) <= 0):
                return False
            if any(np.diff(self.board[:, i][self.board[:, i] != self.default_value]) <= 0):
                return False
        return True

    def is_valid_spot(self, tile: Tile, x: int, y: int) -> bool:
        """
        Function to check if tile can be correctly placed in (x, y)
        :param tile: Tile to be placed
        :param x: int
        :param y: int
        :return: bool
        """
        previous_tile = self.place_tile(tile, x, y)
        valid = self.is_valid()
        self.place_tile(previous_tile, x, y)
        return valid

    def is_ended(self) -> bool:
        if (self.board == self.default_value).sum() == 0:
            return True
        return False
