import pygame as pyg


def key_down_event(event_key, callback_args):
    """ Hanldes key down events. """
    key_events = {pyg.K_UP: key_down_k_up,
                  pyg.K_DOWN: key_down_k_down,
                  pyg.K_LEFT: key_down_k_left,
                  pyg.K_RIGHT: key_down_k_right,
                  pyg.K_SPACE: key_down_k_space,
                  pyg.K_w: key_down_k_w,
                  pyg.K_s: key_down_k_s,
                  pyg.K_a: key_down_k_a,
                  pyg.K_d: key_down_k_d,
                  pyg.K_x: key_down_k_x
                  }

    # Check if key has defined functionality.
    if event_key in key_events:
        # Callback has supplied arguments.
        if event_key in callback_args:
            key_events[event_key](*callback_args[event_key])

        else:  # Callback has no arguments.
            key_events[event_key]()


def key_up_event(event_key, callback_args):
    """ Handles key up events. """
    key_events = {pyg.K_UP: key_up_k_up,
                  pyg.K_DOWN: key_up_k_down,
                  pyg.K_LEFT: key_up_k_left,
                  pyg.K_w: key_up_k_w,
                  pyg.K_s: key_up_k_s,
                  pyg.K_a: key_up_k_a,
                  pyg.K_d: key_up_k_d,
                  pyg.K_RIGHT: key_up_k_right
                  }

    # Check if key has defined functionality.
    if event_key in key_events:
        # Callback has supplied arguments.
        if event_key in callback_args:
            key_events[event_key](*callback_args[event_key])

        else:  # Callback has no arguments.
            key_events[event_key]()


def key_down_k_x(tank, *shoot_args):
    """ Performs key down x keybinding functionality. """
    key_down_k_space(tank, shoot_args)


def key_down_k_space(tank, *shoot_args):
    """ Performs key down space keybinding functionality. """
    tank.shoot(*shoot_args)


def key_down_k_up(tank):
    """ Performs key down up arrow keybinding functionality. """
    tank.accelerate()


def key_down_k_down(tank):
    """ Performs key down down arrow keybinding functionality. """
    tank.decelerate()


def key_down_k_left(tank):
    """ Performs key down left arrow keybinding functionality. """
    tank.turn_left()


def key_down_k_right(tank):
    """ Performs key down right arrow keybinding functionality. """
    tank.turn_right()


def key_up_k_up(tank):
    """ Performs key up up arrow keybinding functionality. """
    tank.stop_moving()


def key_up_k_down(tank):
    """ Performs key up down arrow keybinding functionality. """
    tank.stop_moving()


def key_up_k_left(tank):
    """ Performs key up left arrow keybinding functionality. """
    tank.stop_turning()


def key_up_k_right(tank):
    """ Performs key up right arrow keybinding functionality. """
    tank.stop_turning()


def key_down_k_w(tank):
    """ Performs key down w keybinding functionality. """
    key_down_k_up(tank)


def key_down_k_s(tank):
    """ Performs key down s keybinding functionality. """
    key_down_k_down(tank)


def key_down_k_a(tank):
    """ Performs key down a keybinding functionality. """
    key_down_k_left(tank)


def key_down_k_d(tank):
    """ Performs key down d keybinding functionality. """
    key_down_k_right(tank)


def key_up_k_w(tank):
    """ Performs key up w keybinding functionality. """
    key_up_k_up(tank)


def key_up_k_s(tank):
    """ Performs key up s keybinding functionality. """
    key_up_k_down(tank)


def key_up_k_a(tank):
    """ Performs key up a keybinding functionality. """
    key_up_k_left(tank)


def key_up_k_d(tank):
    """ Performs key up d keybinding functionality. """
    key_up_k_right(tank)
