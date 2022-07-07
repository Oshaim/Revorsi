import numpy
import math
from game.simulation_board import SimulationBoard

class AIPlayer:
    def __init__(self, board_coefficients, bonus_size, penalty_coefficient):
        self.color = None
        self.board_coefficients = board_coefficients
        self.bonus_size = bonus_size
        self.penalty_coefficient = penalty_coefficient

        self.mapping = numpy.array(
            [[0,7,1,2,2,1,7,0], 
            [7,8,5,6,6,5,8,7],
            [1,5,4,3,3,4,5,1],
            [2,6,3,9,9,3,6,4],
            [2,6,3,9,9,3,6,4],
            [1,5,4,3,3,4,5,1],
            [7,8,5,6,6,5,8,7],
            [0,7,1,2,2,1,7,0]])

        self.fitness_score = 0
        self.fitness_coefficient = 0.03
        self.simulation = SimulationBoard(self.color) 

        self.test_state = \
        [[0, 1, 1, 1, 2, 2, 1, 2],
        [1, 1, 1, 1, 2, 2, 1, 2],
        [2, 2, 1, 2, 2, 2, 1, 2],
        [2, 2, 1, 2, 2, 2, 1, 2],
        [0, 2, 2, 2, 2, 2, 1, 1],
        [1, 1, 2, 2, 2, 2, 1, 1],
        [2, 1, 1, 2, 2, 2, 1, 1],
        [2, 1, 1, 1, 2, 2, 1, 1]]
        self.test_state = numpy.array(self.test_state)

    # Runs over every valid move, and checks which one got the highest evaluate value, and returns that move.
    def choose_best_move(self, board_state):
        self.simulation.set_simulation_state(board_state)
        evaluate, best_move = self.minimax(board_state, 3, -math.inf, math.inf, self.color)
        
        # valid_moves = self.simulation.get_valid_moves(self.color)
        # if len(valid_moves) == 0:
        # best_move = None
        # max_value = None
        # best_move = valid_moves[0]
        # max_value = self.evaluate(self.simulation.simulate_move(valid_moves[0][0], valid_moves[0][1], self.color), self.color)
        # valid_moves.pop()
        # for move in valid_moves:
        #     current_value = self.evaluate(self.simulation.simulate_move(move[0], move[1], self.color), self.color)
        #     if current_value > max_value:
        #         max_value = current_value
        #         best_move = move

        return best_move

    # Applying Minimax Algorithm
    def minimax(self, current_state, current_depth, alpha, beta, color):
        players = [2, 1]
        simulation = SimulationBoard(self.color)
        simulation.set_simulation_state(current_state)
        max_evaluate = -math.inf
        min_evaluate = math.inf
        current_evaluate = 0.0        
        best_move = None

        valid_moves = simulation.get_valid_moves(color)

        if current_depth == 0 or simulation.is_gameover(color) or len(valid_moves) == 0:
            return self.evaluate(current_state, color), (-1, -1)

        if color == self.color:
            for move in valid_moves:
                new_state = simulation.simulate_move(move[0], move[1], color)
                current_evaluate, some_move = self.minimax(new_state.copy(), current_depth - 1, alpha, beta, players[color - 1])
                simulation.set_simulation_state(current_state)
                if current_evaluate > max_evaluate:
                    max_evaluate = current_evaluate
                    best_move = move
                
                alpha = max(alpha, current_evaluate)
                if beta <= alpha:
                    break
        
        else:
            for move in valid_moves:
                new_state = simulation.simulate_move(move[0], move[1], color)
                current_evaluate, some_move = self.minimax(new_state.copy(), current_depth - 1, alpha, beta, players[color - 1])
                simulation.set_simulation_state(current_state)
                if current_evaluate < min_evaluate:
                    min_evaluate = current_evaluate
                    best_move = move

                beta = min(beta, current_evaluate)
                if beta >= alpha:
                    break
        
        return self.evaluate(current_state, color), best_move

    # Creates a static weights map by placing board_coefficients values in mapping
    def set_coefficients_on_board(self):
        static_weights = numpy.zeros((8, 8), dtype=int)
        for row, column in numpy.ndindex(self.mapping.shape):
            static_weights[row, column] = self.board_coefficients[self.mapping[row, column]]
        return static_weights

    # Calculates the evaluate value, by summing weights, bonuses and penalties.
    # Returns the total_score of evaluate. 
    def evaluate(self, state, current_player): 
        weights = numpy.zeros((8, 8), dtype=int)
        
        total_score = 0
    
        self.__update_weights(state, weights, current_player)
        self.__update_weights_near_corner(state, weights, current_player)

        # Sum the total weights of the move
        for row, column in numpy.ndindex(weights.shape):
            total_score += weights[row, column]

        total_score = total_score - (self.__calculate_liberties(state, current_player) * self.penalty_coefficient)
        return total_score

    # Update the current weights map according to the pieces that are on the board. 
    # For every bot player's piece the weight will be positive, and for every enemy's piece negative.
    def __update_weights(self, state, weights, color):
        # Update the weights map according to the static_weights and state
        static_weights = self.set_coefficients_on_board()

        for row, column in numpy.ndindex(state.shape):
            if state[row, column] != 0:
                if state[row, column] == color:
                    weights[row, column] += static_weights[row, column]
                else:
                    weights[row, column] -= static_weights[row, column] 

    # If a player placed a piece in a corner, update the weights around it to 0, 
    # and give a bonus according to same-colored pieces near it
    def __update_weights_near_corner(self, state, weights, color):
        for i in [[0,0], [0,7], [7,0], [7,7]]:
            if state[i[0], i[1]] != 0:
                weights = self.__change_state_by_corners(weights, i)
                self.__add_bonus(state, weights, i[0], i[1], color)

    # Calculates the liberties of each player, 
    # and returns the subtract of the enemy_player_liberties of current_player_liberties
    def __calculate_liberties(self, state, color):  
        current_player_libreties = 0
        enemy_player_libreties = 0  
        for row, column in numpy.ndindex(state.shape):
            if state[row, column] != 0:
                if state[row, column] == color:
                    current_player_libreties += self.__count_near_liberties(state, row, column)
                else:
                    enemy_player_libreties += self.__count_near_liberties(state, row, column)
        return current_player_libreties - enemy_player_libreties

    # Returns the amount of near liberties of a player. Being used in __calculate_liberties()
    def __count_near_liberties(self, state, row, column):
        vectors = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
        near_liberties = 0
        for vector in vectors:
            try:
                _row, _column = row, column
                [_row, _column] = self.add_vector([_row, _column], vector)

                if state[_row, _column] == 0:
                    near_liberties += 1

            except IndexError:
                continue

        return near_liberties

    # A private func of __count_near_liberties() that helps search around a specific cell, by adding a vector to the given cell.
    # Returns coords of column and row
    def add_vector(self, coords, vector):
        [row, column] = [sum(i) for i in zip(coords, vector)]
        if not (-1 < column < 8 and -1 < row < 8):
            raise IndexError
        return [row, column]

    # Changes the cell's value around a corner that got a piece on it to zero
    def __change_state_by_corners(self, weights, index):
        row, column = index[0], index[1]
        vectors = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
        for vector in vectors:
            try:
                _row, _column = row, column
                [_row, _column] = self.add_vector([_row, _column], vector)

                weights[_row, _column] = 0
            except IndexError:
                continue

        return weights

    # Adds bonus on the weights map when there are pieces from the same color near a corner, in a row or column.
    def __add_bonus(self, state, weights, row, column, color): 
        _column = column
        _row = row    
        
        try:
            while (color == state[row, _column]):
                if column == 0:
                    _column += 1
                else:
                    _column -= 1
                weights[row, _column] += self.bonus_size
        except IndexError:
            pass

        try:
            while (color == state[_row, column]):
                if row == 0:
                    _row += 1
                else:
                    _row -= 1
                weights[_column, row] += self.bonus_size
        except IndexError:
            pass

    # Calculates the fitness value of one match, and adding it to the total fitness_score 
    def fitness(self, pieces_difference):
        if pieces_difference == 0:
            victory = 0
        else:
            victory = pieces_difference / abs(pieces_difference)
        
        self.fitness_score += (victory + pieces_difference * self.fitness_coefficient)

    def set_color(self, color):
        self.color = color
    
    def get_color(self):
        return self.color

    def get_fitness(self):
        return self.fitness_score
    
    def reset_fitness(self):
        self.fitness_score = 0

    def get_board_coefficients(self):
        return self.board_coefficients.copy()

    def set_board_coefficients(self, new_coefficients):
        self.board_coefficients = new_coefficients

    def get_bonus_size(self):
        return self.bonus_size

    def set_bonus_size(self, new_size):
        self.bonus_size = new_size
    
    def get_penalty_coefficient(self):
        return self.penalty_coefficient

    def set_penalty_coefficient(self, new_coefficient):
        self.penalty_coefficient = new_coefficient