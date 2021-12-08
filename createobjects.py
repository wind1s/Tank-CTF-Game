import pygame as pyg
import pymunk as pym
from gameobjects import (Tank, Base, Box)
from images import CTFImages
from ai import Ai
from config import PLAYER_NAMES, TILE_SIZE
from utility import list_comp


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
                (x * TILE_SIZE, y * TILE_SIZE))

    return background


def create_boxes(current_map, space):
    """ Creates boxes at map coord with corresponding box type. """
    width = current_map.width
    height = current_map.height

    def box_func(x, y):
        return Box.create_box(x, y, current_map.box_at(x, y), space)

    def not_grass_tile(x, y):
        return current_map.box_at(x, y) != Box.GRASS_TYPE

    return [box_func(x, y) for y in range(height)
            for x in range(width) if not_grass_tile(x, y)]


def create_tanks(current_map, space, clock):
    """ Creates a tank at the start positions. """
    def tank_func(index, tank_img):
        tank_pos = current_map.start_positions[index]
        return Tank(
            PLAYER_NAMES[index],
            tank_pos[0], tank_pos[1], tank_pos[2],
            tank_img, space, clock, Tank.HIT_POINTS, Tank.NORMAL_MAX_SPEED)

    return list_comp(
        range(current_map.n_players),
        CTFImages.tank_images, func=tank_func)


def create_bases(current_map):
    """ Creates a base at the start positions. """
    def base_func(index, base_img):
        base_pos = current_map.start_positions[index]
        return Base.create_base(base_pos[0], base_pos[1], base_img)

    return list_comp(
        range(current_map.n_players),
        CTFImages.base_images, func=base_func)


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
    def ai_func(tank):
        return Ai.create_ai(tank, game_objects, space, current_map, clock)

    return list_comp(tanks, func=ai_func)
