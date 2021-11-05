import gameobjects
import pygame
import images


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


# <INSERT CREATE BOXES>
def create_boxes(current_map, space):

    game_objects = []
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
                game_objects.append(box)

    return game_objects


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


# <INSERT CREATE FLAG>

def create_flag(current_map):
    # -- Create the flag
    return gameobjects.Flag(
        current_map.flag_position[0],
        current_map.flag_position[1])
