"""
"""
from initdisplay import *
import pygame as pyg
import pymunk as pym
import maps
import createobjects as cobj
import collision


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

game_objects = boxes + [flag] + bases

ai_objects = cobj.create_ai(tanks, game_objects, space, current_map)
path = ai_objects[0].find_shortest_path(tanks[0].start_position, pym.Vec2d(4,4))
print(path)

test = ai_objects[1]
print(test.tank.get_pos())
test.turn(pym.Vec2d(4,4))
print(test.tank.get_pos())