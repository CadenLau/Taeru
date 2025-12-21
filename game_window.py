import arcade
from constants import *


class GameWindow(arcade.Window):
    def __init__(self, fullscreen=True):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, title=SCREEN_TITLE)
        self.set_vsync(True)

        self.camera = arcade.Camera2D()
        self.camera.position = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

        self.toggle_fullscreen()

    def toggle_fullscreen(self):
        self.set_fullscreen(not self.fullscreen)

        self.camera.viewport = arcade.types.Viewport(
            left=(self.width - WINDOW_WIDTH) // 2,
            bottom=(self.height - WINDOW_HEIGHT) // 2,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
        )

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            self.toggle_fullscreen() # for macOS
            # arcade.close_window() # for Windows
