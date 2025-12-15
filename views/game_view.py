import arcade
import random
from pyglet.graphics import Batch
from views.ending_view import EndingView
from utils.dialogue_box import DialogueBox
from utils.fade import FadingView
from constants import *
from entities.player import Player
from entities.sister import Sister


class GameView(FadingView):
    def __init__(self):
        super().__init__()

        # Game stats
        self.medicine = 0
        self.food = 1
        self.total_time = 0

        # Sounds
        self.music = arcade.play_sound(GAME_MUSIC, volume=VOLUME, loop=True)
        self.siren_only = None
        self.shelter_bombs = None

        # State flags
        self.scene_state = "OPENING"
        self.scene_time = 0
        self.scene_phase = 0

        self.dialogue_box = None

        self.air_raid = False
        self.air_raid_transition = False
        self.first_air_raid = True
        self.next_air_raid = random.uniform(90, 120)
        self.final_air_raid = 10000  # Will be set after sister death

        self.food_available = True
        self.food_time = 0

        self.delivery_phase = 0
        self.doing_delivery = False

        # Load player
        self.player = Player()

        # Ground
        self.ground = arcade.Sprite(
            GROUND_TEXTURE,
            scale=BACKGROUND_SCALE,
            center_x=3 * WINDOW_WIDTH / 2,
            center_y=40,
        )

        # Background
        self.far_background = arcade.Sprite(
            FAR_BACKGROUND_TEXTURE,
            scale=BACKGROUND_SCALE,
            center_x=WINDOW_WIDTH,
            center_y=WINDOW_HEIGHT / 2,
        )
        self.far_background_speed = 0.7
        self.near_background = arcade.Sprite(
            NEAR_BACKGROUND_TEXTURE,
            scale=BACKGROUND_SCALE,
            center_x=WINDOW_WIDTH,
            center_y=WINDOW_HEIGHT / 2,
        )
        self.near_background_speed = 0.5

        # Inner Shelter
        self.shelter_center_x = 1500
        self.inner_shelter = arcade.Sprite(
            INNER_SHELTER_TEXTURE,
            scale=BACKGROUND_SCALE,
            center_x=self.shelter_center_x,
            center_y=WINDOW_HEIGHT / 2,
        )

        # Buildings
        self.shelter = arcade.Sprite(
            SHELTER_TEXTURE,
            scale=BUILDING_SCALE / 2,
            center_x=self.shelter_center_x,
            center_y=144,
        )
        self.house = arcade.Sprite(
            HOUSE_TEXTURE, scale=BUILDING_SCALE, center_x=200, center_y=216
        )
        self.hospital = arcade.Sprite(
            HOSPITAL_OKAY_TEXTURE,
            scale=BUILDING_SCALE,
            center_x=2100,
            center_y=288,
        )
        self.food_stand = arcade.Sprite(
            FOOD_STAND_TEXTURE,
            scale=BUILDING_SCALE / 2,
            center_x=3700,
            center_y=144,
        )
        self.elderly_lady_house = arcade.Sprite(
            ELDERLY_LADY_HOUSE_TEXTURE,
            scale=BUILDING_SCALE,
            center_x=3200,
            center_y=256,
        )

        # Characters
        self.sister = Sister()
        self.food_rationer_pos = 3700, 119
        self.food_rationer = arcade.Sprite(
            FOOD_RATIONER_TEXTURE,
            scale=CHARACTER_SCALE,
        )
        self.food_rationer.position = self.food_rationer_pos
        self.doctor_pos = 2150, 119
        self.doctor = arcade.Sprite(
            DOCTOR_TEXTURE,
            scale=CHARACTER_SCALE,
        )
        self.doctor.position = self.doctor_pos
        self.elderly_pos = 3010, 116
        self.elderly_lady = arcade.Sprite(
            ELDERLY_LADY_TEXTURE,
            scale=CHARACTER_SCALE,
        )
        self.elderly_lady.position = self.elderly_pos
        self.young_boy_pos = 2500, 107
        self.young_boy = arcade.Sprite(
            YOUNG_BOY_TEXTURE,
            scale=CHARACTER_SCALE,
        )
        self.young_boy.position = self.young_boy_pos
        self.dude_pos = 1350, 119
        self.dude = arcade.Sprite(
            DUDE_TEXTURE,
            scale=CHARACTER_SCALE,
        )
        self.dude.position = self.dude_pos

        # Setup scene
        self.scene = arcade.Scene()
        self.scene.add_sprite("Far background", self.far_background)
        self.scene.add_sprite("Near background", self.near_background)
        self.scene.add_sprite("Shelter", self.shelter)
        self.scene.add_sprite("Hospital", self.hospital)
        self.scene.add_sprite("Food rationer", self.food_rationer)
        self.scene.add_sprite("Food stand", self.food_stand)
        self.scene.add_sprite("Elderly lady house", self.elderly_lady_house)
        self.scene.add_sprite("Ground", self.ground)
        self.scene.add_sprite("House", self.house)
        self.scene.add_sprite("Doctor", self.doctor)
        self.scene.add_sprite("Elderly lady", self.elderly_lady)
        self.scene.add_sprite("Young boy", self.young_boy)
        self.scene.add_sprite("Dude", self.dude)
        self.scene.add_sprite("Sister", self.sister)
        self.scene.add_sprite("Player", self.player)

        self.shelter_scene = arcade.Scene()
        self.shelter_scene.add_sprite("Inner shelter", self.inner_shelter)
        self.shelter_scene.add_sprite("Food rationer", self.food_rationer)
        self.shelter_scene.add_sprite("Doctor", self.doctor)
        self.shelter_scene.add_sprite("Elderly lady", self.elderly_lady)
        self.shelter_scene.add_sprite("Young boy", self.young_boy)
        self.shelter_scene.add_sprite("Dude", self.dude)
        self.shelter_scene.add_sprite("Player", self.player)

        self.final_bomb = None

        # Physics
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player, arcade.SpriteList([self.ground])
        )

        # UI
        self.batch = Batch()
        self.ui = arcade.Text(
            f"Medicine: {self.medicine}  |  Food: {self.food}  |  Sister: {int(self.sister.health)}%",
            20,
            WINDOW_HEIGHT - 40,
            arcade.color.WHITE,
            ITEMS_FONT_SIZE,
            batch=self.batch,
            font_name="Pixel",
        )

        # Camera
        self.camera_bounds = arcade.LRBT(
            WINDOW_WIDTH / 2.0,
            self.ground.width - WINDOW_WIDTH / 2.0,
            WINDOW_HEIGHT / 2.0,
            WINDOW_HEIGHT / 2.0,
        )

    def on_draw(self):
        self.clear()
        self.window.ctx.scissor = self.window.camera.viewport
        self.window.camera.use()
        if not (self.scene_state == "ENDING" and self.scene_phase >= 10):
            if self.player.in_shelter:
                self.shelter_scene.draw(pixelated=True)
            elif self.player.carrying_sister:
                self.scene.draw(
                    names=[
                        "Far background",
                        "Near background",
                        "Shelter",
                        "Hospital",
                        "Food stand",
                        "Elderly lady house",
                        "Ground",
                        "House",
                        "Doctor",
                        "Elderly lady",
                        "Young boy",
                        "Dude",
                        "Player",
                    ],
                    pixelated=True,
                )
            else:
                self.scene.draw(pixelated=True)

            # Update UI text before drawing
            self.ui.text = f"Medicine: {self.medicine}  |  Food: {self.food}  |  Sister health: {int(self.sister.health)}%"
            self.batch.draw()
        else:
            arcade.draw_lbwh_rectangle_filled(
                0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, arcade.color.WHITE
            )

        if self.dialogue_box:
            self.dialogue_box.draw()

        self.draw_fading()

        self.window.ctx.scissor = None

    def on_update(self, delta_time):
        self.update_fade()
        # In case update at end of function isn't reached
        self.ui.text = f"Medicine: {self.medicine}  |  Food: {self.food}  |  Sister health: {int(self.sister.health)}%"

        if self.air_raid:
            if not self.siren_only.playing and not self.shelter_bombs.playing:
                self.air_raid = False
                self.air_raid_transition = True
                self.dialogue_box = DialogueBox("air_raid", "end", self.window.camera)

        if self.dialogue_box:
            return  # pause gameplay during dialogue

        if self.air_raid_transition:
            self.air_raid_transition = False
            self.leave_shelter()

        self.player.update(delta_time=delta_time)
        self.physics_engine.update()

        if self.scene_state == "OPENING":
            self.update_opening(delta_time)
            return
        elif self.scene_state == "SISTER DEATH":
            self.update_sister_death(delta_time)
            return
        elif self.scene_state == "ENDING":
            self.update_ending(delta_time)
            return

        if not self.air_raid:
            self.total_time += delta_time

        # Sister life status and health decay
        if not self.air_raid:  # Pause during air raid to prevent bugs
            if self.sister.alive:
                self.sister.update(delta_time=delta_time)
                if self.total_time >= 300:
                    self.sister.loss_rate = 2
                elif self.total_time >= 150:
                    self.sister.loss_rate = 3
            if not self.sister.alive and not (
                self.sister.texture in (self.sister.dead, self.sister.gone)
            ):
                self.scene_state = "SISTER DEATH"
                self.player.on_key_release(arcade.key.A)
                self.player.on_key_release(arcade.key.D)
                return
            if (
                self.sister.texture == self.sister.dead and self.player.center_x >= 900
            ):  # Placed here rather than at end of scene animation for slightly smoother texture swap
                self.sister.texture = self.sister.gone
            if (
                self.sister.texture == self.sister.away and self.player.center_x >= 900
            ):  # Swap textures once sister is off screen after opening cut scene
                self.sister.texture = self.sister.up

        # Trigger ending sequence
        if self.total_time >= self.final_air_raid and self.player.center_x > 2700:
            self.scene_state = "ENDING"
            self.player.on_key_release(arcade.key.A)
            self.player.on_key_release(arcade.key.D)
            arcade.stop_sound(self.music)
            return

        # Food ration availability
        if not self.food_available:
            self.food_time += delta_time
            if self.food_time >= 90:
                self.food_available = True
                self.food_time = 0

        # Random air raid trigger
        if self.total_time > self.next_air_raid:
            self.trigger_air_raid()

        self.move_camera()

        if self.player.in_shelter:
            self.player.center_x = arcade.math.clamp(
                self.player.center_x,
                self.inner_shelter.center_x
                - self.inner_shelter.width / 2
                + 8 * BACKGROUND_SCALE
                + abs(self.player.width / 2),
                self.inner_shelter.center_x
                + self.inner_shelter.width / 2
                - 5 * BACKGROUND_SCALE
                - abs(self.player.width / 2),
            )
        else:
            self.player.center_x = arcade.math.clamp(
                self.player.center_x,
                abs(self.player.width / 2),
                self.ground.width - abs(self.player.width / 2),
            )

        # Update UI text after everything
        self.ui.text = f"Medicine: {self.medicine}  |  Food: {self.food}  |  Sister health: {int(self.sister.health)}%"

    def update_opening(self, delta_time) -> None:
        if self.scene_time == 0 and self.scene_phase == 0:
            self.player.on_key_press(arcade.key.A)
            self.scene_phase += 1

        self.scene_time += delta_time

        if self.scene_time >= 5.9 and self.scene_phase == 1:
            self.player.on_key_release(arcade.key.A)
            self.scene_phase += 1
        if self.scene_time >= 6.5 and self.scene_phase == 2:
            self.scene_phase += 1
            self.food -= 1
            self.sister.health += 5
            self.dialogue_box = DialogueBox("sister", "opening1", self.window.camera)
        if self.scene_time >= 8 and self.scene_phase == 3:
            self.scene_phase += 1
            self.sister.texture = self.sister.up
        if self.scene_time >= 10 and self.scene_phase == 4:
            self.scene_phase += 1
            self.dialogue_box = DialogueBox("sister", "opening2", self.window.camera)
        if self.scene_time >= 12 and self.scene_phase == 5:
            self.scene_phase += 1
            self.dialogue_box = DialogueBox("sister", "opening3", self.window.camera)
        if self.scene_time >= 15 and self.scene_phase == 6:
            self.scene_phase += 1
            self.sister.texture = self.sister.towards
        if self.scene_time >= 16 and self.scene_phase == 7:
            self.scene_phase += 1
            self.dialogue_box = DialogueBox("sister", "opening4", self.window.camera)
        if self.scene_time >= 16.5 and self.scene_phase == 8:
            self.scene_phase += 1
            self.sister.texture = self.sister.away
        if self.scene_time >= 19 and self.scene_phase == 9:
            self.scene_phase += 1
            self.dialogue_box = DialogueBox("sister", "opening5", self.window.camera)
        if self.scene_time >= 22 and self.scene_phase == 10:
            self.scene_phase += 1
            self.dialogue_box = DialogueBox("sister", "opening6", self.window.camera)
        if self.scene_time >= 22.1 and self.scene_phase == 11:
            self.scene_phase = 0
            self.scene_time = 0
            self.scene_state = "GAMEPLAY"

    def update_sister_death(self, delta_time) -> None:
        if self.scene_phase == 0:
            if self.player.center_x > 94:
                if not self.player.key_pressed["left"]:
                    self.player.on_key_press(arcade.key.A)
                self.move_camera()
                return

            elif self.player.center_x < 92:
                if not self.player.key_pressed["right"]:
                    self.player.on_key_press(arcade.key.D)
                self.move_camera()
                return

            else:
                self.scene_phase += 1
                self.player.on_key_release(arcade.key.A)
                self.player.on_key_release(arcade.key.D)

        self.scene_time += delta_time

        if self.scene_time >= 2 and self.scene_phase == 1:
            self.scene_phase += 1
            self.sister.texture = self.sister.dead
            arcade.stop_sound(self.music)
            # self.music.pause()
        if self.scene_time >= 4 and self.scene_phase == 2:
            self.scene_phase += 1
            self.player.texture = self.player.over_sister
        if self.scene_time >= 9 and self.scene_phase == 3:
            self.scene_phase += 1
            self.dialogue_box = DialogueBox("sister", "death1", self.window.camera)
        if self.scene_time >= 14 and self.scene_phase == 4:
            self.scene_phase += 1
            self.player.idle = AFTER_DEATH_IDLE_TEXTURE
            self.player.walk = AFTER_DEATH_WALK_TEXTURE
            self.player.texture = self.player.idle
            self.player.walk_speed = 1
            self.player.scale_x = -CHARACTER_SCALE
        if self.scene_time >= 17 and self.scene_phase == 5:
            self.scene_phase += 1
            self.player.scale_x = CHARACTER_SCALE
            self.player.on_key_press(arcade.key.D)
        if self.scene_time >= 22 and self.scene_phase == 6:
            self.scene_phase += 1
            self.player.on_key_release(arcade.key.D)
        if self.scene_time >= 25 and self.scene_phase == 7:
            self.scene_phase += 1
            self.player.scale_x = -CHARACTER_SCALE
        if self.scene_time >= 28 and self.scene_phase == 8:
            self.scene_phase += 1
            self.dialogue_box = DialogueBox("sister", "death2", self.window.camera)
        if self.scene_time >= 30 and self.scene_phase == 9:
            self.scene_phase += 1
            self.player.scale_x = CHARACTER_SCALE
        if self.scene_time >= 32 and self.scene_phase == 10:
            self.scene_phase += 1
            self.player.on_key_press(arcade.key.D)
        if self.scene_time >= 39.5 and self.scene_phase == 11:
            self.scene_phase += 1
            self.player.on_key_release(arcade.key.D)
        if self.scene_time >= 44.5 and self.scene_phase == 12:
            self.scene_phase += 1
            self.player.on_key_press(arcade.key.D)
        if self.scene_time >= 53.9 and self.scene_phase == 13:
            self.scene_phase = 0
            self.scene_time = 0
            self.scene_state = "GAMEPLAY"
            self.player.idle = IDLE_TEXTURE
            self.player.walk = WALK_TEXTURE
            self.player.on_key_release(arcade.key.D)
            self.player.walk_speed = 1.5
            # Make next air raid never happen
            self.next_air_raid = 10000
            self.final_air_raid = self.total_time + 75
            # self.music.play()
            self.music = arcade.play_sound(
                AFTER_DEATH_MUSIC, volume=VOLUME * 4, loop=True
            )

    def update_ending(self, delta_time) -> None:
        if self.player.center_x > 2500:
            if self.scene_phase == 0:
                self.scene_phase += 1
                self.player.on_key_press(arcade.key.A)
                self.dialogue_box = DialogueBox("ending", "zero", self.window.camera)
            self.move_camera()
            return
        if self.scene_phase == 1:
            self.scene_phase += 1
            self.player.walk_speed = 1.25
            self.dialogue_box = DialogueBox("ending", "one", self.window.camera)

        if self.scene_phase != 9:
            self.scene_time += delta_time

        if self.scene_time >= 3 and self.scene_phase == 2:
            self.scene_phase += 1
            self.player.walk_speed = 1
            self.dialogue_box = DialogueBox("ending", "two", self.window.camera)
        if self.scene_time >= 7 and self.scene_phase == 3:
            self.scene_phase += 1
            self.player.walk_speed = 0.75
            self.dialogue_box = DialogueBox("ending", "three", self.window.camera)
        if self.scene_time >= 12 and self.scene_phase == 4:
            self.scene_phase += 1
            self.player.walk_speed = 0.5
            self.dialogue_box = DialogueBox("ending", "four", self.window.camera)
        if self.scene_time >= 17.5 and self.scene_phase == 5:
            self.scene_phase += 1
            self.player.on_key_release(arcade.key.A)
            self.dialogue_box = DialogueBox("ending", "five", self.window.camera)
        if self.scene_time >= 21 and self.scene_phase == 6:
            self.scene_phase += 1
            self.player.texture = self.player.back
        if self.scene_time >= 26 and self.scene_phase == 7:
            self.scene_phase += 1
            self.dialogue_box = DialogueBox("ending", "six", self.window.camera)
        if self.scene_time >= 29 and self.scene_phase == 8:
            self.scene_phase += 1
            self.final_bomb = arcade.Sprite(
                BOMB_TEXTURE,
                scale=BACKGROUND_SCALE / 4,
                center_x=self.player.center_x - 10,
                center_y=WINDOW_HEIGHT,
                angle=90,
            )
            self.scene.add_sprite_list_after(
                "Bomb",
                "Near background",
            )
            self.scene.add_sprite("Bomb", self.final_bomb)
        if self.scene_phase == 9:
            if arcade.check_for_collision(self.final_bomb, self.near_background):
                self.scene_phase += 1
                self.window.camera.position = WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2
                self.window.camera.use()
            self.final_bomb.center_x += 0.25
            self.final_bomb.center_y -= 2.5
        if self.scene_time >= 31 and self.scene_phase == 10:
            self.scene_phase += 1
            arcade.play_sound(ENDING_BOMBS, volume=VOLUME * 2)
        if self.scene_time >= 33 and self.scene_phase == 11:
            self.scene_phase += 1
            self.dialogue_box = DialogueBox("ending", "seven", self.window.camera)
        if self.scene_time >= 37 and self.scene_phase == 12:
            self.window.show_view(EndingView())

        if self.scene_phase < 9:
            self.move_camera()

    def move_camera(self) -> None:
        # Save old position for parallax scrolling
        old_position = self.window.camera.position
        self.pan_camera_to_player(CAMERA_PAN_SPEED)
        self.move_text_with_camera()
        self.scroll_background(old_position)

    def move_text_with_camera(self) -> None:
        self.ui.x = self.window.camera.center_left.x + 20

    def scroll_background(self, old_position) -> None:
        position_difference = self.window.camera.position - old_position
        self.near_background.center_x += (
            position_difference.x * self.near_background_speed
        )
        self.far_background.center_x += (
            position_difference.x * self.far_background_speed
        )

    def pan_camera_to_player(self, panning_fraction: float = 1.0) -> None:
        self.window.camera.position = arcade.math.smerp_2d(
            self.window.camera.position,
            self.player.position,
            self.window.delta_time,
            panning_fraction,
        )
        self.window.camera.position = arcade.camera.grips.constrain_xy(
            self.window.camera.view_data, self.camera_bounds
        )

    def trigger_air_raid(self) -> None:
        self.music.pause()
        self.siren_only = arcade.play_sound(SIREN_ONLY, volume=VOLUME, loop=True)
        self.dialogue_box = DialogueBox(
            "air_raid",
            "trigger",
            self.window.camera,
        )
        self.next_air_raid = self.total_time + random.uniform(120, 150)
        self.air_raid = True

    def on_key_press(self, key, modifiers) -> None:
        if key == arcade.key.SPACE and self.dialogue_box:
            if not self.dialogue_box.next_line():
                self.dialogue_box = None
        if not self.scene_state == "GAMEPLAY":
            return
        if not self.dialogue_box:
            self.player.on_key_press(key)
            if key == arcade.key.E:
                if arcade.check_for_collision(self.player, self.food_stand):
                    self.food_stand_interaction()
                elif arcade.check_for_collision(
                    self.player, self.dude
                ):  # Must be above food rationer for best in shelter interaction
                    self.dude_interaction()
                elif arcade.check_for_collision(self.player, self.food_rationer):
                    self.food_rationer_interaction()
                elif arcade.check_for_collision(self.player, self.sister):
                    self.sister_interaction()
                elif arcade.check_for_collision(
                    self.player, self.young_boy
                ):  # Must be above elderly lady and doctor for best in shelter interaction
                    self.young_boy_interaction()
                elif arcade.check_for_collision(self.player, self.doctor):
                    self.doctor_interaction()
                elif arcade.check_for_collision(self.player, self.elderly_lady):
                    self.elderly_lady_interaction()
                elif self.air_raid and arcade.check_for_collision(
                    self.player, self.shelter
                ):
                    self.shelter_interaction()

    def enter_shelter(self) -> None:
        self.fade_in = 255
        self.player.enter_shelter()
        self.food_rationer.position = self.inner_shelter.center_x - 100, 283
        self.food_rationer.color = (128, 128, 128)
        self.doctor.position = self.inner_shelter.center_x + 50, 283
        self.doctor.color = (128, 128, 128)
        self.elderly_lady.position = self.inner_shelter.center_x + 160, 280
        self.elderly_lady.color = (128, 128, 128)
        self.young_boy.position = self.inner_shelter.center_x + 110, 271
        self.young_boy.color = (128, 128, 128)
        self.dude.position = self.inner_shelter.center_x - 150, 283
        self.dude.color = (128, 128, 128)
        arcade.stop_sound(self.siren_only)
        if self.first_air_raid:
            self.first_air_raid = False
            self.shelter_bombs = arcade.play_sound(
                SIREN_WITH_PLANES,
                volume=VOLUME,
            )
        else:
            num = random.random()
            if num > 0.5:
                self.shelter_bombs = arcade.play_sound(
                    SHELTER_SHORT,
                    volume=VOLUME,
                )
            else:
                self.shelter_bombs = arcade.play_sound(
                    SHELTER_LONG,
                    volume=VOLUME,
                )
            if (
                self.hospital.texture == HOSPITAL_OKAY_TEXTURE
            ):  # Change hospital after second air raid
                self.hospital.texture = HOSPITAL_BOMBED_TEXTURE

        self.dialogue_box = DialogueBox("air_raid", "enter_shelter", self.window.camera)

    def leave_shelter(self) -> None:
        self.fade_in = 255
        self.player.leave_shelter(self.shelter_center_x)
        self.food_rationer.position = self.food_rationer_pos
        self.food_rationer.color = (255, 255, 255)
        self.doctor.position = self.doctor_pos
        self.doctor.color = (255, 255, 255)
        self.elderly_lady.position = self.elderly_pos
        self.elderly_lady.color = (255, 255, 255)
        self.young_boy.position = self.young_boy_pos
        self.young_boy.color = (255, 255, 255)
        self.dude.position = self.dude_pos
        self.dude.color = (255, 255, 255)
        self.music.play()

    def food_stand_interaction(self) -> None:
        if not self.sister.alive:
            self.dialogue_box = DialogueBox(
                "food_stand", "sister_dead", self.window.camera
            )
        elif self.air_raid:
            self.dialogue_box = DialogueBox(
                "food_stand", "air_raid", self.window.camera
            )
        elif self.doing_delivery and self.delivery_phase == 3:
            self.dialogue_box = DialogueBox(
                "food_stand",
                "delivery",
                self.window.camera,
            )
            self.doing_delivery = False
            self.medicine -= 1
        else:
            if self.food_available:
                self.dialogue_box = DialogueBox(
                    "food_stand", "has_rations", self.window.camera
                )
                self.food_available = False
                self.food += 1
            else:
                self.dialogue_box = DialogueBox(
                    "food_stand", "no_rations", self.window.camera
                )

    def dude_interaction(self) -> None:
        if self.player.in_shelter:
            num = random.random()
            if num > 0.5:
                self.dialogue_box = DialogueBox(
                    "dude",
                    "shelter1",
                    self.window.camera,
                )
            else:
                self.dialogue_box = DialogueBox(
                    "dude",
                    "shelter2",
                    self.window.camera,
                )
        elif not self.sister.alive:
            self.dialogue_box = DialogueBox("dude", "sister_dead", self.window.camera)
        elif self.air_raid:
            self.dialogue_box = DialogueBox("dude", "air_raid", self.window.camera)
        elif self.doing_delivery and self.delivery_phase == 5:
            self.dialogue_box = DialogueBox(
                "dude",
                "delivery",
                self.window.camera,
            )
            self.doing_delivery = False
            self.medicine -= 1
        else:
            num = random.random()
            if num > 0.66:
                self.dialogue_box = DialogueBox(
                    "dude",
                    "dialogue1",
                    self.window.camera,
                )
            elif num > 0.33:
                self.dialogue_box = DialogueBox(
                    "dude",
                    "dialogue2",
                    self.window.camera,
                )
            else:
                self.dialogue_box = DialogueBox(
                    "dude",
                    "dialogue3",
                    self.window.camera,
                )

    def food_rationer_interaction(self) -> None:
        if self.player.in_shelter:
            num = random.random()
            if num > 0.66:
                self.dialogue_box = DialogueBox(
                    "food_rationer",
                    "shelter1",
                    self.window.camera,
                )
            elif num > 0.33:
                self.dialogue_box = DialogueBox(
                    "food_rationer",
                    "shelter2",
                    self.window.camera,
                )
            else:
                self.dialogue_box = DialogueBox(
                    "food_rationer",
                    "shelter3",
                    self.window.camera,
                )

    def sister_interaction(self) -> None:
        if self.sister.alive:
            if self.air_raid:
                self.player.carrying_sister = True
                self.player.texture = self.player.carry_idle
            elif self.medicine > 0 and not self.doing_delivery:
                self.dialogue_box = DialogueBox(
                    "sister",
                    "medicine",
                    self.window.camera,
                )
                self.medicine -= 1
                self.sister.health += 10
            elif self.food > 0:
                self.dialogue_box = DialogueBox("sister", "food", self.window.camera)
                self.food -= 1
                self.sister.health += 5
            else:
                num = random.random()
                if num > 0.83:
                    self.dialogue_box = DialogueBox(
                        "sister", "dialogue1", self.window.camera
                    )
                elif num > 0.66:
                    self.dialogue_box = DialogueBox(
                        "sister", "dialogue2", self.window.camera
                    )
                elif num > 0.49:
                    self.dialogue_box = DialogueBox(
                        "sister", "dialogue3", self.window.camera
                    )
                elif num > 0.32:
                    self.dialogue_box = DialogueBox(
                        "sister", "dialogue4", self.window.camera
                    )
                elif num > 0.15:
                    self.dialogue_box = DialogueBox(
                        "sister", "dialogue5", self.window.camera
                    )
                else:
                    self.dialogue_box = DialogueBox(
                        "sister", "dialogue6", self.window.camera
                    )
        else:
            num = random.random()
            if num > 0.5:
                self.dialogue_box = DialogueBox("sister", "dead1", self.window.camera)
            else:
                self.dialogue_box = DialogueBox("sister", "dead2", self.window.camera)

    def young_boy_interaction(self) -> None:
        if self.player.in_shelter:
            num = random.random()
            if num > 0.5:
                self.dialogue_box = DialogueBox(
                    "young_boy",
                    "shelter1",
                    self.window.camera,
                )
            else:
                self.dialogue_box = DialogueBox(
                    "young_boy",
                    "shelter2",
                    self.window.camera,
                )
        elif not self.sister.alive:
            self.dialogue_box = DialogueBox(
                "young_boy", "sister_dead", self.window.camera
            )
        elif self.air_raid:
            self.dialogue_box = DialogueBox("young_boy", "air_raid", self.window.camera)
        elif self.doing_delivery and self.delivery_phase == 4:
            self.dialogue_box = DialogueBox(
                "young_boy",
                "delivery",
                self.window.camera,
            )
            self.doing_delivery = False
            self.medicine -= 1
        else:
            num = random.random()
            if num > 0.66:
                self.dialogue_box = DialogueBox(
                    "young_boy",
                    "dialogue1",
                    self.window.camera,
                )
            elif num > 0.33:
                self.dialogue_box = DialogueBox(
                    "young_boy",
                    "dialogue2",
                    self.window.camera,
                )
            else:
                self.dialogue_box = DialogueBox(
                    "young_boy",
                    "dialogue3",
                    self.window.camera,
                )

    def doctor_interaction(self) -> None:
        if self.player.in_shelter:
            num = random.random()
            if num > 0.5:
                self.dialogue_box = DialogueBox(
                    "doctor",
                    "shelter1",
                    self.window.camera,
                )
            else:
                self.dialogue_box = DialogueBox(
                    "doctor",
                    "shelter2",
                    self.window.camera,
                )
        elif not self.sister.alive:
            self.dialogue_box = DialogueBox("doctor", "sister_dead", self.window.camera)
        elif self.air_raid:
            self.dialogue_box = DialogueBox("doctor", "air_raid", self.window.camera)
        elif self.doing_delivery:
            num = random.random()
            if num > 0.5:
                self.dialogue_box = DialogueBox(
                    "doctor",
                    "delivering1",
                    self.window.camera,
                )
            else:
                self.dialogue_box = DialogueBox(
                    "doctor",
                    "delivering2",
                    self.window.camera,
                )
        else:
            if self.delivery_phase == 0:
                self.dialogue_box = DialogueBox(
                    "doctor",
                    "phase0",
                    self.window.camera,
                )
                self.delivery_phase += 1
            elif self.delivery_phase == 1:
                self.dialogue_box = DialogueBox(
                    "doctor",
                    "phase1",
                    self.window.camera,
                )
                self.delivery_phase += 1
                self.doing_delivery = True
                self.medicine += 1
            elif self.delivery_phase == 2:
                self.dialogue_box = DialogueBox(
                    "doctor",
                    "phase2",
                    self.window.camera,
                )
                self.delivery_phase += 1
                self.doing_delivery = True
                self.medicine += 1
            elif self.delivery_phase == 3:
                self.dialogue_box = DialogueBox(
                    "doctor",
                    "phase3",
                    self.window.camera,
                )
                self.delivery_phase += 1
                self.doing_delivery = True
                self.medicine += 1
            elif self.delivery_phase == 4:
                self.dialogue_box = DialogueBox(
                    "doctor",
                    "phase4",
                    self.window.camera,
                )
                self.delivery_phase += 1
                self.doing_delivery = True
                self.medicine += 1
            elif self.delivery_phase == 5:
                self.dialogue_box = DialogueBox(
                    "doctor",
                    "phase5",
                    self.window.camera,
                )
                self.delivery_phase += 1
                self.doing_delivery = True
                self.medicine += 1
            elif self.delivery_phase == 6:
                self.dialogue_box = DialogueBox(
                    "doctor",
                    "phase6",
                    self.window.camera,
                )
                self.delivery_phase += 1
                self.medicine += 1
            elif self.delivery_phase == 7:
                num = random.random()
                if num > 0.5:
                    self.dialogue_box = DialogueBox(
                        "doctor",
                        "delivered1",
                        self.window.camera,
                    )
                else:
                    self.dialogue_box = DialogueBox(
                        "doctor",
                        "delivered2",
                        self.window.camera,
                    )

    def elderly_lady_interaction(self) -> None:
        if self.player.in_shelter:
            num = random.random()
            if num > 0.5:
                self.dialogue_box = DialogueBox(
                    "elderly_lady",
                    "shelter1",
                    self.window.camera,
                )
            else:
                self.dialogue_box = DialogueBox(
                    "elderly_lady",
                    "shelter2",
                    self.window.camera,
                )
        elif not self.sister.alive:
            self.dialogue_box = DialogueBox(
                "elderly_lady", "sister_dead", self.window.camera
            )
        elif self.air_raid:
            self.dialogue_box = DialogueBox(
                "elderly_lady", "air_raid", self.window.camera
            )
        elif self.doing_delivery and self.delivery_phase == 2:
            self.dialogue_box = DialogueBox(
                "elderly_lady",
                "delivery1",
                self.window.camera,
            )
            self.doing_delivery = False
            self.medicine -= 1
        elif self.doing_delivery and self.delivery_phase == 6:
            self.dialogue_box = DialogueBox(
                "elderly_lady",
                "delivery2",
                self.window.camera,
            )
            self.doing_delivery = False
            self.medicine -= 1
        else:
            num = random.random()
            if num > 0.66:
                self.dialogue_box = DialogueBox(
                    "elderly_lady",
                    "dialogue1",
                    self.window.camera,
                )
            elif num > 0.33:
                self.dialogue_box = DialogueBox(
                    "elderly_lady",
                    "dialogue2",
                    self.window.camera,
                )
            else:
                self.dialogue_box = DialogueBox(
                    "elderly_lady",
                    "dialogue3",
                    self.window.camera,
                )

    def shelter_interaction(self) -> None:
        if self.player.carrying_sister or not self.sister.alive:
            self.enter_shelter()
        else:
            self.dialogue_box = DialogueBox(
                "air_raid",
                "cannot_enter_shelter",
                self.window.camera,
            )

    def on_key_release(self, key, modifiers) -> None:
        if self.scene_state == "GAMEPLAY":
            self.player.on_key_release(key)
