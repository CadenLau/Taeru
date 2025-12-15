import arcade
from pyglet.graphics import Batch
from constants import *
from views.controls_view import ControlsView
from utils.fade import FadingView

TITLE_SIZE = 50
ENTER_SIZE = 30


class MenuView(FadingView):
    def __init__(self):
        super().__init__()
        self.fade_alpha = 0

        self.batch = Batch()
        self.title = arcade.Text(
            SCREEN_TITLE,
            WINDOW_WIDTH / 2,
            2 * WINDOW_HEIGHT / 3,
            arcade.color.WHITE,
            TITLE_SIZE,
            anchor_x="center",
            batch=self.batch,
            font_name="Pixel",
        )
        self.press_text = arcade.Text(
            "Press SPACE to begin",
            WINDOW_WIDTH / 2,
            WINDOW_HEIGHT / 2,
            arcade.color.WHITE,
            ENTER_SIZE,
            anchor_x="center",
            batch=self.batch,
            font_name="Pixel",
        )

        # Background
        self.background = arcade.SpriteList()
        self.far_background = arcade.Sprite(
            FAR_BACKGROUND_TEXTURE,
            scale=BACKGROUND_SCALE,
            center_x=WINDOW_WIDTH,
            center_y=WINDOW_HEIGHT / 2,
        )
        self.near_background = arcade.Sprite(
            NEAR_BACKGROUND_TEXTURE,
            scale=BACKGROUND_SCALE,
            center_x=WINDOW_WIDTH,
            center_y=WINDOW_HEIGHT / 2,
        )
        self.ground = arcade.Sprite(
            GROUND_TEXTURE,
            scale=BACKGROUND_SCALE,
            center_x=3 * WINDOW_WIDTH / 2,
            center_y=40,
        )
        self.background.append(self.far_background)
        self.background.append(self.near_background)
        self.background.append(self.ground)

        self.music = arcade.play_sound(TITLE_MUSIC, volume=VOLUME * 2, loop=True)

    def on_update(self, delta_time):
        self.update_fade()

    def on_draw(self):
        self.clear()
        self.window.ctx.scissor = self.window.camera.viewport
        self.window.camera.use()
        self.background.draw(pixelated=True)
        self.batch.draw()
        self.draw_fading()
        self.window.ctx.scissor = None

    def on_key_press(self, symbol, modifiers):
        if not symbol == arcade.key.ESCAPE:
            arcade.stop_sound(self.music)
            self.window.show_view(ControlsView())
