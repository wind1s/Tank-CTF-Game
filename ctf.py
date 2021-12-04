#!/usr/bin/env python3
"""
"""
from ctfgame import *
from gameloop import game_loop
from sys import argv


game_mode = None

if len(argv) > 1:
    game_mode = argv[1]


"""

game_map = maps.map0

game = CTFGame(game_mode, game_map)
game.run_loop()

"""

game_loop(game_mode)
