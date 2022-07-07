import numpy
import arcade
from game.board_logic import BoardLogic
from utils import get_root_dir, load_image


class GameBoard(BoardLogic):
    def __init__(self, grid_x, grid_y, cell_size, line_width, radius, first_player) :
        super().__init__(first_player)
        
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.cell_size = cell_size
        self.line_width = line_width
        self.radius = radius

    # Draws the game board and any pieces on it based on internal state
    def draw(self):
        game_view_texture = load_image("game_view.png") 
        arcade.draw_lrwh_rectangle_textured(
            bottom_left_x = 0, 
            bottom_left_y = 0, 
            width = (1920 / 125) * 100, # TODO
            height = (1080 / 125) * 100, # TODO
            texture = game_view_texture)

        for column, row in numpy.ndindex(self.state.shape):
            if self.state[column, row] == 1:
                self.draw_circle(row, column, 1)
            if self.state[column, row] == 2:
                self.draw_circle(row, column, 2)
        
    # Draws a circle on the board by given column, row and color (player)
    def draw_circle(self, column, row, color):
        texture = load_image("ingame_black_piece.png") if color == 1 else load_image("ingame_white_piece.png")

        arcade.draw_scaled_texture_rectangle(
            center_x = self.grid_x + column * self.cell_size + (self.cell_size / 2), 
            center_y = self.grid_y + (7 - row) * self.cell_size + (self.cell_size / 2),
            scale = 0.55,
            texture = texture)

    # Placing piece on board by given location on board using locate_mouse and place_piece funcs, and returns True.
    # If its impossible to place piece because of invalid location, returns False.
    def player_place_piece(self, y, x, color):
        row, column = self.locate_mouse(y, x)
        return self.place_piece(row, column, color)

    # Locating the wanted cell to place a piece on according to (x,y) location.
    def locate_mouse(self, y, x):
        y_index = 7 - int((y - self.grid_y) / self.cell_size)
        x_index = int((x - self.grid_x) / self.cell_size)
        if not (-1 < x_index < 8 or -1 < y_index < 8):
            raise IndexError
        return y_index, x_index

    # Draws all the placed that are valid to choose on the board
    def draw_valid_moves(self, current_player):
        valid_moves = self.get_valid_moves(current_player)
        for move in valid_moves:
            arcade.draw_circle_filled(
                center_x=self.grid_x + move[1] * self.cell_size + (self.cell_size / 2),
                center_y=self.grid_y + (7 - move[0]) * self.cell_size + (self.cell_size / 2),
                radius=self.radius / 2,
                color=arcade.csscolor.GREEN)
