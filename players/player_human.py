from game_elements.tile import Tile
from players.player import Player


class HumanPlayer(Player):
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
