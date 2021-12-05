#!/usr/bin/env python3
"""
"""
import maps
import pygame as pyg
from sounds import CTFSounds
from images import CTFImages
from ctfgame import CTFGame
from sys import argv
from config import SINGLEPLAYER_MODE
from cmdparser import parse_cmd_args


# Init the display
pyg.init()
pyg.display.set_mode()

# Init the game sounds and images.
CTFImages()
CTFSounds()
CTFSounds.background.play()

arguments = parse_cmd_args()

game_map = maps.map0
game = CTFGame(arguments.game_mode, game_map)
game.run_loop()
