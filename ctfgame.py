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
space = collision.add_collision_handlers(current_map, space)
screen = pyg.display.set_mode(current_map.rect().size)
background = cobj.create_grass_background(current_map, screen)

boxes = cobj.create_boxes(current_map, space)
tanks = cobj.create_tanks(current_map, space)
flag = cobj.create_flag(current_map)
bases = cobj.create_bases(current_map)

game_objects = [*boxes, *bases, flag]

ai_objects = cobj.create_ai(tanks[1:], game_objects, space, current_map)


"""
from createobjects import (
    create_ai, create_bases, create_boxes, create_flag, create_tanks,
    create_grass_background)
from collision import add_collision_handlers
from pymunk import Space
from pygame import (display, time, init)

class CTFGame:
    def __init__(self, game_map, framerate):
        # Initialise the display
        init()
        display.set_mode()

        self.framerate = framerate
        self.current_map = game_map
        # Initialise the clock
        self.clock = time.Clock()

        # Initialise the physics engine
        self.space = Space()
        self.space.gravity = (0.0,  0.0)
        self.space.damping = 0.1  # Adds friction to the ground for all objects

        self.space = add_collision_handlers(
            self.current_map, self.space)
        self.screen = display.set_mode(self.current_map.rect().size)
        self.background = create_grass_background(
            self.current_map, self.screen)

        self.boxes = create_boxes(self.current_map, self.space)
        self.tanks = create_tanks(self.current_map, self.space)
        self.flag = create_flag(self.current_map)
        self.bases = create_bases(self.current_map)

        self.game_objects = [*self.boxes, *self.bases, self.flag]

        self.ai_objects = create_ai(
            self.tanks[1:],
            self.game_objects, self.space, self.current_map)

    def run(self):
        pass
"""
