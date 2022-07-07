# imports of libraries
import arcade
import arcade.gui
import random
from time import sleep
from itertools import cycle

# imports from other scrips
import config
from game.game_board import GameBoard
from AI.AI_player import AIPlayer
from utils import *


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.menu_background = load_image("new_main_menu.png")
        self.buttons = {
            "AI" : load_image("button_AI.png"), 
            "player" : load_image("button_player.png"),
            "help" : load_image("button_how_to_play.png")}

        self.h_box = arcade.gui.UIBoxLayout(
            x=0, 
            y=0, 
            vertical = False, 
            space_between = 50
            )
        self.create_buttons()

        self.manager.add(arcade.gui.UIAnchorWidget(
                anchor_x = "center_x",
                anchor_y = "center_y",
                child = self.h_box))

    def setup(self):
        pass

    # Creates buttons and waiting for "clicks" on them, thanks to events.
    def create_buttons(self):
        player_button = arcade.gui.UITextureButton(
            x = 0, 
            y = 0, 
            texture = self.buttons["player"]
            # texture_hovered: Optional[arcade.texture.Texture] = None, 
            # texture_pressed: Optional[arcade.texture.Texture] = None
            )

        @player_button.event("on_click")
        def _on_click_player_button(event):
            game_view = GameView(is_bot = False, difficulty = 0)
            self.manager.disable()
            self.window.show_view(game_view)

        help_button = arcade.gui.UITextureButton(
            x = 0, 
            y = 0, 
            texture = self.buttons["help"]
            # texture_hovered: Optional[arcade.texture.Texture] = None, 
            # texture_pressed: Optional[arcade.texture.Texture] = None
            )

        @help_button.event("on_click")
        def _on_click_player_button(event):
            help_view = HelpViewFirst("Menu", None)
            self.manager.disable()
            self.window.show_view(help_view)

        AI_button = arcade.gui.UITextureButton(
            x = 0, 
            y = 0, 
            texture = self.buttons["AI"]
            # texture_hovered: Optional[arcade.texture.Texture] = None, 
            # texture_pressed: Optional[arcade.texture.Texture] = None
            )

        @AI_button.event("on_click")
        def _on_click_player_button(event):
            game_view = GameView(is_bot = True, difficulty = 0)
            self.manager.disable()
            self.window.show_view(game_view)

        self.h_box.add(player_button)
        self.h_box.add(help_button)
        self.h_box.add(AI_button)

    # Draws the background of the page
    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(
            bottom_left_x = 0, 
            bottom_left_y = 0, 
            width = (config.SCREEN_WIDTH / 125) * 100, # TODO
            height = (config.SCREEN_HEIGHT / 125) * 100, # TODO
            texture = self.menu_background)
        
        self.manager.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    # When the ESC key pressed, the program will close
    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            arcade.close_window()

class HelpViewFirst(arcade.View):
    def __init__(self, view, difficulty):
        super().__init__()
        self.view = view
        self.difficulty = difficulty


        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.background = load_image("how_first_page.png")
        self.buttons = {
            "ok" : load_image("help_ok_button.png"), 
            "next" : load_image("help_next_button.png")}

        self.h_box = arcade.gui.UIBoxLayout(
            x=0, 
            y=0, 
            vertical = False, 
            space_between = 29.6
            )
        self.create_buttons()

        self.manager.add(arcade.gui.UIAnchorWidget(
                anchor_x = "center_x",
                anchor_y = "bottom",
                align_y= 35,
                child = self.h_box))

    # Creates buttons and waiting for "clicks" on them, thanks to events.
    def create_buttons(self):
        ok_button = arcade.gui.UITextureButton(
            x = 0, 
            y = 0, 
            texture = self.buttons["ok"],
            scale = 0.75
            # texture_hovered: Optional[arcade.texture.Texture] = None, 
            # texture_pressed: Optional[arcade.texture.Texture] = None
            )

        @ok_button.event("on_click")
        def _on_click_player_button(event):
            back_view = None
            if self.view == "Bot_Game":
                back_view = GameView(True, self.difficulty)
                self.manager.disable()
                self.window.show_view(back_view)
            if self.view == "Players_Game":
                back_view = GameView(False, self.difficulty)
                self.manager.disable()
                self.window.show_view(back_view)
            if self.view == "Menu":
                back_view = MenuView()
                self.manager.disable()
                self.window.show_view(back_view)

        next_button = arcade.gui.UITextureButton(
            x = 0, 
            y = 0, 
            texture = self.buttons["next"],
            scale = 0.75
            # texture_hovered: Optional[arcade.texture.Texture] = None, 
            # texture_pressed: Optional[arcade.texture.Texture] = None
            )

        @next_button.event("on_click")
        def _on_click_player_button(event):
            next_view = HelpViewSecond(self.view, self.difficulty)
            self.manager.disable()
            self.window.show_view(next_view)

        self.h_box.add(ok_button)
        self.h_box.add(next_button)

    # Draws the background of the page
    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(
            bottom_left_x = 0, 
            bottom_left_y = 0, 
            width = (config.SCREEN_WIDTH / 125) * 100, # TODO
            height = (config.SCREEN_HEIGHT / 125) * 100, # TODO
            texture = self.background)
        
        self.manager.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    # When the ESC key pressed, the program will close
    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            arcade.close_window()

