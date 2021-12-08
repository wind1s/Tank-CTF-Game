import math
import pymunk as pym
from config import TILE_SIZE


def remove_object(game_objects, obj, shape=None, space=None):
    """ Removes a physics object and it's body. """
    if obj in game_objects:
        game_objects.remove(obj)

    if shape is not None:
        assert space is not None, "If object has a shape then a space object must be provided to remove it from the game!"
        space.remove(shape, shape.body)


def add_object(game_objects, obj):
    """ Adds a object to the game world. """
    game_objects.append(obj)


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
    return x * TILE_SIZE


def get_tile_position(position_vector):
    """ Converts and returns the float position of our tank to an integer position. """
    x, y = position_vector
    return pym.Vec2d(int(x), int(y))


def reduce_until_zero(val, reduction):
    val -= reduction if val >= 0 else 0
    return val


def generator_comp(*iterables, func=lambda x: x, pred=lambda *_: True):
    """ Generator comprehension utility function. """
    return (func(*args) for args in zip(*iterables) if pred)


def list_comp(*iterables, func=lambda x: x, pred=lambda *_: True):
    """ List comprehension utility function. """
    return [func(*args) for args in zip(*iterables) if pred(*args)]
