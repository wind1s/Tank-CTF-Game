import argparse
import os
from config import (SINGLEPLAYER_MODE, HOT_MULTIPLAYER_MODE,
                    CO_OP_MODE, MAP_PATH)


def parse_editor_cmd_args():
    parser = argparse.ArgumentParser(
        description='Map editor for CTF game.')
    parser.add_argument(
        "size",
        type=str,
        help="Choose the size of the map."
    )
    """
    parser.add_argument(
        "--map",
        type=str,
        default=os.path.join(MAP_PATH, "map0.txt"),
        choices=(),
        help="set the map to play."
    )
    """

    return parser.parse_args()


def parse_game_cmd_args():
    parser = argparse.ArgumentParser(
        description='Capture the Flag game with Tanks!')
    parser.add_argument(
        "--game-mode",
        type=str,
        default=SINGLEPLAYER_MODE,
        choices=(SINGLEPLAYER_MODE, HOT_MULTIPLAYER_MODE, CO_OP_MODE),
        help="set the game mode"
    )
    parser.add_argument(
        "--map",
        type=str,
        default="map0.json",
        help="set the map to play."
    )

    return parser.parse_args()
