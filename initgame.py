import pygame as pyg
from initengine import *

import maps
import gameobjects as gameobj
import images
import ai
import initfunctions as init

# -- Variables
#   Define the current level
current_map = maps.map0

# -- Resize the screen to the size of the current level
screen = pyg.display.set_mode(current_map.rect().size)

# -- Generate the background
background = init.create_grass_background(current_map, screen)

collision_object = {}
collision_object["box"] = init.create_boxes(current_map, space)
collision_object["tank"] = init.create_tanks(current_map, space)
collision_object["bullet"] = []

no_collision_object = {}
no_collision_object["flag"] = init.create_flag(current_map)
no_collision_object["base"] = init.create_bases(current_map)

space.add(*init.create_map_bounds(current_map, space.static_body))
space.add_collision_handler(1, 2).pre_solve = init.collision_bullet_tank
space.add_collision_handler(1, 3).pre_solve = init.collision_bullet_box
space.add_collision_handler(1, 0).pre_solve = init.collision_bullet_wall
