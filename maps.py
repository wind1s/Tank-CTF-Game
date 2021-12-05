from config import (MAP_PATH, MAP_START_POS_REF,
                    MAP_BOXES_REF, MAP_FLAG_POS_REF)
import os
import json
import pygame as pyg
from images import CTFImages
from gameobjects import Box


class CTFMap:
    """ An instance of Map is a blueprint for how the game map will look. """

    def __init__(self, width, height, boxes, start_positions, flag_position):
        """
        Takes as argument the size of the map (width, height), an array with the boxes type,
        the start position of tanks (start_positions) and the position of the flag (flag_position).
        """
        self.width = width
        self.height = height
        self.boxes = boxes
        self.start_positions = start_positions
        self.flag_position = flag_position

    def rect(self):
        return pyg.Rect(0, 0, CTFImages.TILE_SIZE*self.width, CTFImages.TILE_SIZE*self.height)

    def box_at(self, x, y):
        """ Return the type of the box at coordinates (x, y). """
        return self.boxes[y][x]

    @staticmethod
    def load_map(map_file_name):
        """ Loads a map file. """

        with open(os.path.join(MAP_PATH, map_file_name), "r") as outfile:
            if map_file_name.endswith(".txt"):
                return CTFMap.load_txt_map(outfile)
            elif map_file_name.endswith(".json"):
                return CTFMap.load_json_map(outfile)
            else:
                assert False, f"Can't read map file type."

    @staticmethod
    def load_txt_map(map_file):
        """ Loads a map from a txt file. """
        assert False, "Reading txt map files is not implemented yet!"
        return

    @staticmethod
    def load_json_map(map_file):
        """ Loads a map from a json file. """
        json_obj = json.load(map_file)
        CTFMap.check_json_file(json_obj)

        boxes = json_obj[MAP_BOXES_REF]
        map_width = len(boxes[0])
        map_height = len(boxes)
        start_positions = json_obj[MAP_START_POS_REF]
        flag_position = json_obj[MAP_FLAG_POS_REF]

        return CTFMap(
            map_width, map_height, boxes, start_positions, flag_position)

    @staticmethod
    def check_json_file(json_obj):
        """ Checks if json map file is correct. """
        for setting in (MAP_BOXES_REF, MAP_START_POS_REF, MAP_FLAG_POS_REF):
            assert setting in json_obj.keys(
            ), f"Setting {setting} is not defined in json map file."

        boxes = json_obj[MAP_BOXES_REF]
        n_rows = len(boxes[0])

        entire_board_defined = all(len(row) == n_rows for row in boxes)
        assert entire_board_defined, "Json file is incorrect, entire board is not defined in boxes positions."

        start_positions = json_obj[MAP_START_POS_REF]
        correct_start_pos_format = all(len(start_pos) == 3
                                       for start_pos in start_positions)
        assert correct_start_pos_format, "The format of start positions is incorrect (x, y, orientation)."

        start_pos_on_grass = all(
            boxes[int(y)][int(x)] == Box.GRASS_TYPE for x, y,
            _ in start_positions)
        assert start_pos_on_grass, "All start positions are not place on a grass tile."

        flag_pos_x, flag_pos_y = json_obj[MAP_FLAG_POS_REF]
        flag_pos_on_grass = boxes[int(flag_pos_y)][int(
            flag_pos_x)] == Box.GRASS_TYPE
        assert flag_pos_on_grass, "Flag position is not on a grass tile."


"""
map0 = CTFMap(
    9, 9,
    [[0, 1, 0, 0, 0, 0, 0, 1, 0],
     [0, 1, 0, 2, 0, 2, 0, 1, 0],
     [0, 2, 0, 1, 0, 1, 0, 2, 0],
     [0, 0, 0, 1, 0, 1, 0, 0, 0],
     [1, 1, 0, 3, 0, 3, 0, 1, 1],
     [0, 0, 0, 1, 0, 1, 0, 0, 0],
     [0, 2, 0, 1, 0, 1, 0, 2, 0],
     [0, 1, 0, 2, 0, 2, 0, 1, 0],
     [0, 1, 0, 0, 0, 0, 0, 1, 0]],
    [[0.5, 0.5, 0],
     [8.5, 0.5, 0],
     [0.5, 8.5, 180],
     [8.5, 8.5, 180]],
    [4.5, 4.5])

map1 = CTFMap(
    15, 11,
    [[0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0],
     [0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0],
     [0, 1, 0, 3, 1, 1, 0, 0, 0, 1, 1, 3, 0, 1, 0],
     [0, 2, 0, 0, 3, 0, 0, 2, 0, 0, 3, 0, 0, 2, 0],
     [2, 1, 0, 1, 1, 0, 1, 3, 1, 0, 1, 1, 0, 1, 2],
     [1, 1, 3, 0, 3, 2, 3, 0, 3, 2, 3, 0, 3, 1, 1],
     [2, 1, 0, 1, 1, 0, 1, 3, 1, 0, 1, 1, 0, 1, 2],
     [0, 2, 0, 0, 3, 0, 0, 2, 0, 0, 3, 0, 0, 2, 0],
     [0, 1, 0, 3, 1, 1, 0, 0, 0, 1, 1, 3, 0, 1, 0],
     [0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0],
     [0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0]],
    [[0.5, 0.5, 0],
     [14.5, 0.5, 0],
     [0.5, 10.5, 180],
     [14.5, 10.5, 180],
     [7.5, 0.5, 0],
     [7.5, 10.5, 180]],
    [7.5, 5.5])

map2 = CTFMap(10, 5,
              [[0, 2, 0, 2, 0, 0, 2, 0, 2, 0],
               [0, 3, 0, 1, 3, 3, 1, 0, 3, 0],
               [0, 1, 0, 1, 0, 0, 1, 0, 1, 0],
               [0, 3, 0, 1, 3, 3, 1, 0, 3, 0],
               [0, 2, 0, 2, 0, 0, 2, 0, 2, 0]],
              [[0.5, 2.5, 270], [9.5, 2.5, 90]], [5, 2.5])
"""
