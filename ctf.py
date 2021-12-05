#!/usr/bin/env python3
"""
"""
import maps
from ctfgame import CTFGame
from sys import argv
from config import SINGLEPLAYER_MODE


game_mode = None

if len(argv) > 1:
    game_mode = argv[1]
else:
    game_mode = SINGLEPLAYER_MODE

game_map = maps.map0
game = CTFGame(game_mode, game_map)
game.run_loop()
