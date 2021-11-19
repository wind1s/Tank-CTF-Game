import pygame as pyg


def key_down_event(event_key, callback_args):
    key_events = {pyg.K_UP: key_down_k_up,
                  pyg.K_DOWN: key_down_k_down,
                  pyg.K_LEFT: key_down_k_left,
                  pyg.K_RIGHT: key_down_k_right,
                  pyg.K_w: key_down_k_w,
                  pyg.K_s: key_down_k_s,
                  pyg.K_a: key_down_k_a,
                  pyg.K_d: key_down_k_d,
                  pyg.K_SPACE: key_down_k_space
                  }

    # Check if key has defined functionality.
    if event_key in key_events:
        # Callback has supplied arguments.
        if event_key in callback_args:
            key_events[event_key](*callback_args[event_key])

        else:  # Callback has no arguments.
            key_events[event_key]()


def key_up_event(event_key, callback_args):
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


def key_down_k_space(tank, *shoot_args):
    tank.shoot(*shoot_args)


def key_down_k_up(tank):
    tank.accelerate()


def key_down_k_down(tank):
    tank.decelerate()


def key_down_k_left(tank):
    tank.turn_left()


def key_down_k_right(tank):
    tank.turn_right()


def key_up_k_up(tank):
    tank.stop_moving()


def key_up_k_down(tank):
    tank.stop_moving()


def key_up_k_left(tank):
    tank.stop_turning()


def key_up_k_right(tank):
    tank.stop_turning()


def key_down_k_w(tank):
    key_down_k_up(tank)


def key_down_k_s(tank):
    key_down_k_down(tank)


def key_down_k_a(tank):
    key_down_k_left(tank)


def key_down_k_d(tank):
    key_down_k_right(tank)


def key_up_k_w(tank):
    key_up_k_up(tank)


def key_up_k_s(tank):
    key_up_k_down(tank)


def key_up_k_a(tank):
    key_up_k_left(tank)


def key_up_k_d(tank):
    key_up_k_right(tank)
