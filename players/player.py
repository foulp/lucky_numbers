from typing import Optional
from typing_extensions import Self

from game_elements.board import Board
from game_elements.queue_tiles import QueueTiles
from game_elements.tile import Tile


class Player:
    def __init__(self, index: int, board_size: int, verbose: bool = True):
        self.index: int = index
        self.board: Board = Board(board_size)
        self.tiles: int = 0
        self.verbose: bool = verbose

    def play_turn(self, queue_tiles: QueueTiles, stock: list[Tile], opponents: dict[int: Self]) -> Tile:
        """
        Player turn.
        First, player can select a Tile from the stock, if not empty.
        Loop until a tile selected from stock is correctly placed or player chooses to draw a tile.
        Then, if no tile from the stock was correctly placed, a tile is drawn and placed or discarded
        :param queue_tiles:
        :param stock:
        :param opponents:
        :return: Tile, the discarded tile or the exchanged tile
        """
        if self.verbose:
            print(f"Player {self.index}, it's your turn.")
            print(f"This is your board:\n{self.board.board}")
            print(f"These are other players' boards:")
            for i in opponents:
                if i != self.index:
                    print(f"Player {i}")
                    print(opponents[i].board.board)

        if len(stock):
            tried_tiles = []
            while True:
                picked_tile = self._pick_tile_from_stock(stock)
                if picked_tile == self.board.default_value:
                    stock.extend(tried_tiles)
                    stock.sort()
                    break
                exchanged_tile = self._place_stocked_tile(picked_tile)
                if exchanged_tile != picked_tile:
                    stock.extend(tried_tiles)
                    stock.sort()
                    return exchanged_tile
                else:
                    tried_tiles.append(picked_tile)

                if len(stock) == 0:
                    stock.extend(tried_tiles)
                    stock.sort()
                    break

        drawn_tile = queue_tiles.draw_tile()
        return self._place_drawn_tile(drawn_tile)

    def _pick_tile_from_stock(self, stock: list[Tile]) -> Tile:
        """
        Players function to pick a tile from the stock.
        :return: Tile chosen by the player, Tile(default_value) if no tile was picked
        """
        if self.verbose:
            print(f"These are the tiles on the stock: {stock}.")
        while True:
            player_choice = input(f"If you want one, type its value. Otherwise type 0 to draw one tile.\n")
            try:
                player_choice = Tile(int(player_choice))
                assert 0 <= player_choice <= 20
                assert player_choice == 0 or player_choice in stock
                break
            except ValueError:
                print("Please type in a number: either 0 either a tile on the stock.")
                continue
            except AssertionError:
                print("Please type either 0 either a tile on the stock.")

        if player_choice in stock:
            return stock.pop(stock.index(player_choice))
        else:
            return Tile(self.board.default_value)

    def _place_tile(self, tile: Tile, x: int, y: int) -> (bool, Optional[Tile]):
        """
        Function to attempt to place the tile on the board.
        :param tile:
        :param x:
        :param y:
        :return: (bool, Tile), if bool is True, return the exchanged tile too, else None
        """
        if self.board.is_valid_spot(tile, x, y):
            previous_tile = self.board.place_tile(tile, x, y)
            if previous_tile == -1:
                self.tiles += 1
            if self.verbose:
                print(f"You placed you tile {tile} on ({x},{y}) and exchanged it with {previous_tile}")
            return True, previous_tile
        else:
            if self.verbose:
                print(
                    f"Location ({x},{y}) is not valid, rows and/or columns are not strictly increasing. "
                    f"Please retry."
                )
            return False, None

    def _place_stocked_tile(self, tile: Tile) -> Tile:
        """
        Place the tile picked from the stock
        :param tile: Tile picked by the player
        :return: Tile, the input tile if finally the player wants to draw a tile, the exchanged tile otherwise
        """
        while True:
            try:
                index = input(
                    f"Where do you wanna place your tile {tile}?. Please type as: x,y. "
                    f"Or 0 to select another tile from the stock.\n")
                if index == "0":
                    return tile
                x, y = map(int, index.split(','))
            except ValueError:
                print("Invalid input.")
                continue

            spot_correct, exchanged_tile = self._place_tile(tile, x, y)
            if spot_correct:
                return exchanged_tile

    def _place_drawn_tile(self, tile: Tile) -> Tile:
        """
        Place the tile drawn from the queue_tiles
        :param tile: Tile drawn by the player
        :return: Tile, the input tile if discarded, the exchanged tile otherwise
        """
        while True:
            try:
                index = input(f"Where do you wanna place your tile {tile}?. Please type as: x,y. Or 0 to discard.\n")
                if index == "0":
                    return tile
                x, y = map(int, index.split(','))
            except ValueError:
                print("Invalid input.")
                continue

            spot_correct, exchanged_tile = self._place_tile(tile, x, y)
            if spot_correct:
                return exchanged_tile
