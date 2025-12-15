import arcade
import os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

arcade.load_font(os.path.join(BASE_PATH, "assets", "fonts", "pixel.ttf"))

# Window
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
SCREEN_TITLE = "Taeru"

# Font sizes (Some are stored directly in the files they are used)
ITEMS_FONT_SIZE = 18
DIALOGUE_FONT_SIZE = 16
PRESS_FONT_SIZE = 14

# Scales
CHARACTER_SCALE = 6
BACKGROUND_SCALE = 8
BUILDING_SCALE = 16

# Other
CAMERA_PAN_SPEED = 0.3
FADE_RATE = 2
VOLUME = 0.3

# Sounds
TITLE_MUSIC = arcade.load_sound(
    os.path.join(BASE_PATH, "assets", "sounds", "title_music.wav")
)
GAME_MUSIC = arcade.load_sound(
    os.path.join(BASE_PATH, "assets", "sounds", "game_music.ogg")
)
AFTER_DEATH_MUSIC = arcade.load_sound(
    os.path.join(BASE_PATH, "assets", "sounds", "after_death2_clipped.wav")
)
SIREN_ONLY = arcade.load_sound(
    os.path.join(BASE_PATH, "assets", "sounds", "siren_only.mp3")
)
SIREN_WITH_PLANES = arcade.load_sound(
    os.path.join(BASE_PATH, "assets", "sounds", "siren_with_planes.wav")
)
SHELTER_SHORT = arcade.load_sound(
    os.path.join(BASE_PATH, "assets", "sounds", "shelter_short.wav")
)
SHELTER_LONG = arcade.load_sound(
    os.path.join(BASE_PATH, "assets", "sounds", "shelter_long.wav")
)
ENDING_BOMBS = arcade.load_sound(
    os.path.join(BASE_PATH, "assets", "sounds", "ending_bombs_clipped.wav")
)
END_DRONE = arcade.load_sound(
    os.path.join(BASE_PATH, "assets", "sounds", "end_drone.mp3")
)

# Background textures
GROUND_TEXTURE = arcade.load_texture(
    os.path.join(BASE_PATH, "assets", "tiles", "ground.png")
)
FAR_BACKGROUND_TEXTURE = arcade.load_texture(
    os.path.join(BASE_PATH, "assets", "tiles", "far_background.png")
)
NEAR_BACKGROUND_TEXTURE = arcade.load_texture(
    os.path.join(BASE_PATH, "assets", "tiles", "near_background.png")
)
INNER_SHELTER_TEXTURE = arcade.load_texture(
    os.path.join(BASE_PATH, "assets", "tiles", "inner_shelter.png")
)

# Building textures
SHELTER_TEXTURE = arcade.load_texture(
    os.path.join(BASE_PATH, "assets", "sprites", "shelter.png")
)
HOUSE_TEXTURE = arcade.load_texture(
    os.path.join(BASE_PATH, "assets", "sprites", "house.png")
)
HOSPITAL_OKAY_TEXTURE = arcade.load_texture(
    os.path.join(BASE_PATH, "assets", "sprites", "hospital.png")
)
HOSPITAL_BOMBED_TEXTURE = arcade.load_texture(
    os.path.join(BASE_PATH, "assets", "sprites", "hospital_bombed.png")
)
FOOD_STAND_TEXTURE = arcade.load_texture(
    os.path.join(BASE_PATH, "assets", "sprites", "food_stand.png")
)
ELDERLY_LADY_HOUSE_TEXTURE = arcade.load_texture(
    os.path.join(BASE_PATH, "assets", "sprites", "elderly_lady_house.png")
)

# Player textures
IDLE_TEXTURE = arcade.load_texture(
    os.path.join(BASE_PATH, "assets", "sprites", "player_idle.png")
)
WALK_TEXTURE = arcade.load_texture(
    os.path.join(BASE_PATH, "assets", "sprites", "player_walk.png")
)
CARRY_IDLE_TEXTURE = arcade.load_texture(
    os.path.join(BASE_PATH, "assets", "sprites", "sister_carry_idle.png")
)
CARRY_WALK_TEXTURE = arcade.load_texture(
    os.path.join(BASE_PATH, "assets", "sprites", "sister_carry_walk.png")
)
AFTER_DEATH_IDLE_TEXTURE = arcade.load_texture(
    os.path.join(BASE_PATH, "assets", "sprites", "player_after_death_idle.png")
)
AFTER_DEATH_WALK_TEXTURE = arcade.load_texture(
    os.path.join(BASE_PATH, "assets", "sprites", "player_after_death_walk.png")
)
OVER_SISTER_TEXTURE = arcade.load_texture(
    os.path.join(BASE_PATH, "assets", "sprites", "player_over_sister.png")
)
BACK_TEXTURE = arcade.load_texture(
    os.path.join(BASE_PATH, "assets", "sprites", "player_final_bomb.png")
)

# Sister textures
UP_TEXTURE = arcade.load_texture(
    os.path.join(BASE_PATH, "assets", "sprites", "sister_up.png")
)
TOWARDS_TEXTURE = arcade.load_texture(
    os.path.join(BASE_PATH, "assets", "sprites", "sister_towards.png")
)
AWAY_TEXTURE = arcade.load_texture(
    os.path.join(BASE_PATH, "assets", "sprites", "sister_away.png")
)
DEAD_TEXTURE = arcade.load_texture(
    os.path.join(BASE_PATH, "assets", "sprites", "sister_dead.png")
)
GONE_TEXTURE = arcade.load_texture(
    os.path.join(BASE_PATH, "assets", "sprites", "sister_gone.png")
)

# Character textures
FOOD_RATIONER_TEXTURE = arcade.load_texture(
    os.path.join(BASE_PATH, "assets", "sprites", "food_rationer.png")
)
DOCTOR_TEXTURE = arcade.load_texture(
    os.path.join(BASE_PATH, "assets", "sprites", "doctor.png")
)
ELDERLY_LADY_TEXTURE = arcade.load_texture(
    os.path.join(BASE_PATH, "assets", "sprites", "elderly_lady.png")
)
YOUNG_BOY_TEXTURE = arcade.load_texture(
    os.path.join(BASE_PATH, "assets", "sprites", "young_boy.png")
)
DUDE_TEXTURE = arcade.load_texture(
    os.path.join(BASE_PATH, "assets", "sprites", "dude.png")
)

# Other textures
BOMB_TEXTURE = arcade.load_texture(
    os.path.join(BASE_PATH, "assets", "sprites", "bomb.png")
)
