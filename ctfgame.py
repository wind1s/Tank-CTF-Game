"""
"""
from initdisplay import *
import pygame as pyg
import pymunk as pym
import createobjects as cobj
import collision
import maps

FRAMERATE = 50

# Initialise the clock
clock = pyg.time.Clock()

# Initialise the physics engine
space = pym.Space()
space.gravity = (0.0,  0.0)
space.damping = 0.1  # Adds friction to the ground for all objects

current_map = maps.map0
screen = pyg.display.set_mode(current_map.rect().size)
background = cobj.create_grass_background(current_map, screen)

boxes = cobj.create_boxes(current_map, space)
tanks = cobj.create_tanks(current_map, space)
flag = cobj.create_flag(current_map)
bases = cobj.create_bases(current_map)

game_objects = [*boxes, *bases, flag]

space = collision.add_collision_handlers(current_map, game_objects, space)
ai_objects = cobj.create_ai(tanks[1:], game_objects, space, current_map)


class CTFGame:
    def __init__(self, game_map, framerate):
        # Initialise the display
        pyg.init()
        pyg.display.set_mode()

        self.framerate = framerate
        self.current_map = game_map
        # Initialise the clock
        self.clock = pyg.time.Clock()

        # Initialise the physics engine
        self.space = pym.Space()
        self.space.gravity = (0.0,  0.0)
        self.space.damping = 0.1  # Adds friction to the ground for all objects

        self.screen = pyg.display.set_mode(self.current_map.rect().size)
        self.background = cobj.create_grass_background(
            self.current_map, self.screen)

        # Create game objects.
        self.boxes = cobj.create_boxes(self.current_map, self.space)
        self.tanks = cobj.create_tanks(self.current_map, self.space)
        self.flag = cobj.create_flag(self.current_map)
        self.bases = cobj.create_bases(self.current_map)
        self.physics_objects = [*self.boxes, *self.tanks]
        self.visible_objects = [*self.bases, self.flag]

        self.space = collision.add_collision_handlers(
            self.current_map, self.game_objects, self.space)

        # Create ai's.
        self.ai_objects = cobj.create_ai(
            self.tanks[1:],
            self.game_objects, self.space, self.current_map)

        self.player1_tank = tanks[0]
        self.player2_tank = None

        if mode == "--multiplayer":
            ai_objects.remove(ai_objects[-1])
            player2_tank = tanks[-1]

    def init_game_loop(self):
        pass

    def game_loop(self):
        pass
