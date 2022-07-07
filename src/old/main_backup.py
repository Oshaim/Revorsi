# imports of other scrips
from inspect import ismemberdescriptor
from AI.AI_player import AIPlayer
import config
from game.game_board import GameBoard

# imports of libraries
import arcade
import random
from itertools import cycle
from time import sleep


class MenuScreen(arcade.View):
    def __init__ (self, width, height, title):
        pass

    def on_show(self):
        pass

    def on_draw(self):
        pass

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        pass


class GameScreen(arcade.Window):
    is_playing = True
    player = cycle([1, 2])
    bot_player = 2
    if random.randrange(1, 3) == 2:
        next(player)
    current_player = next(player)

    board = GameBoard(config.GRID_X, config.GRID_Y, config.CELL_SIZE, config.LINE_WIDTH, config.RADIUS, current_player)
    bot = AIPlayer()

    def __init__(self, width, height, title, isBot):
        super().__init__(width, height, title)
        self.isBot = isBot

        arcade.set_background_color(arcade.csscolor.BISQUE)

        # If you have sprite lists, you should create them here,
        # and set them to None

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here
        self.set_fullscreen(self.fullscreen)

    def on_draw(self):
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()
        self.board.draw()
        self.draw_background()
        self.draw_winner()

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        if self.is_playing:
            valid_moves = self.board.get_valid_moves(self.current_player)
            if len(valid_moves) == 0:
                self.current_player = next(self.player)
                print(1)
                valid_moves = self.board.get_valid_moves(self.current_player)
                if len(valid_moves) == 0:
                    self.is_playing = False
                return

            if self.current_player == self.bot_player:
                row, column = self.bot.choose_best_move(valid_moves)
                if self.board.place_piece(row, column, self.bot_player):
                    self.current_player = next(self.player)

    def on_mouse_press(self, x, y, button, key_modifiers):
        if self.current_player != self.bot_player:
            if self.on_board(x, y):
                if self.board.player_place_piece(x, y, self.current_player):
                    self.current_player = next(self.player)
            else:
                pass

    def on_board(self, x, y):
        if (x > config.GRID_X) and (x < (config.GRID_X + config.CELL_SIZE * 8)) and \
            (y > config.GRID_Y) and (y < (config.GRID_Y + config.CELL_SIZE * 8)):
            return True
        return False

    def draw_background(self):
        # Draw a frame for the game board
        arcade.draw_rectangle_outline(
            center_x=(config.GRID_X + config.CELL_SIZE * 4),
            center_y=(config.GRID_Y + config.CELL_SIZE * 4),
            width=config.CELL_SIZE * 8 + (config.LINE_WIDTH + 20),
            height=config.CELL_SIZE * 8 + (config.LINE_WIDTH + 20),
            color=arcade.color.CHARCOAL,
            border_width=config.LINE_WIDTH + 10,
            tilt_angle=0)

        # Draw piece counters above the board
        self.draw_counter(1, self.counter()[0])
        self.draw_counter(2, self.counter()[1])

        # Draw a frame with the color of current player
        self.draw_current_player(self.current_player)

    def draw_counter(self, color, count):
        add_on_rec = 1
        color_back = arcade.color.BLACK
        color_text = arcade.color.WHITE
        if color == 2:
            add_on_rec = 3
            color_back = arcade.color.WHITE
            color_text = arcade.color.BLACK

        arcade.draw_rectangle_filled(
            center_x=(config.GRID_X + config.CELL_SIZE * 2 * add_on_rec),
            center_y=(config.GRID_Y + config.CELL_SIZE * 10),
            width=config.CELL_SIZE * 3,
            height=config.CELL_SIZE * 1.5,
            color=color_back,
            tilt_angle=0)

        arcade.draw_rectangle_outline(
            center_x=(config.GRID_X + config.CELL_SIZE * 2 * add_on_rec),
            center_y=(config.GRID_Y + config.CELL_SIZE * 10),
            width=config.CELL_SIZE * 3,
            height=config.CELL_SIZE * 1.5,
            color=arcade.color.CHARCOAL,
            border_width=config.LINE_WIDTH * 2,
            tilt_angle=0)

        arcade.draw_text(
            text = str(count),
            start_x = config.GRID_X + (config.CELL_SIZE * 2 * add_on_rec) - (config.CELL_SIZE * 1.5),
            start_y = (config.GRID_Y + config.CELL_SIZE * 9.5),
            color = color_text,
            font_size = config.CELL_SIZE,
            width = config.CELL_SIZE * 3,
            align = 'center',
            bold = True,
            rotation = 0)

    def draw_winner(self):
        if not self.is_playing:
            black_pieces, white_pieces = self.counter()
            if black_pieces > white_pieces:
                winner_player = 1
                arcade.draw_text(
                    text="The winner is BLACK!",
                    start_x=config.GRID_X * 1.5 + config.CELL_SIZE * 8,
                    start_y=config.SCREEN_HEIGHT / 2,
                    color=arcade.color.CHARCOAL,
                    font_size=config.CELL_SIZE,
                    width=config.CELL_SIZE * 10,
                    align='center',
                    bold=True,
                    rotation=0)

            elif black_pieces < white_pieces:
                winner_player = 2
                arcade.draw_text(
                    text = "The winner is WHITE!",
                    start_x = config.GRID_X * 2 + config.CELL_SIZE * 8,
                    start_y = config.SCREEN_HEIGHT / 2,
                    color = arcade.color.CHARCOAL,
                    font_size = config.CELL_SIZE,
                    width = config.CELL_SIZE * 10,
                    align = 'center',
                    bold = True,
                    rotation = 0)
            else:
                winner_player = 0
                arcade.draw_text(
                    text="It's a tie!",
                    start_x=config.GRID_X * 2 + config.CELL_SIZE * 8,
                    start_y=config.SCREEN_HEIGHT / 2,
                    color=arcade.color.CHARCOAL,
                    font_size=config.CELL_SIZE,
                    width=config.CELL_SIZE * 10,
                    align='center',
                    bold=True,
                    rotation=0)

    def counter(self):
        black_pieces, white_pieces = self.board.piece_count()
        return black_pieces, white_pieces

    def draw_current_player(self, current):
        if current == 1:
            player_color = arcade.csscolor.BLACK
        else:
            player_color = arcade.csscolor.WHITE

        arcade.draw_rectangle_filled(
            center_x=(config.GRID_X + config.CELL_SIZE * 4),
            center_y=(config.GRID_Y + config.CELL_SIZE * 10),
            width=config.CELL_SIZE / 5,
            height=config.CELL_SIZE * 1.5,
            color=player_color,
            tilt_angle=0)


def main():
    """ Main functiond """
    game = GameScreen(config.SCREEN_WIDTH, config.SCREEN_HEIGHT, config.SCREEN_TITLE, True)
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()
