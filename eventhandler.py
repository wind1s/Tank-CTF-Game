import ctfgame
import pygame as pyg
import utility


class EventHandler(ctfgame.CTFGame):
    def __init__(self, game_mode):

        self.game_mode = game_mode

        player_key_args = {
            "up": {
                "player1": {
                    pyg.K_UP: [self.player1_tank],
                    pyg.K_DOWN: [self.player1_tank],
                    pyg.K_LEFT: [self.player1_tank],
                    pyg.K_RIGHT: [self.player1_tank],
                },
                "player2": {
                    pyg.K_w: [self.player2_tank],
                    pyg.K_s: [self.player2_tank],
                    pyg.K_a: [self.player2_tank],
                    pyg.K_d: [self.player2_tank],
                }
            },
            "down": {
                "player1": {
                    pyg.K_UP: [self.player1_tank],
                    pyg.K_DOWN: [self.player1_tank],
                    pyg.K_LEFT: [self.player1_tank],
                    pyg.K_RIGHT: [self.player1_tank],
                    pyg.K_SPACE: [self.player1_tank, self.space, self.game_objects]
                },
                "player2": {
                    pyg.K_w: [self.player2_tank],
                    pyg.K_s: [self.player2_tank],
                    pyg.K_a: [self.player2_tank],
                    pyg.K_d: [self.player2_tank],
                    pyg.K_x: [self.player2_tank, self.space, self.game_objects]
                }
            }
        }

        def set_singleplayer():
            for mode, players in player_key_args.items():
                self.args_key[mode] = {players["player1"]}

        def set_hot_multiplayer():
            self.args_key = player_key_args

        option_actions = {
            "--singleplayer": set_singleplayer,
            "--multiplayer": set_hot_multiplayer}

        utility.lookup_call(game_mode, option_actions)

        self.args_key = {}

        self.mapping_key = {
            "up": {
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
            },
            "down": {
                pyg.K_UP: self.keyup_k_up,
                pyg.K_DOWN: self.keyup_k_down,
                pyg.K_LEFT: self.keyup_k_left,
                pyg.K_w: self.keyup_k_w,
                pyg.K_s: self.keyup_k_s,
                pyg.K_a: self.keyup_k_a,
                pyg.K_d: self.keyup_k_d,
                pyg.K_RIGHT: self.keyup_k_right
            }
        }

        self.event_mapping = {
            pyg.QUIT: self.event_quit,
            pyg.KEYDOWN: self.event_keydown,
            pyg.KEYUP: self.event_keyup
        }

    def handle_events(self, pygame_event):
        """ Handles all game events. """
        for event in pygame_event.get():

            # Check if key has defined functionality.
            if event in self.event_mapping:
                # Callback has supplied arguments.
                event_callback = self.event_mapping[event]

                if hasattr(event, "key"):
                    event_callback(event.key)
                else:
                    event_callback()

    def event_quit(self):
        """ Quits the game. """
        self.running = False

    def event_keydown(self, event_key):
        """ Hanldes key down events. """

        mapping = self.mapping_key["down"]
        args = self.args_key["down"].prepend(event_key)

        utility.lookup_call(event_key, mapping, args)

    def event_keyup(self, event_key):
        """ Handles key up events. """

        mapping = self.mapping_key["up"]
        args = self.args_key["up"].prepend(event_key)

        utility.lookup_call(event_key, mapping, args)

    def keydown_k_x(self, tank, *shoot_args):
        """ Performs key down x keybinding functionality. """
        self.keydown_k_space(tank, *shoot_args)

    def keydown_k_space(self, tank, *shoot_args):
        """ Performs key down space keybinding functionality. """
        tank.shoot(*shoot_args)

    def keydown_k_up(self, tank):
        """ Performs key down up arrow keybinding functionality. """
        tank.accelerate()

    def keydown_k_down(self, tank):
        """ Performs key down down arrow keybinding functionality. """
        tank.decelerate()

    def keydown_k_left(self, tank):
        """ Performs key down left arrow keybinding functionality. """
        tank.turn_left()

    def keydown_k_right(self, tank):
        """ Performs key down right arrow keybinding functionality. """
        tank.turn_right()

    def keyup_k_up(self, tank):
        """ Performs key up up arrow keybinding functionality. """
        tank.stop_moving()

    def keyup_k_down(self, tank):
        """ Performs key up down arrow keybinding functionality. """
        tank.stop_moving()

    def keyup_k_left(self, tank):
        """ Performs key up left arrow keybinding functionality. """
        tank.stop_turning()

    def keyup_k_right(self, tank):
        """ Performs key up right arrow keybinding functionality. """
        tank.stop_turning()

    def keydown_k_w(self, tank):
        """ Performs key down w keybinding functionality. """
        self.keydown_k_up(tank)

    def keydown_k_s(self, tank):
        """ Performs key down s keybinding functionality. """
        self.keydown_k_down(tank)

    def keydown_k_a(self, tank):
        """ Performs key down a keybinding functionality. """
        self.keydown_k_left(tank)

    def keydown_k_d(self, tank):
        """ Performs key down d keybinding functionality. """
        self.keydown_k_right(tank)

    def keyup_k_w(self, tank):
        """ Performs key up w keybinding functionality. """
        self.keyup_k_up(tank)

    def keyup_k_s(self, tank):
        """ Performs key up s keybinding functionality. """
        self.keyup_k_down(tank)

    def keyup_k_a(self, tank):
        """ Performs key up a keybinding functionality. """
        self.keyup_k_left(tank)

    def keyup_k_d(self, tank):
        """ Performs key up d keybinding functionality. """
        self.keyup_k_right(tank)