class HelpViewSecond(arcade.View):
    def __init__(self, view, difficulty):
        super().__init__()
        self.view = view
        self.difficulty = difficulty

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.background = load_image("how_second_page.png")
        self.buttons = {
            "ok" : load_image("help_ok_button.png"), 
            "previous" : load_image("help_previous_button.png")}

        self.h_box = arcade.gui.UIBoxLayout(
            x=0, 
            y=0, 
            vertical = False, 
            space_between = 29.6
            )
        self.create_buttons()

        self.manager.add(arcade.gui.UIAnchorWidget(
                anchor_x = "center_x",
                anchor_y = "bottom",
                align_y= 35,
                child = self.h_box))
    
    # Creates buttons and waiting for "clicks" on them, thanks to events.
    def create_buttons(self):
        ok_button = arcade.gui.UITextureButton(
            x = 0, 
            y = 0, 
            texture = self.buttons["ok"],
            scale = 0.75
            # texture_hovered: Optional[arcade.texture.Texture] = None, 
            # texture_pressed: Optional[arcade.texture.Texture] = None
            )

        @ok_button.event("on_click")
        def _on_click_player_button(event):
            back_view = None
            if self.view == "Bot_Game":
                back_view = GameView(True, self.difficulty)
                self.manager.disable()
                self.window.show_view(back_view)
            if self.view == "Players_Game":
                back_view = GameView(False, self.difficulty)
                self.manager.disable()
                self.window.show_view(back_view)
            if self.view == "Menu":
                back_view = MenuView()
                self.manager.disable()
                self.window.show_view(back_view)

        previous_button = arcade.gui.UITextureButton(
            x = 0, 
            y = 0, 
            texture = self.buttons["previous"],
            scale = 0.75
            # texture_hovered: Optional[arcade.texture.Texture] = None, 
            # texture_pressed: Optional[arcade.texture.Texture] = None
            )

        @previous_button.event("on_click")
        def _on_click_player_button(event):
            previous_view = HelpViewFirst(self.view, self.difficulty)
            self.manager.disable()
            self.window.show_view(previous_view)

        self.h_box.add(ok_button)
        self.h_box.add(previous_button)

    # Draws the background of the page
    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(
            bottom_left_x = 0, 
            bottom_left_y = 0, 
            width = (config.SCREEN_WIDTH / 125) * 100, # TODO
            height = (config.SCREEN_HEIGHT / 125) * 100, # TODO
            texture = self.background)
        
        self.manager.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    # When the ESC key pressed, the program will close
    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            arcade.close_window()

