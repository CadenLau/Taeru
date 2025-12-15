import arcade
import views.view_holder
from pyglet.graphics import Batch
from constants import *


class EndingView(arcade.View):
    def __init__(self):
        super().__init__()
        self.time = 0
        self.continue_after = 15

        self.batch1 = Batch()
        self.et_fade_in = 0
        self.end_text = arcade.Text(
            "Thank you for playing",
            WINDOW_WIDTH / 2,
            WINDOW_HEIGHT / 2 + 20,
            (0, 0, 0, self.et_fade_in),
            44,
            align="center",
            anchor_x="center",
            anchor_y="center",
            batch=self.batch1,
            font_name="Pixel",
            multiline=True,
            width=1100,
        )
        self.batch2 = Batch()
        self.ct_fade_in = 0
        self.continue_text = arcade.Text(
            "Press [SPACE] to continue",
            WINDOW_WIDTH / 2,
            WINDOW_HEIGHT / 4,
            (0, 0, 0, self.ct_fade_in),
            30,
            align="center",
            anchor_x="center",
            anchor_y="center",
            batch=self.batch2,
            font_name="Pixel",
        )

        self.end_drone = arcade.play_sound(END_DRONE, volume=VOLUME / 3.5)

    def on_draw(self):
        self.clear()
        self.window.ctx.scissor = self.window.camera.viewport
        self.window.camera.use()
        arcade.draw_lbwh_rectangle_filled(
            0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, arcade.color.WHITE
        )
        self.batch1.draw()
        if self.time >= self.continue_after:
            self.batch2.draw()
        self.window.ctx.scissor = None

    def on_update(self, delta_time):
        self.time += delta_time

        if not self.et_fade_in == None:
            self.et_fade_in += FADE_RATE
            if self.et_fade_in >= 255:
                self.et_fade_in = None
                self.end_text.color = (0, 0, 0)
            else:
                self.end_text.color = (0, 0, 0, self.et_fade_in)

        if self.time >= self.continue_after and not self.ct_fade_in == None:
            self.ct_fade_in += FADE_RATE
            if self.ct_fade_in >= 255:
                self.ct_fade_in = None
                self.continue_text.color = (0, 0, 0)
            else:
                self.continue_text.color = (0, 0, 0, self.ct_fade_in)

    def on_key_press(self, key, modifiers):
        if self.time >= self.continue_after and not key == arcade.key.ESCAPE:
            if self.end_drone:
                arcade.stop_sound(self.end_drone)
            self.window.show_view(views.view_holder.menu_view)
