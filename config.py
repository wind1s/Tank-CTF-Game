""" Internal configurations for the game. """
from os.path import (abspath, join, split)

DEBUG = False  # Change this to set it in debug mode
FRAMERATE = 60
TILE_SIZE = 70

SINGLEPLAYER_MODE = "singleplayer"
HOT_MULTIPLAYER_MODE = "hot-multiplayer"
CO_OP_MODE = "co-op"

MAP_PATH = join(split(abspath(__file__))[0], "map_files")
SOUNDS_PATH = join(split(abspath(__file__))[0], "sound_files")
IMAGES_PATH = join(split(abspath(__file__))[0], "image_files")

JSON_BOXES_REF = "boxes"
JSON_START_POS_REF = "start_positions"
JSON_FLAG_POS_REF = "flag_position"

EXPLOSION_IMG_FILE = "explosion.png"
BULLET_IMG_FILE = "bullet.png"
FLAG_IMG_FILE = "flag.png"
GRASS_IMG_FILE = "grass.png"
WOOD_IMG_FILE = "woodbox.png"
METAL_IMG_FILE = "metalbox.png"
ROCK_IMG_FILE = "rockbox.png"

TANKS_IMG_FILES = ("tank_orange.png", "tank_blue.png", "tank_white.png",
                   "tank_yellow.png", "tank_red.png", "tank_gray.png")
BASES_IMG_FILES = ("base_orange.png", "base_blue.png", "base_white.png",
                   "base_yellow.png", "base_red.png", "base_gray.png")
PLAYER_NAMES = ("William", "Petter", "Player 3 AI",
                "Player 4 AI", "Player 5 AI", "Player 6 AI")

TERMINAL_DISPLAY_TITLE = """
   _____            _                    _______ _            ______ _
  / ____|          | |                  |__   __| |          |  ____| |
 | |     __ _ _ __ | |_ _   _ _ __ ___     | |  | |__   ___  | |__  | | __ _  __ _
 | |    / _` | '_ \| __| | | | '__/ _ \    | |  | '_ \ / _ \ |  __| | |/ _` |/ _` |
 | |___| (_| | |_) | |_| |_| | | |  __/    | |  | | | |  __/ | |    | | (_| | (_| |
  \_____\__,_| .__/ \__|\__,_|_|  \___|    |_|  |_| |_|\___| |_|    |_|\__,_|\__, |
             | |                                                              __/ |
             |_|                                                             |___/
"""
