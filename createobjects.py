import pygame as pyg
import pymunk as pym
from gameobjects import (Tank, Base, Flag, Box)
from images import CTFImages
from ai import Ai
from config import PLAYER_NAMES


def create_grass_background(current_map, screen):
    background = pyg.Surface(screen.get_size())
    #   Copy the grass tile all over the level area
    for x in range(0, current_map.width):
        for y in range(0,  current_map.height):
            # The call to the function "blit" will copy the image
            # contained in "images.grass" into the "background"
            # image at the coordinates given as the second argument
            background.blit(
                CTFImages.grass,
                (x * CTFImages.TILE_SIZE, y * CTFImages.TILE_SIZE))

    return background


def create_boxes(current_map, space):
    """ Creates boxes at map coord with corresponding box type. """
    get_type = current_map.box_at

    width = current_map.width
    height = current_map.height

    return [Box.get_box_with_type(x, y, get_type(x, y), space) for y in range(height)
            for x in range(width) if get_type(x, y) != 0]


def create_tanks(current_map, space, clock):
    """ Creates a tank at the start positions. """
    n_tanks = len(current_map.start_positions)
    pos = current_map.start_positions

    return [Tank(PLAYER_NAMES[i], pos[i][0], pos[i][1], pos[i][2], CTFImages.tank_images[i],
                 space, clock, Tank.HIT_POINTS, Tank.NORMAL_MAX_SPEED) for i in range(n_tanks)]


def create_bases(current_map):
    """ Creates a base at the start positions. """
    n_bases = len(current_map.start_positions)
    pos = current_map.start_positions

    return [Base(pos[i][0], pos[i][1], CTFImages.base_images[i])
            for i in range(n_bases)]


def create_flag(current_map):
    """ Creates the flag at its start position. """
    return Flag(
        current_map.flag_position[0],
        current_map.flag_position[1])


def create_map_bounds(current_map, body):
    """ Creates the map bounds. """
    map_width = current_map.width
    map_height = current_map.height

    return (
        pym.Segment(body, (0, 0), (0, map_height), 0.0),
        pym.Segment(body, (0, map_height), (map_width, map_height), 0.0),
        pym.Segment(body, (map_width, map_height), (map_width, 0), 0.0),
        pym.Segment(body, (map_width, 0), (0, 0), 0.0)
    )


def create_ai(tanks, game_objects, space, current_map, clock):
    """ Creates the ai object to control tanks. """
    return [Ai(tank, game_objects, space, current_map, clock) for tank in tanks]
