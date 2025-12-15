import arcade
from pyglet.graphics import Batch
from constants import *
from views.game_view import GameView
from utils.fade import FadingView

TITLE_FONT_SIZE = 36
CONTROLS_FONT_SIZE = 30
DESCRIPTION_FONT_SIZE = 24
DESCRIPTION_WIDTH = 450


class ControlsView(FadingView):
    def __init__(self):
        super().__init__()
        self.fade_alpha = 0
        self.time = 0

        self.batch = Batch()
        self.title = arcade.Text(
            "Controls",
            WINDOW_WIDTH / 2,
            WINDOW_HEIGHT / 2 + 250,
            arcade.color.WHITE,
            TITLE_FONT_SIZE,
            anchor_x="center",
            anchor_y="center",
            batch=self.batch,
            font_name="Pixel",
        )
        self.ad_control = arcade.Text(
            "A  /  D",
            WINDOW_WIDTH / 3,
            WINDOW_HEIGHT / 2 + 100,
            arcade.color.WHITE,
            CONTROLS_FONT_SIZE,
            anchor_x="center",
            anchor_y="center",
            batch=self.batch,
            font_name="Pixel",
        )
        self.ad_description = arcade.Text(
            "Left/Right Movement",
            WINDOW_WIDTH * 2 / 3,
            WINDOW_HEIGHT / 2 + 100,
            arcade.color.WHITE,
            DESCRIPTION_FONT_SIZE,
            anchor_x="center",
            anchor_y="center",
            batch=self.batch,
            font_name="Pixel",
            multiline=True,
            width=DESCRIPTION_WIDTH,
        )
        self.enter_control = arcade.Text(
            "E",
            WINDOW_WIDTH / 3,
            WINDOW_HEIGHT / 2 - 50,
            arcade.color.WHITE,
            CONTROLS_FONT_SIZE,
            anchor_x="center",
            anchor_y="center",
            batch=self.batch,
            font_name="Pixel",
        )
        self.enter_description = arcade.Text(
            "Interact with environment",
            WINDOW_WIDTH * 2 / 3,
            WINDOW_HEIGHT / 2 - 50,
            arcade.color.WHITE,
            DESCRIPTION_FONT_SIZE,
            anchor_x="center",
            anchor_y="center",
            batch=self.batch,
            font_name="Pixel",
            multiline=True,
            width=DESCRIPTION_WIDTH,
        )
        self.space_control = arcade.Text(
            "SPACE",
            WINDOW_WIDTH / 3,
            WINDOW_HEIGHT / 2 - 200,
            arcade.color.WHITE,
            CONTROLS_FONT_SIZE,
            anchor_x="center",
            anchor_y="center",
            batch=self.batch,
            font_name="Pixel",
        )
        self.space_description = arcade.Text(
            "Scroll through dialogue",
            WINDOW_WIDTH * 2 / 3,
            WINDOW_HEIGHT / 2 - 200,
            arcade.color.WHITE,
            DESCRIPTION_FONT_SIZE,
            anchor_x="center",
            anchor_y="center",
            batch=self.batch,
            font_name="Pixel",
            multiline=True,
            width=DESCRIPTION_WIDTH,
        )

        self.outlines = arcade.shape_list.ShapeElementList()
        self.a_outline = arcade.shape_list.create_rectangle_outline(
            WINDOW_WIDTH / 3 - 68,
            WINDOW_HEIGHT / 2 + 100 - 10,
            width=55,
            height=55,
            color=arcade.color.WHITE,
            border_width=6,
        )
        self.d_outline = arcade.shape_list.create_rectangle_outline(
            WINDOW_WIDTH / 3 + 59,
            WINDOW_HEIGHT / 2 + 100 - 10,
            width=55,
            height=55,
            color=arcade.color.WHITE,
            border_width=6,
        )
        self.e_outline = arcade.shape_list.create_rectangle_outline(
            WINDOW_WIDTH / 3 - 4,
            WINDOW_HEIGHT / 2 - 50 - 10,
            width=55,
            height=55,
            color=arcade.color.WHITE,
            border_width=6,
        )
        self.space_outline = arcade.shape_list.create_rectangle_outline(
            WINDOW_WIDTH / 3 - 4,
            WINDOW_HEIGHT / 2 - 200 - 10,
            width=200,
            height=55,
            color=arcade.color.WHITE,
            border_width=6,
        )

        self.outlines.append(self.a_outline)
        self.outlines.append(self.d_outline)
        self.outlines.append(self.e_outline)
        self.outlines.append(self.space_outline)

    def on_update(self, delta_time):
        self.update_fade()

        self.time += delta_time
        if self.time >= 10:
            self.window.show_view(GameView())

    def on_draw(self):
        self.clear()
        self.window.ctx.scissor = self.window.camera.viewport
        self.window.camera.use()
        self.outlines.draw()
        self.batch.draw()
        self.draw_fading()
        self.window.ctx.scissor = None

    # def on_key_press(self, symbol, modifiers):  # for testing
    #     self.window.show_view(GameView())
