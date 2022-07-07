from game.board_logic import BoardLogic

class SimulationBoard(BoardLogic):
    def __init__(self, first_player):
        super().__init__(first_player)

    # Set a given state as self.state
    def set_simulation_state(self, state):
        self.state = state.copy()

    # Simulating move by using given row, column and color (player), and placing piece on the simulated state using place_piece func
    def simulate_move(self, row, column, color):
        self.place_piece(row, column, color)
        return self.state.copy()
