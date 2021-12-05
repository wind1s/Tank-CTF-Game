import math
import pymunk as pym
from images import CTFImages


def seconds_to_ms(seconds: float):
    """ Convertes seconds to milliseconds. """
    return seconds * 1000.0


def lookup_call(mapped_name, callback_table, args_table={}):
    # Check if key has defined functionality.
    if mapped_name in callback_table:
        # Callback has supplied arguments.
        if mapped_name in args_table:
            callback_table[mapped_name](*args_table[mapped_name])
        else:  # Callback has no arguments.
            callback_table[mapped_name]()


def clamp(min_max, value):
    """ Convenient helper function to bound a value to a specific interval. """
    return min(max(-min_max, value), min_max)


def angle_between_vectors(vec1, vec2):
    """ Since Vec2d operates in a cartesian coordinate space we have to
        convert the resulting vector to get the correct angle for our space.
    """
    vec = vec1 - vec2
    vec = vec.perpendicular()
    return vec.angle


def periodic_difference_of_angles(angle1, angle2):
    return (angle1 % (2*math.pi)) - (angle2 % (2*math.pi))


def physics_to_display(x):
    """ This function is used to convert coordinates in the physic engine into the display coordinates """
    return x * CTFImages.TILE_SIZE


def get_tile_position(position_vector):
    """ Converts and returns the float position of our tank to an integer position. """
    x, y = position_vector
    return pym.Vec2d(int(x), int(y))
