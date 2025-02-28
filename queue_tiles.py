import random
from collections import deque
from tile import Tile


class QueueTiles:
    def __init__(self, nb_players: int):
        self.tiles: deque[Tile] = deque()
        for _ in range(nb_players):
            self.tiles.extend(Tile(v) for v in range(1, 21))
        random.shuffle(self.tiles)

    def draw_tile(self):
        return self.tiles.pop()

    def get_tiles_left(self):
        return len(self.tiles)
