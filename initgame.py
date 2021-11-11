"""
"""
from initdisplay import *
import pygame as pyg
import pymunk as pym
import maps
import createobjects as cobj
import collision


def init_collision_objects(game_map, space):
    collison_obj = {}
    collison_obj["box"] = cobj.create_boxes(game_map, space)
    collison_obj["tank"] = cobj.create_tanks(game_map, space)
    collison_obj["bullet"] = []

    return collison_obj


def init_no_collison_objects(game_map):
    collison_obj = {}
    collison_obj["flag"] = cobj.create_flag(game_map)
    collison_obj["base"] = cobj.create_bases(game_map)

    return collison_obj


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

collision_object = init_collision_objects(current_map, space)
no_collision_object = init_no_collison_objects(current_map)
