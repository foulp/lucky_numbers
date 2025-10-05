from typing import cast

from game_elements.tile import Tile
from players.player import Player


class BotPlayer(Player):
    """
    Simple Bot: Works on the concept of target diagonal for a Tile.
    target_diag = Tile.value // 3
    We aim for target_diag = row + col
    - Draw a Tile if any Tile in stock can replace a non optimistic Tile on our board (on the sens of target diag)
    - Place to any available spot on the target diag
    - If there aren't, discard the Tile
    """

    def _pick_tile_from_stock(self, stock: list[Tile]) -> Tile:
        """
        Players function to pick a tile.
        :return: Tile drawn by the Bot
        """
        for tile in stock:
            target_diag = tile // 3
            for row in range(0, self.board.board.shape[0]):
                col = target_diag - row
                if col < 0 or col >= self.board.board.shape[1]:
                    continue
                if target_diag not in (self.board.board[row, col] // 3, self.board.board[col, row] // 3):
                    stock.remove(tile)
                    if self.verbose:
                        print(f"Getting tile {tile} from stock.")
                    return tile
        return Tile(self.board.default_value)

    def _place_drawn_tile(self, tile: Tile) -> Tile:
        """
        Place the tile
        :param tile: Tile drawn by the Bot
        :return: Tile, the input tile if discarded, the exchange tile or None if no tile was removed
        """
        if tile == 1:
            self.board.place_tile(tile, 0, 0)
        elif tile == 20:
            self.board.place_tile(tile, 3, 3)

        target_diag = max(0, min(7, tile // 3))

        for row in range(self.board.board.shape[0]):
            for col in range(self.board.board.shape[1]):
                if target_diag != row + col:
                    continue
                current_tile_diag = max(0, min(6, cast(Tile, self.board.board[row, col]) // 3))
                if self.board.board[row, col] == -1 or current_tile_diag != row + col:
                    r, changed_tile = self._place_tile(tile, row, col)
                    if r:
                        return changed_tile
        return tile

    def _place_stocked_tile(self, tile: Tile) -> Tile:
        return self._place_drawn_tile(tile)