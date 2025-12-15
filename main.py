import arcade
import views.view_holder
from game_window import GameWindow
from views.menu_view import MenuView
from constants import *


def main():
    window = GameWindow()
    views.view_holder.menu_view = MenuView()
    window.show_view(views.view_holder.menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
