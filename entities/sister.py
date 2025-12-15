import arcade
from constants import *


class Sister(arcade.Sprite):
    def __init__(self):
        self.health = 55
        self.loss_rate = 4
        self.loss_time = 0
        self.alive = True
        self.up = UP_TEXTURE
        self.towards = TOWARDS_TEXTURE
        self.away = AWAY_TEXTURE
        self.dead = DEAD_TEXTURE
        self.gone = GONE_TEXTURE

        super().__init__(self.towards, scale=CHARACTER_SCALE, center_x=75, center_y=98)

    def update(self, delta_time=1 / 60, *args, **kwargs):
        self.loss_time += delta_time
        if self.loss_time >= self.loss_rate:
            self.loss_time = 0
            self.health -= 1
        if self.health == 0:
            self.alive = False
            self.texture = self.away
