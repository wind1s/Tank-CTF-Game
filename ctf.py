#!/usr/bin/env python3
"""
"""
import pygame as pyg
from maps import CTFMap
from sounds import CTFSounds
from images import CTFImages
from ctfgame import CTFGame
from cmdparser import parse_game_cmd_args
from config import TERMINAL_DISPLAY_TITLE

print(TERMINAL_DISPLAY_TITLE)
arguments = parse_game_cmd_args()

# Init the display
pyg.init()
pyg.display.set_mode()

# Init the game sounds and images.
CTFImages()
CTFSounds()
CTFSounds.background.play()

game = CTFGame(arguments.game_mode, CTFMap.load_map(arguments.map))
game.run_loop()
