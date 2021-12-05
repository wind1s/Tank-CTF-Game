#!/usr/bin/env python3
"""
"""
import maps
import pygame as pyg
from sounds import CTFSounds
from images import CTFImages
from ctfgame import CTFGame
from cmdparser import parse_game_cmd_args


# Init the display
pyg.init()
pyg.display.set_mode()

# Init the game sounds and images.
CTFImages()
CTFSounds()
CTFSounds.background.play()

arguments = parse_game_cmd_args()

game = CTFGame(arguments.game_mode, maps.CTFMap.load_map(arguments.map))
game.run_loop()
