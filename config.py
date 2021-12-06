""" Internal configurations for the game. """
from os.path import (abspath, join, split)

DEBUG = False  # Change this to set it in debug mode
FRAMERATE = 60

SINGLEPLAYER_MODE = "singleplayer"
HOT_MULTIPLAYER_MODE = "hot-multiplayer"
CO_OP_MODE = "co-op"

MAP_PATH = join(split(abspath(__file__))[0], "map_files")
SOUNDS_PATH = join(split(abspath(__file__))[0], "sound_files")
IMAGES_PATH = join(split(abspath(__file__))[0], "image_files")

MAP_BOXES_REF = "boxes"
MAP_START_POS_REF = "start_positions"
MAP_FLAG_POS_REF = "flag_position"


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
