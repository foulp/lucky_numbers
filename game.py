import numpy as np


BOARD_SHAPE = 4


class Tile:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def __ge__(self, other):
        return self.value >= other.value

    def __gt__(self, other):
        return self.value > other.value

    def __le__(self, other):
        return self.value <= other.value

    def __lt__(self, other):
        return self.value < other.value

    def __str__(self):
        return f"{self.value}"


class QueueTiles:
    def __init__(self, nb_players):
        self.tiles = []
        for _ in range(nb_players):
            self.tiles += [Tile(v) for v in range(1, 21)]
        np.random.shuffle(self.tiles)

    def draw_tile(self):
        return self.tiles.pop()

    def get_tiles_left(self):
        return len(self.tiles)


class Game:
    def __init__(self, nb_players=2):
        """
        Initialise lucky numbers board
        One numpy array per player, and fill the diagonal for each player with 4 sorted Tiles randomly drawn
        :param nb_players: int, from 2 to 4
        """
        assert 2 <= nb_players <= 4
        self.nb_players = nb_players
        self.boards = {i: np.array((BOARD_SHAPE, BOARD_SHAPE)) for i in range(nb_players)}
        self.queue_tiles = QueueTiles(nb_players)
        self.stock = []

        for i in range(nb_players):
            diag_tiles = [self.queue_tiles.draw_tile() for _ in range(BOARD_SHAPE)]
            diag_tiles.sort()
            np.fill_diagonal(self.boards[i], diag_tiles)

    def get_player_tile(self):
        """
        Players function to pick a tile. Either from the stock if available, otherwise from the QueueTile
        :return: Tile drawn by the player
        """
        if len(self.stock) > 0:
            while True:
                player_choice = input(
                    f"There are tiles on the stock: {self.stock}. "
                    f"If you want one, type in its value. Otherwise type 0 to draw one card."
                )
                try:
                    player_choice = int(player_choice)
                    assert 0 <= player_choice <= 20
                    assert player_choice == 0 or player_choice in self.stock
                    break
                except ValueError or AssertionError:
                    print("Please type in a number: either 0 either a tile on the stock.")
                    continue

            if player_choice in self.stock:
                return self.stock.pop(self.stock.index(player_choice))

        return self.queue_tiles.draw_tile()

    def place_player_tile(self, i, tile):
        """
        Place the tile
        :param i: index of the player
        :param tile: Tile drawn by the player
        :return: None
        """
        print(self.boards[i])
        index = input(f"This is your board. Where do you wanna place your tile {tile}?. Please type as (x,y).")
        

