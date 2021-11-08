import gameobjects as gameobj
import images as img
import pygame as pyg
import pymunk as pym
import initgame as game


def create_grass_background(current_map, screen):
    background = pyg.Surface(screen.get_size())
    #   Copy the grass tile all over the level area
    for x in range(0, current_map.width):
        for y in range(0,  current_map.height):
            # The call to the function "blit" will copy the image
            # contained in "images.grass" into the "background"
            # image at the coordinates given as the second argument
            background.blit(
                img.grass, (x*img.TILE_SIZE, y*img.TILE_SIZE))

    return background


def create_boxes(curr_map, space):
    boxes = []
    # -- Create the boxes
    for x in range(0, curr_map.width):
        for y in range(0,  curr_map.height):
            # Get the type of boxes
            box_type = curr_map.boxAt(x, y)
            # If the box type is not 0 (aka grass tile), create a box
            if(box_type != 0):
                # Create a "Box" using the box_type, aswell as the x,y coordinates,
                # and the pymunk space
                box = gameobj.get_box_with_type(x, y, box_type, space)
                boxes.append(box)

    return boxes


def create_tanks(curr_map, space):
    # -- Create the tanks
    tanks = []
    # Loop over the starting poistion
    for i in range(0, len(curr_map.start_positions)):
        # Get the starting position of the tank "i"
        pos = curr_map.start_positions[i]
        # Create the tank, images.tanks contains the image representing the tank
        tank = gameobj.Tank(pos[0], pos[1], pos[2], img.tanks[i], space)
        # Add the tank to the list of tanks
        tanks.append(tank)

    return tanks


def create_bases(curr_map):
    # -- Create the tanks
    bases = []
    # Loop over the starting poistion
    for i in range(0, len(curr_map.start_positions)):
        # Get the starting position of the tank "i"
        pos = curr_map.start_positions[i]
        # Create the tank, images.tanks contains the image representing the tank
        base = gameobj.Base(pos[0], pos[1], img.bases[i])
        # Add the tank to the list of tanks
        bases.append(base)

    return bases


def create_flag(curr_map):
    # -- Create the flag
    return gameobj.Flag(
        curr_map.flag_position[0],
        curr_map.flag_position[1])


def create_map_bounds(curr_map, body):
    bounds = [pym.Segment(
        body, (0, 0),
        (0, curr_map.height),
        0.0),
        pym.Segment(
        body, (0, curr_map.height),
        (curr_map.width, curr_map.height),
        0.0),
        pym.Segment(
        body, (curr_map.width, curr_map.height),
        (curr_map.width, 0),
        0.0),
        pym.Segment(
        body, (curr_map.width, 0),
        (0, 0),
        0.0)]

    for line in bounds:
        line.elasticity = 0.0
        line.friction = 0.0

    return bounds


def collision_bullet_tank(arb, space, _):
    game_objects = game.game_objects
    tanks = game.tanks
    curr_map = game.current_map
    bullet_shape = arb.shapes[0]
    tank_shape = arb.shapes[1]

    if bullet_shape.parent in game_objects:
        game_objects.remove(bullet_shape.parent)
    space.remove(bullet_shape, bullet_shape.body)

    for i in range(0, len(curr_map.start_positions)):
        if tank_shape.parent == tanks[i]:
            pos = curr_map.start_positions[i]

            # TODO, make a tank reset method to avoid loading sprite again.
            tanks[i] = gameobj.Tank(pos[0], pos[1], pos[2],
                                    img.tanks[i], space)
        space.remove(tank_shape, tank_shape.body)

    return True


def collision_bullet_box(arb, space, _):
    game_objects = game.game_objects
    bullet_shape = arb.shapes[0]
    box_shape = arb.shapes[1]

    if bullet_shape.parent in game_objects:
        game_objects.remove(bullet_shape.parent)
    space.remove(bullet_shape, bullet_shape.body)

    if box_shape.parent.type == 1:
        game_objects.remove(box_shape.parent)
        space.remove(box_shape, box_shape.body)

    return True


def collision_bullet_wall(arb, space, _):
    game_objects = game.game_objects
    bullet_shape = arb.shapes[0]

    if bullet_shape.parent in game_objects:
        game_objects.remove(bullet_shape.parent)
    space.remove(bullet_shape, bullet_shape.body)

    return True
