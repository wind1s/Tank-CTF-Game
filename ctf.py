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

pyg.mixer.pre_init(44100, -16, 1, 512)
pyg.mixer.init()

# Init the display
pyg.init()
pyg.display.set_mode()

# Load map and get the number of players.
game_map = CTFMap.load_map(arguments.map)

# Init the game sounds and images.
CTFImages(game_map.n_players)
CTFSounds()
CTFSounds.music.set_volume(0.6)
CTFSounds.music.play(-1)

# Init game and run game loop.
game = CTFGame(arguments.game_mode, game_map, {})
game.run_loop()
