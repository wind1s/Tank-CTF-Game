from config import (SINGLEPLAYER_MODE, HOT_MULTIPLAYER_MODE, CO_OP_MODE)
import pygame as pyg
import utility


class KeyAction():
    def __init__(
            self, game_mode, player_tanks, game_objects, space, quit_callback):

        self.player1_tank = player_tanks[0]
        self.player2_tank = player_tanks[1]
        self.game_objects = game_objects
        self.space = space

        # Functions mapped to key presses.
        self.keydown_mapping = {
            pyg.K_ESCAPE: quit_callback,
            pyg.K_UP: self.keydown_k_up,
            pyg.K_DOWN: self.keydown_k_down,
            pyg.K_LEFT: self.keydown_k_left,
            pyg.K_RIGHT: self.keydown_k_right,
            pyg.K_SPACE: self.keydown_k_space,
            pyg.K_w: self.keydown_k_w,
            pyg.K_s: self.keydown_k_s,
            pyg.K_a: self.keydown_k_a,
            pyg.K_d: self.keydown_k_d,
            pyg.K_x: self.keydown_k_x
        }

        self.keyup_mapping = {
            pyg.K_UP: self.keyup_k_up,
            pyg.K_DOWN: self.keyup_k_down,
            pyg.K_RIGHT: self.keyup_k_right,
            pyg.K_LEFT: self.keyup_k_left,
            pyg.K_w: self.keyup_k_w,
            pyg.K_s: self.keyup_k_s,
            pyg.K_a: self.keyup_k_a,
            pyg.K_d: self.keyup_k_d
        }

        player_keys = {
            "player1":
            {pyg.K_UP, pyg.K_DOWN, pyg.K_LEFT, pyg.K_RIGHT, pyg.K_SPACE},
            "player2":
            {pyg.K_w, pyg.K_s, pyg.K_a, pyg.K_d, pyg.K_x}
        }

        self.accepted_keys = set()
        self.accepted_keys.update(self.keyup_mapping.keys())
        self.accepted_keys.update(set(self.keydown_mapping.keys()))

        def set_singleplayer_keybinds():
            self.accepted_keys.difference_update(player_keys["player2"])

        def set_hot_multiplayer_keybinds():
            return

        def set_co_op_keybinds():
            set_hot_multiplayer_keybinds()
            assert False, "co-op not implemented!"

        utility.lookup_call(game_mode, {
            SINGLEPLAYER_MODE: set_singleplayer_keybinds,
            HOT_MULTIPLAYER_MODE: set_hot_multiplayer_keybinds,
            CO_OP_MODE: set_co_op_keybinds
        })

    def keydown_action(self, event):
        """ Calls corresponding function to mapped keydown. """
        event_key = event.key

        if event_key in self.accepted_keys:
            utility.lookup_call(event_key, self.keydown_mapping)

    def keyup_action(self, event):
        """ Calls corresponding function to mapped keyup. """
        event_key = event.key

        if event_key in self.accepted_keys:
            utility.lookup_call(event_key, self.keyup_mapping)

    def keydown_k_space(self):
        """ Performs key down space keybinding functionality. """
        self.player1_tank.shoot(self.space, self.game_objects)

    def keydown_k_x(self):
        """ Performs key down x keybinding functionality. """
        self.player2_tank.shoot(self.space, self.game_objects)

    def keydown_k_up(self):
        """ Performs key down up arrow keybinding functionality. """
        self.player1_tank.accelerate()

    def keydown_k_down(self):
        """ Performs key down down arrow keybinding functionality. """
        self.player1_tank.decelerate()

    def keydown_k_left(self):
        """ Performs key down left arrow keybinding functionality. """
        self.player1_tank.turn_left()

    def keydown_k_right(self):
        """ Performs key down right arrow keybinding functionality. """
        self.player1_tank.turn_right()

    def keyup_k_up(self):
        """ Performs key up up arrow keybinding functionality. """
        self.player1_tank.stop_moving()

    def keyup_k_down(self):
        """ Performs key up down arrow keybinding functionality. """
        self.player1_tank.stop_moving()

    def keyup_k_left(self):
        """ Performs key up left arrow keybinding functionality. """
        self.player1_tank.stop_turning()

    def keyup_k_right(self):
        """ Performs key up right arrow keybinding functionality. """
        self.player1_tank.stop_turning()

    def keydown_k_w(self):
        """ Performs key down w keybinding functionality. """
        self.player2_tank.accelerate()

    def keydown_k_s(self):
        """ Performs key down s keybinding functionality. """
        self.player2_tank.decelerate()

    def keydown_k_a(self):
        """ Performs key down a keybinding functionality. """
        self.player2_tank.turn_left()

    def keydown_k_d(self):
        """ Performs key down d keybinding functionality. """
        self.player2_tank.turn_right()

    def keyup_k_w(self):
        """ Performs key up w keybinding functionality. """
        self.player2_tank.stop_moving()

    def keyup_k_s(self):
        """ Performs key up s keybinding functionality. """
        self.player2_tank.stop_moving()

    def keyup_k_a(self):
        """ Performs key up a keybinding functionality. """
        self.player2_tank.stop_turning()

    def keyup_k_d(self):
        """ Performs key up d keybinding functionality. """
        self.player2_tank.stop_turning()
