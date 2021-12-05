import argparse
import os
from config import (SINGLEPLAYER_MODE, HOT_MULTIPLAYER_MODE,
                    CO_OP_MODE, MAP_PATH)


def parse_cmd_args():
    parser = argparse.ArgumentParser(
        description='Capture the Flag game with Tanks!')
    parser.add_argument(
        "--game-mode",
        type=str,
        default=SINGLEPLAYER_MODE,
        choices=(SINGLEPLAYER_MODE, HOT_MULTIPLAYER_MODE, CO_OP_MODE),
        help="set the game mode"
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


args = parse_cmd_args()
print(args)
