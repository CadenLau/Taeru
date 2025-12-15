import arcade
import json
from constants import *

with open(os.path.join(BASE_PATH, "data", "dialogue.json"), "r") as f:
    DIALOGUE = json.load(f)


class DialogueBox:
    def __init__(self, event, key, camera: arcade.Camera2D):
        self.lines = DIALOGUE[event][key]
        self.index = 0
        self.camera = camera

    @property
    def text(self):
        return self.lines[self.index]

    def next_line(self):
        self.index += 1
        if self.index >= len(self.lines):
            self.index -= 1  # Prevents errors
            return False
        return True

    def draw(self):
        width = 1000
        height = 140
        x = self.camera.position.x
        y = 3 * WINDOW_HEIGHT / 4
        arcade.shape_list.create_rectangle_filled(
            x, y, width, height, (0, 0, 0, 180)
        ).draw()
        arcade.shape_list.create_rectangle_outline(
            x, y, width, height, (255, 255, 255, 180), 8
        ).draw()
        arcade.Text(
            self.text,
            x - width / 2 + 20,
            y + 30,
            arcade.color.WHITE,
            DIALOGUE_FONT_SIZE,
            font_name="Pixel",
        ).draw()
        arcade.Text(
            "[SPACE] Continue",
            x + width / 4 + 10,
            y - 45,
            arcade.color.LIGHT_GRAY,
            PRESS_FONT_SIZE,
            font_name="Pixel",
        ).draw()
