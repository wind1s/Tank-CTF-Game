#!/usr/bin/env python3
"""
"""
from ctfgame import *
from gameloop import game_loop
from sys import argv
from eventhandler import EventHandler
from keyaction import KeyAction


game_mode = None

if len(argv) > 1:
    game_mode = argv[1]


"""

game_map = maps.map0

game = CTFGame(game_mode, game_map)
game.run_loop(event_handler)

"""

game_loop(game_mode)