class GameView(arcade.View):

    def __init__(self, is_bot, difficulty):
        super().__init__()
        self.is_bot = is_bot
        self.difficulty = difficulty
        self.is_playing = True
        self.manager_settings = arcade.gui.UIManager()
        self.manager_settings.enable()
        self.manager_difficulty = arcade.gui.UIManager()
        self.manager_difficulty.enable()

        self.player = cycle([1, 2])
        self.current_player = next(self.player)
        self.bot_player = 2
        if random.randrange(1, 3) == 2:
            self.current_player = next(self.player)
            self.bot_player = 1

        self.board = GameBoard(config.GRID_X, config.GRID_Y, config.CELL_SIZE, config.LINE_WIDTH, config.RADIUS, self.current_player)
        self.bot_easy = AIPlayer([157.1631276, 189.1123849, 67.51682668, 177.5403242, 147.3622692, 92.84156371, 106.7564277, 58.11331044, 74.3171162, 133.0320761], 26.45187719, 28.50986688)
        self.bot_hard = AIPlayer([211.87188680367024, 127.08906770260882, 126.57109287240054, 33.98778849796111, 8.460626770740863, 0.05003660800909029, 0.04006195728609308, -9.98750351939673, -230.24933704119175, 28.75327447170266], 29.649114001314693, 10.651903063952647 )
        self.bot = None

        if self.difficulty == 0:
            self.bot = self.bot_easy
        if self.difficulty == 1:
            self.bot = self.bot_hard

        self.bot.set_color(self.bot_player)

        self.buttons = {
            "help" : load_image("ingame_howto_button.png"),
            "home" : load_image("ingame_home_button.png"), 
            "replay" : load_image("ingame_replay_button.png"),
            "easy_pressed" : load_image("easy_pressed_button.png"),
            "hard_pressed" : load_image("hard_pressed_button.png"),
            "easy" : load_image("easy_button.png"),
            "hard" : load_image("hard_button.png")}

        if self.difficulty == 0:
            self.buttons["easy"] = self.buttons["easy_pressed"]
        else:
            self.buttons["hard"] = self.buttons["hard_pressed"]

        self.h_box_settings = arcade.gui.UIBoxLayout(
            x=0, 
            y=0, 
            vertical = False, 
            space_between = 72
            )
        
        self.h_box_difficulty = arcade.gui.UIBoxLayout(
            x=0, 
            y=0, 
            vertical = False, 
            space_between = 90
            )

        self.create_buttons()

        self.manager_settings.add(arcade.gui.UIAnchorWidget(
                anchor_x = "right",
                anchor_y = "center_y",
                align_x = - config.SCREEN_WIDTH / 13,
                align_y = - config.SCREEN_HEIGHT / 9,
                child = self.h_box_settings))
        
        self.manager_difficulty.add(arcade.gui.UIAnchorWidget(
                anchor_x = "right",
                anchor_y = "center_y",
                align_x = - config.SCREEN_WIDTH / 13,
                align_y = 0,
                child = self.h_box_difficulty))

    def setup(self):
        pass

    # Creates buttons and waiting for "clicks" on them, thanks to events.
    def create_buttons(self):
        home_button = arcade.gui.UITextureButton(
            x = 0, 
            y = 0, 
            texture = self.buttons["home"],
            scale = 0.75
            # texture_hovered: Optional[arcade.texture.Texture] = None, 
            # texture_pressed: Optional[arcade.texture.Texture] = None
            )

        @home_button.event("on_click")
        def _on_click_player_button(event):
            home_view = MenuView()
            self.manager_settings.disable()
            self.window.show_view(home_view)

        help_button = arcade.gui.UITextureButton(
            x = 0, 
            y = 0, 
            texture = self.buttons["help"],
            scale = 0.75
            # texture_hovered: Optional[arcade.texture.Texture] = None, 
            # texture_pressed: Optional[arcade.texture.Texture] = None
            )

        @help_button.event("on_click")
        def _on_click_player_button(event):
            if self.is_bot:
                game_type = "Bot_Game"
            else:
                game_type = "Players_Game"
            
            help_view = HelpViewFirst(game_type, self.difficulty)       
            self.manager_settings.disable()
            self.window.show_view(help_view)

        replay_button = arcade.gui.UITextureButton(
            x = 0, 
            y = 0, 
            texture = self.buttons["replay"],
            scale = 0.75
            # texture_hovered: Optional[arcade.texture.Texture] = None, 
            # texture_pressed: Optional[arcade.texture.Texture] = None
            )

        @replay_button.event("on_click")
        def _on_click_player_button(event):
            replay_view = GameView(is_bot = self.is_bot, difficulty = self.difficulty)
            self.manager_settings.disable()
            self.window.show_view(replay_view)

        easy_button = arcade.gui.UITextureButton(
            x = 0, 
            y = 0, 
            texture = self.buttons["easy"],
            scale = 0.75
            # texture_hovered: Optional[arcade.texture.Texture] = None, 
            # texture_pressed: Optional[arcade.texture.Texture] = None
            )

        @easy_button.event("on_click")
        def _on_click_player_button(event):
            if self.difficulty == 0:
                return
            game_view = GameView(self.is_bot, 0)
            self.manager_difficulty.disable()
            self.window.show_view(game_view)

        hard_button = arcade.gui.UITextureButton(
            x = 0, 
            y = 0, 
            texture = self.buttons["hard"],
            scale = 0.75
            # texture_hovered: Optional[arcade.texture.Texture] = None, 
            # texture_pressed: Optional[arcade.texture.Texture] = None
            )

        @hard_button.event("on_click")
        def _on_click_player_button(event):
            if self.difficulty == 1:
                return
            game_view = GameView(self.is_bot, 1)
            self.manager_difficulty.disable()
            self.window.show_view(game_view)

        self.h_box_settings.add(help_button)
        self.h_box_settings.add(home_button)
        self.h_box_settings.add(replay_button)
        self.h_box_difficulty.add(easy_button)
        self.h_box_difficulty.add(hard_button)

    # Draws on the screen
    def on_draw(self):
        self.clear()
        # This command should happen before we start drawing. 
        # It will clear the screen to the background color, and erase what we drew last frame.
        self.board.draw()
        self.draw_background()
        self.manager_settings.draw()
        if self.is_bot:
            self.manager_difficulty.draw()
        self.board.draw_valid_moves(self.current_player)
        self.draw_winner()

    # Runs every delta_time that sets up in ahead in Arcade's lib.
    # Checks if the game is still on. In addition, checks if there are any valid moves, and if not skips to the other player.
    # If the game played with bot, does the bot move if it it's turn.
    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here. Normally, you'll call update() on the sprite lists that need it.
        """
        
        if self.is_playing:
            valid_moves = self.board.get_valid_moves(self.current_player)
            if len(valid_moves) == 0:
                self.current_player = next(self.player)
                valid_moves = self.board.get_valid_moves(self.current_player)
                if len(valid_moves) == 0:
                    self.is_playing = False
                return
            
            if self.is_bot:
                if self.current_player == self.bot_player:
                    row, column = self.bot.choose_best_move(self.board.get_state())
                    if self.board.place_piece(row, column, self.bot_player):
                        self.current_player = next(self.player)
        
    # When there is a mouse press on the screen, locates the mouse and places piece if the click was on board.
    def on_mouse_press(self, x, y, button, key_modifiers):
        if self.current_player != self.bot_player or not self.is_bot:
            if self.on_board(y, x):
                if self.board.player_place_piece(y, x, self.current_player):
                    self.current_player = next(self.player)
        else:
            pass
    
    # If there was a press on escape key, the game will close
    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            arcade.close_window()

    # Checks if given coords of x,y are in a cell on board. If yes - returns True, if not - returns False.
    def on_board(self, y, x):
        if (x > config.GRID_X) and (x < (config.GRID_X + config.CELL_SIZE * 8)) and \
            (y > config.GRID_Y) and (y < (config.GRID_Y + config.CELL_SIZE * 8)):
            return True
        return False

    # Collect all the elements and funcs that requires a draw on the background
    def draw_background(self):
        # Draw piece counters above the board
        black_pieces, white_pieces = self.board.piece_count()
        self.draw_counter(1, black_pieces)
        self.draw_counter(2, white_pieces)

        # Draw a frame with the color of current player
        self.draw_current_player(self.current_player)

    # Draws the piece counters 
    def draw_counter(self, color, count):
        add_on_rec = 1
        color_text = arcade.color.WHITE
        if color == 1:
            add_on_rec = 3
            color_text = arcade.color.BLACK

        arcade.draw_text(
            text = str(count),
            start_x = config.GRID_X + (config.CELL_SIZE * 2 * add_on_rec) - (config.CELL_SIZE * 1.5),
            start_y = (config.GRID_Y + config.CELL_SIZE * 9.4),
            color = color_text,
            font_size = config.CELL_SIZE,
            width = config.CELL_SIZE * 3,
            align = 'center',
            bold = True,
            rotation = 0)

    # Draws the winner when the value is_playing = False.
    def draw_winner(self):
        if not self.is_playing:
            winner = self.board.get_winner()
            if winner == 1:
                # arcade.draw_text(
                    # text="The winner is BLACK!",
                    # # start_x=config.GRID_X * 1 + config.CELL_SIZE * 8,
                    # start_x = config.SCREEN_WIDTH - config.GRID_X * 2 - config.CELL_SIZE * 10,
                    # start_y = config.CELL_SIZE * 8 + config.GRID_Y,
                    # color = arcade.color.WHITE,
                    # font_size=config.CELL_SIZE * 0.75,
                    # width=config.CELL_SIZE * 10,
                    # align='center',
                    # bold=True,
                    # rotation=0)
                arcade.draw_lrwh_rectangle_textured(
                    bottom_left_x = (1100 / 125) * 100, 
                    bottom_left_y = (650 / 125) * 100 , 
                    width = (750 / 125) * 100, # TODO
                    height = (250 / 125) * 100, # TODO
                    texture = load_image("winner_black.png"))

            elif winner == 2:
                # arcade.draw_text(
                #     text = "The winner is WHITE!",
                #     start_x = config.SCREEN_WIDTH - config.GRID_X * 2 - config.CELL_SIZE * 10,
                #     start_y = config.CELL_SIZE * 8 + config.GRID_Y,
                #     color = arcade.color.WHITE,
                #     font_size = config.CELL_SIZE * 0.75,
                #     width = config.CELL_SIZE * 10,
                #     align = 'center',
                #     bold = True,
                #     rotation = 0)
                arcade.draw_lrwh_rectangle_textured(
                    bottom_left_x = (1100 / 125) * 100, 
                    bottom_left_y = (650 / 125) * 100 , 
                    width = (750 / 125) * 100, # TODO
                    height = (250 / 125) * 100, # TODO
                    texture = load_image("winner_white.png"))
            else:
                # arcade.draw_text(
                #     text="It's a tie!",
                #     start_x=config.GRID_X * 2 + config.CELL_SIZE * 8,
                #     start_y=config.SCREEN_HEIGHT / 2,
                #     color=arcade.color.CHARCOAL,
                #     font_size=config.CELL_SIZE,
                #     width=config.CELL_SIZE * 10,
                #     align='center',
                #     bold=True,
                #     rotation=0)
                arcade.draw_lrwh_rectangle_textured(
                    bottom_left_x = (1100 / 125) * 100, 
                    bottom_left_y = (650 / 125) * 100 , 
                    width = (750 / 125) * 100, # TODO
                    height = (250 / 125) * 100, # TODO
                    texture = load_image("winner_tie.png"))

    # Draws a small rectangle that signs which player plays this turn
    def draw_current_player(self, current):
        if current == 1:
            arcade.draw_lrwh_rectangle_textured(
            bottom_left_x = (670 / 125) * 100, 
            bottom_left_y = (885 / 125) * 100, 
            width = (350 / 125) * 100, # TODO
            height = (145 / 125) * 100, # TODO
            texture = load_image("outer_glow.png"))

        else:
            arcade.draw_lrwh_rectangle_textured(
            bottom_left_x = (180 / 125) * 100, 
            bottom_left_y = (885 / 125) * 100 , 
            width = (350 / 125) * 100, # TODO
            height = (145 / 125) * 100, # TODO
            texture = load_image("outer_glow.png"))