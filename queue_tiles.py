import random
from collections import deque
from tile import Tile


class QueueTiles:
    """
    Class to represent to deck of Tiles to be drawn
    Has one Tile of each value (from 1 to nb_tiles) per player
    Is randomly shuffled at the beginning of the game
    """
    def __init__(self, nb_players: int, nb_tiles: int = 20):
        self.tiles = deque()
        for _ in range(nb_players):
            self.tiles.extend(Tile(v) for v in range(1, nb_tiles+1))
        random.shuffle(self.tiles)

    def draw_tile(self) -> Tile:
        return self.tiles.pop()

    def get_tiles_left(self) -> int:
        return len(self.tiles)
