from player import Player, BotPlayer
from queue_tiles import QueueTiles
import numpy as np
BOARD_SIZE = 4


class LuckyNumbers:
    def __init__(self, nb_humans: int = 2, nb_bots: int = 0, board_size: int = BOARD_SIZE):
        """
        Initialise lucky numbers board
        One numpy array per player, and fill the diagonal for each player with 4 sorted Tiles randomly drawn
        :param nb_humans: int, from 0 to 4
        :param nb_bots: int, from 0 to 4
        """
        assert 0 <= nb_humans <= 4
        assert 0 <= nb_bots <= 4
        assert 2 <= nb_bots + nb_humans <= 4
        self.nb_players = nb_humans + nb_bots
        self.players = {i: Player(i, board_size, True) for i in range(nb_humans)}
        self.players.update({nb_humans + i: BotPlayer(i, board_size, False) for i in range(nb_bots)})
        self.queue_tiles = QueueTiles(self.nb_players)
        self.stock = []
        self.current_player = np.random.randint(0, self.nb_players)

        for i in self.players:
            self.players[i].board.init_diagonal(self.queue_tiles)
            self.players[i].tiles += board_size

    def player_turn(self) -> bool:
        self.current_player = (self.current_player + 1) % self.nb_players

        exchanged_tile = self.players[self.current_player].play_turn(self.queue_tiles, self.stock, self.players)
        if exchanged_tile != -1:
            self.stock.append(exchanged_tile)
            self.stock.sort()

        return self.players[self.current_player].board.is_ended()

    def play_game(self) -> int:
        player_won = False
        while not player_won and self.queue_tiles.get_tiles_left() >= self.nb_players:
            player_won = self.player_turn()

        if player_won:  # current player has finished his board
            print(f"Congrats! Player {self.current_player} won! He completed his board.")
            return 1
        else:  # too many tiles have been drawn
            tiles_placed = [self.players[i].tiles for i in self.players]
            max_tiles = max(tiles_placed)

            if tiles_placed.count(max_tiles) == 1:  # Only one player has the least number of spots left
                winning_player = tiles_placed.index(max_tiles)
                print(f"Congrats! Player {winning_player} won! He has {max_tiles} tiles placed.")

            else:  # Several players have the same number of spots left
                tied_players = [f"Player {i}" for i in self.players if tiles_placed[i] == max_tiles]
                print(f"It's a tie between {' and '.join(tied_players)}. They have {max_tiles} tiles placed.")

            return 0
