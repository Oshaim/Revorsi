# imports of libraries
import arcade

# imports from other scrips
import config
from game_views import GameView, MenuView


def main():
    window = arcade.Window(config.SCREEN_WIDTH, config.SCREEN_HEIGHT, config.SCREEN_TITLE, fullscreen=True)
    start_view = MenuView()
    window.show_view(start_view)
    start_view.setup()
    # The main loop of the script
    arcade.run() 

if __name__ == "__main__":
    main()