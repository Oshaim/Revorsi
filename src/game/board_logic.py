import numpy

class BoardLogic:
    def __init__(self, first_player):
        self.state = numpy.zeros((8, 8), dtype=int)
        self.reset(first_player)
    
    # Resets the board and place in self.state the first pieces, according to first_player
    def reset(self, first_player):
        self.state.fill(0)
        if first_player == 1:
            self.state[3:5, 3:5] = [[1, 2], [2, 1]]
        if first_player == 2:
            self.state[3:5, 3:5] = [[2, 1], [1, 2]]
    
    # Placing piece if the cell is empty and the move is valid. If one of the conditions isnt fulfill, returns False.
    # In addition, flips pieces according to the game rules.
    def place_piece(self, row, column, color):
        if self.state[row, column] == 0 and self.is_valid_move(row, column, color):
            self.state[row, column] = color
            self.flop(self.get_flops(row, column, color))
            return True
        return False
    
    # Returns a list with all the valid moves for the player
    def get_valid_moves(self, color): 
        return [move for move in self.get_blanks() if self.is_valid_move(move[0], move[1], color)]

    # Returns a list with all the empty places on board (all the cells in state that equal to 0)
    def get_blanks(self):
        blank_list = []
        for row, column in numpy.ndindex(self.state.shape):
            if self.state[row, column] == 0:
                blank_list.append((row, column))
        return blank_list

    # Boolean func that returns is the move valid
    def is_valid_move(self, row, column, color):
        return len(self.get_flops(row, column, color)) != 0

    # For every cell in the flip list, change the color from one to another 
    def flop(self, to_flop):
        for cell in to_flop:
            [row, column] = cell
            if self.state[row, column] == 1:
                self.state[row, column] = 2

            elif self.state[row, column] == 2:
                self.state[row, column] = 1

    # Checks for every cell around the current-placed piece if there are any pieces nerby. 
    # Returns a list with all the cells that required a flip.
    def get_flops(self, row, column, color):
        vectors = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
        to_flop = []
        for vector in vectors:
            try:
                _row, _column = row, column
                [_row, _column] = self.__add_vector([_row, _column], vector)

                while self.is_enemy(_row, _column, color):
                    [_row, _column] = self.__add_vector([_row, _column], vector)

                if self.state[_row, _column] != 0:
                    vector = [val * -1 for val in vector]
                    [_row, _column] = self.__add_vector([_row, _column], vector)

                while self.is_enemy(_row, _column, color):
                    to_flop.append([_row, _column])
                    [_row, _column] = self.__add_vector([_row, _column], vector)
            except IndexError:
                continue
        return to_flop

    # A private func of get_flops() that helps search around a specific cell, by adding a vector to the given cell.
    # Returns coords of column and row
    def __add_vector(self, coords, vector):
        [row, column] = [sum(i) for i in zip(coords, vector)]
        if not (-1 < row < 8 and -1 < column < 8):
            raise IndexError
        return [row, column]

    # Checks if the piece (if any) in the given column and row, is an enemy's one. 
    # If yes - returns True, and if not - returns False.
    def is_enemy(self, row, column, player_color):
        if self.state[row, column] == 0 or player_color == self.state[row, column]:
            return False
        return True

    # Checks how many pieces are on the board (in state) for each player. Returns the amount for each player as tuple of int.
    def piece_count(self):
        black_pieces = numpy.count_nonzero(self.state == 1)
        white_pieces = numpy.count_nonzero(self.state == 2)
        return black_pieces, white_pieces

    # Returns the state
    def get_state(self):
        return self.state.copy()

    # Returns who is the winner, while 1 = black, 2 = white, 0 = tie
    def get_winner(self):
        black_pieces, white_pieces = self.piece_count()
        if black_pieces > white_pieces:
            return 1
        elif white_pieces > black_pieces:
            return 2
        else:
            return 0
    
    # Checks if the game is still on. If both players got no more moves, returns the number of the winner. 
    # If the game is still on, returns None.
    def is_gameover(self, color): 
        players = [2,1] 
        valid_moves = self.get_valid_moves(color) 
        if len(valid_moves) == 0: 
            valid_moves = self.get_valid_moves(players[color - 1]) 
            if len(valid_moves) == 0: 
                return self.get_winner() 
        return None