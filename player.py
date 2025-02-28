from board import Board
from queue_tiles import QueueTiles
from tile import Tile


class Player:
    def __init__(self, index: int, board_size: int):
        self.index: int = index
        self.board: Board = Board(board_size)
        self.tiles = 0

    @staticmethod
    def pick_tile(queue_tiles: QueueTiles, stock: list[int]):
        """
        Players function to pick a tile. Either from the stock if available, otherwise from the QueueTile
        :return: Tile drawn by the player
        """
        if len(stock) > 0:
            while True:
                player_choice: str = input(
                    f"There are tiles on the stock: {stock}. "
                    f"If you want one, type in its value. Otherwise type 0 to draw one tile."
                )
                try:
                    player_choice: int = int(player_choice)
                    assert 0 <= player_choice <= 20
                    assert player_choice == 0 or player_choice in stock
                    break
                except ValueError:
                    print("Please type in a number: either 0 either a tile on the stock.")
                    continue
                except AssertionError:
                    print("Please type either 0 either a tile on the stock.")

            if player_choice in stock:
                tile_to_remove: int = player_choice
                return Tile(stock.pop(stock.index(tile_to_remove)))
        else:
            print("There are no tiles on the stock.")
        return queue_tiles.draw_tile()

    def place_tile(self, tile: Tile):
        """
        Place the tile
        :param tile: Tile drawn by the player
        :return: int, the input tile's value if discarded, the exchange tile's value or None if no tile was removed
        """
        while True:
            try:
                index = input(f"Where do you wanna place your tile {tile}?. Please type as: x,y. Or 0 to discard.\n")
                if index == "0":
                    return tile.value
                x, y = map(int, index.split(','))
            except ValueError:
                print("Invalid input.")
                continue
            r, changed_tile = self.board.place_tile(tile, x, y)
            if r:
                self.tiles += 1
                break
        if changed_tile:
            self.tiles -= 1
        return changed_tile
