import arcade
from constants import *


class FadingView(arcade.View):
    def __init__(self):
        super().__init__()
        self.fade_in = 255

    def update_fade(self, next_view=None):
        if self.fade_in is not None:
            self.fade_in -= FADE_RATE
            if self.fade_in <= 0:
                self.fade_in = None

    def draw_fading(self):
        if self.fade_in is not None:
            if self.window.background_color == arcade.color.WHITE:
                arcade.draw_rect_filled(
                    arcade.XYWH(
                        self.width * 3 / 2,
                        self.height / 2,
                        self.width * 3,
                        self.height,
                    ),
                    color=(255, 255, 255, self.fade_in),
                )
            else:
                arcade.draw_rect_filled(
                    arcade.XYWH(
                        self.width * 3 / 2,
                        self.height / 2,
                        self.width * 3,
                        self.height,
                    ),
                    color=(0, 0, 0, self.fade_in),
                )
