from keyaction import KeyAction
import ctfgame
import pygame as pyg
import keyaction


class EventHandler(ctfgame.CTFGame):
    def __init__(self, game_mode):

        self.game_mode = game_mode

        self.event_mapping = {
            pyg.QUIT: self.event_quit,
            pyg.KEYDOWN: self.event_keydown,
            pyg.KEYUP: self.event_keyup
        }

        self.keyaction = keyaction.KeyAction(game_mode)

    def handle_events(self, pygame_event):
        """ Handles all game events. """
        for event in pygame_event.get():

            # Check if key has defined functionality.
            if event in self.event_mapping:
                # Callback has supplied arguments.
                event_callback = self.event_mapping[event]

                event_callback(event)

    def event_quit(self, _):
        """ Quits the game. """
        self.running = False

    def event_keydown(self, event):
        """ Hanldes key down events. """
        self.keyaction.keydown_action(event)

    def event_keyup(self, event):
        """ Handles key up events. """
        self.keyaction.keyup_action(event)
