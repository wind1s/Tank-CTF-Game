import ai
import gameobjects as obj
import images as img
import pygame as pyg
import utility
import pymunk as pym


def create_grass_background(current_map, screen):
    background = pyg.Surface(screen.get_size())
    #   Copy the grass tile all over the level area
    for x in range(0, current_map.width):
        for y in range(0,  current_map.height):
            # The call to the function "blit" will copy the image
            # contained in "images.grass" into the "background"
            # image at the coordinates given as the second argument
            background.blit(
                img.grass_img, (x*img.TILE_SIZE, y*img.TILE_SIZE))

    return background


def create_boxes(current_map, space):
    boxes = []

    for x in range(0, current_map.width):
        for y in range(0,  current_map.height):
            # Get the type of boxes
            box_type = current_map.boxAt(x, y)
            # If the box type is not 0 (aka grass tile), create a box
            if(box_type != 0):
                # Create a "Box" using the box_type, aswell as the x,y coordinates,
                # and the pymunk space
                box = utility.get_box_with_type(x, y, box_type, space)
                boxes.append(box)

    return boxes


def create_tanks(current_map, space):
    tanks = []
    # Loop over the starting poistion
    for i in range(0, len(current_map.start_positions)):
        # Get the starting position of the tank "i"
        pos = current_map.start_positions[i]
        # Create the tank, images.tanks contains the image representing the tank
        tank = obj.Tank(pos[0], pos[1], pos[2], img.tank_images[i], space)
        # Add the tank to the list of tanks
        tanks.append(tank)

    return tanks


def create_bases(current_map):
    bases = []
    # Loop over the starting poistion
    for i in range(0, len(current_map.start_positions)):
        # Get the starting position of the tank "i"
        pos = current_map.start_positions[i]
        # Create the tank, images.tanks contains the image representing the tank
        base = obj.Base(pos[0], pos[1], img.base_images[i])
        # Add the tank to the list of tanks
        bases.append(base)

    return bases


def create_flag(current_map):
    return obj.Flag(
        current_map.flag_position[0],
        current_map.flag_position[1])


def create_map_bounds(current_map, body):
    bounds = [pym.Segment(
        body, (0, 0),
        (0, current_map.height),
        0.0),
        pym.Segment(
        body, (0, current_map.height),
        (current_map.width, current_map.height),
        0.0),
        pym.Segment(
        body, (current_map.width, current_map.height),
        (current_map.width, 0),
        0.0),
        pym.Segment(
        body, (current_map.width, 0),
        (0, 0),
        0.0)]

    for line in bounds:
        line.elasticity = 0.0
        line.friction = 0.0

    return bounds


def create_ai(tanks, game_objects, space, current_map):
    ai_list = []
    for tank in tanks:
        ai_list.append(ai.Ai(tank, game_objects, tanks, space, current_map))

    return ai_list
