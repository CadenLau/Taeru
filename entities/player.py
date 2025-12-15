import arcade
from constants import *


class Player(arcade.Sprite):
    def __init__(self):
        self.idle = IDLE_TEXTURE
        self.walk = WALK_TEXTURE
        self.carry_idle = CARRY_IDLE_TEXTURE
        self.carry_walk = CARRY_WALK_TEXTURE
        self.over_sister = OVER_SISTER_TEXTURE
        self.back = BACK_TEXTURE
        self.walk_speed = 2
        self.walking = False
        self.time_walking = 0
        self.carrying_sister = False
        self.in_shelter = False
        self.key_pressed = {"left": False, "right": False}
        self.last_key_pressed = None

        super().__init__(self.idle, scale=6, center_x=800, center_y=119)

    def update(self, delta_time=1 / 60, *args, **kwargs):

        # Movement based on which key was pressed last if both keys are pressed
        if self.key_pressed["left"] and (
            self.last_key_pressed == "left" or not self.key_pressed["right"]
        ):
            self.change_x = -self.walk_speed
            if self.carrying_sister:
                self.scale_x = -CHARACTER_SCALE
        if self.key_pressed["right"] and (
            self.last_key_pressed == "right" or not self.key_pressed["left"]
        ):
            self.change_x = self.walk_speed
            if self.carrying_sister:
                self.scale_x = CHARACTER_SCALE

        if self.walking:
            self.time_walking += delta_time
            if self.time_walking > 0.8 / self.walk_speed:
                self.time_walking = 0
                if not self.carrying_sister:
                    if self.texture == self.idle:
                        self.texture = self.walk
                    else:
                        self.texture = self.idle
                else:
                    if self.texture == self.carry_idle:
                        self.texture = self.carry_walk
                    else:
                        self.texture = self.carry_idle

    def on_key_press(self, key) -> None:
        if key == arcade.key.D:
            self.key_pressed["right"] = True
            self.last_key_pressed = "right"

            self.walking = True
            if not self.carrying_sister:
                self.texture = self.walk
            else:
                self.texture = self.carry_walk

        elif key == arcade.key.A:
            self.key_pressed["left"] = True
            self.last_key_pressed = "left"

            self.walking = True
            if not self.carrying_sister:
                self.texture = self.walk
            else:
                self.texture = self.carry_walk

    def on_key_release(self, key) -> None:
        if key in (arcade.key.A, arcade.key.D):
            if key == arcade.key.A:
                self.key_pressed["left"] = False
            else:
                self.key_pressed["right"] = False

            if not self.key_pressed["left"] and not self.key_pressed["right"]:
                self.change_x = 0
                if not self.carrying_sister:
                    self.texture = self.idle
                else:
                    self.texture = self.carry_idle
                self.walking = False
                self.time_walking = 0

    def enter_shelter(self) -> None:
        self.in_shelter = True
        self.color = (128, 128, 128)
        self.center_y = 283

    def leave_shelter(self, shelter_center_x) -> None:
        self.carrying_sister = False
        self.texture = self.idle
        self.center_x = shelter_center_x
        self.center_y = 119
        self.scale_x = CHARACTER_SCALE
        self.in_shelter = False
        self.color = (255, 255, 255)
