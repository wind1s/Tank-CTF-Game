#!/usr/bin/env python3
"""
"""
from gameloop import game_loop
from ctfgame import *
from sys import argv

if len(argv) > 1:
    game_mode = argv[1]

game_loop(game_mode)