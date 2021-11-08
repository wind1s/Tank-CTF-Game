import pymunkoptions
import gameobjects
import pygame
import images
import pymunk


def generate_grass_background(current_map, screen):
    # -- Generate the background
    background = pygame.Surface(screen.get_size())
    #   Copy the grass tile all over the level area
    for x in range(0, current_map.width):
        for y in range(0,  current_map.height):
            # The call to the function "blit" will copy the image
            # contained in "images.grass" into the "background"
            # image at the coordinates given as the second argument
            background.blit(
                images.grass, (x*images.TILE_SIZE, y*images.TILE_SIZE))

    return background


def create_boxes(current_map, space):

    boxes = []
    # -- Create the boxes
    for x in range(0, current_map.width):
        for y in range(0,  current_map.height):
            # Get the type of boxes
            box_type = current_map.boxAt(x, y)
            # If the box type is not 0 (aka grass tile), create a box
            if(box_type != 0):
                # Create a "Box" using the box_type, aswell as the x,y coordinates,
                # and the pymunk space
                box = gameobjects.get_box_with_type(x, y, box_type, space)
                boxes.append(box)

    return boxes


def create_tanks(current_map, space):
    # -- Create the tanks
    tanks = []
    # Loop over the starting poistion
    for i in range(0, len(current_map.start_positions)):
        # Get the starting position of the tank "i"
        pos = current_map.start_positions[i]
        # Create the tank, images.tanks contains the image representing the tank
        tank = gameobjects.Tank(pos[0], pos[1], pos[2], images.tanks[i], space)
        # Add the tank to the list of tanks
        tanks.append(tank)

    return tanks


def create_bases(current_map):
    # -- Create the tanks
    bases = []
    # Loop over the starting poistion
    for i in range(0, len(current_map.start_positions)):
        # Get the starting position of the tank "i"
        pos = current_map.start_positions[i]
        # Create the tank, images.tanks contains the image representing the tank
        base = gameobjects.Base(pos[0], pos[1], images.bases[i])
        # Add the tank to the list of tanks
        bases.append(base)

    return bases


def create_flag(current_map):
    # -- Create the flag
    return gameobjects.Flag(
        current_map.flag_position[0],
        current_map.flag_position[1])


def create_map_bounds(curr_map, space):
    bounds = [pymunk.Segment(
        space.static_body, (0, 0),
        (0, curr_map.height),
        0.0),
        pymunk.Segment(
        space.static_body, (0, curr_map.height),
        (curr_map.width, curr_map.height),
        0.0),
        pymunk.Segment(
        space.static_body, (curr_map.width, curr_map.height),
        (curr_map.width, 0),
        0.0),
        pymunk.Segment(
        space.static_body, (curr_map.width, 0),
        (0, 0),
        0.0)]

    for line in bounds:
        line.elasticity = 0.0
        line.friction = 0.0
        line.collision_type = 0
    space.add(*bounds)
