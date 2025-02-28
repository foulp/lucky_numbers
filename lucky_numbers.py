from player import Player
from queue_tiles import QueueTiles
import numpy as np
BOARD_SIZE = 4


class LuckyNumbers:
    def __init__(self, nb_players: int = 2, board_size: int = BOARD_SIZE):
        """
        Initialise lucky numbers board
        One numpy array per player, and fill the diagonal for each player with 4 sorted Tiles randomly drawn
        :param nb_players: int, from 2 to 4
        """
        assert 2 <= nb_players <= 4
        self.nb_players: int = nb_players
        self.players: dict[int: Player] = {i: Player(i, board_size) for i in range(nb_players)}
        self.queue_tiles: QueueTiles = QueueTiles(nb_players)
        self.stock: list[int] = []
        self.current_player: int = np.random.randint(0, nb_players)

        for i in self.players:
            self.players[i].board.init_diagonal(self.queue_tiles)
            self.players[i].tiles += board_size

    def player_turn(self):
        self.current_player = (self.current_player + 1) % self.nb_players
        print(f"Player {self.current_player}, it's your turn.")
        print(f"This is your board:\n{self.players[self.current_player].board.board}")
        print(f"These are other players's boards:")
        for i in self.players:
            if i != self.current_player:
                print(f"Player {i}")
                print(self.players[i].board.board)
        picked_tile = self.players[self.current_player].pick_tile(self.queue_tiles, self.stock)
        exchanged_tile = self.players[self.current_player].place_tile(picked_tile)
        if exchanged_tile:
            self.stock.append(exchanged_tile)
            self.stock.sort()

        return self.players[self.current_player].board.is_ended()

    def play_game(self):
        player_won = False
        while not player_won and self.queue_tiles.get_tiles_left() >= self.nb_players:
            player_won = self.player_turn()
        if player_won:
            print(f"Congrats! Player {self.current_player} won!")
        else:
            tiles_placed = [self.players[i].tiles for i in self.players]
            max_tiles = max(tiles_placed)
            if tiles_placed.count(max_tiles) == 1:
                winning_player = tiles_placed.index(max_tiles)
                print(f"Congrats! Player {winning_player} won! He has {max_tiles} tiles placed.")
            else:
                tied_players = [f"Player {i}" for i in self.players if tiles_placed[i] == max_tiles]
                print(f"It's a tie between {' and '.join(tied_players)}. They have {max_tiles} tiles placed.")
        return True
