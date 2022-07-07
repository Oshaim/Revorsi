from game.board_logic import BoardLogic
from AI.AI_player import AIPlayer

class Tournament():
    def __init__(self, players):
        self.players = players
        
    # Runs a tournament with a list of survivors. 
    # The tournament runs equally for each survivor, and not runs the same survivor against itself.
    def start_tournament(self, players_list : list[AIPlayer]):
        for player_1 in players_list:
            for player_2 in players_list:
                if player_1 == player_2:
                    continue
                player_1_pieces, player_2_pieces = self.match(player_1, player_2)
                pieces_difference = player_1_pieces - player_2_pieces
                player_1.fitness(pieces_difference)
                player_2.fitness(pieces_difference)

    # Runs a match with two players (survivors) 
    def match(self, player_1 : AIPlayer, player_2 : AIPlayer):
        board = BoardLogic(1)
        player_1.set_color(1)
        player_2.set_color(2)

        while(True):
            if len(board.get_valid_moves(1)) == 0:
                if len(board.get_valid_moves(2)) == 0:
                    player_1_pieces, player_2_pieces = board.piece_count()
                    return player_1_pieces, player_2_pieces
            else:
                move = player_1.choose_best_move(board.get_state())
                board.place_piece(move[0], move[1], 1)

            if len(board.get_valid_moves(2)) == 0:
                if len(board.get_valid_moves(1)) == 0:
                    player_1_pieces, player_2_pieces = board.piece_count()
                    return player_1_pieces, player_2_pieces
            else:
                move = player_2.choose_best_move(board.get_state())
                board.place_piece(move[0], move[1], 2)