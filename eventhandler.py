import pygame as pyg
from collections import Hashable


class EventHandler():
    def __init__(self, game_mode, keyaction):

        self.game_mode = game_mode

        self.event_mapping = {
            pyg.QUIT: self.event_quit,
            pyg.KEYDOWN: self.event_keydown,
            pyg.KEYUP: self.event_keyup
        }

        self.keyaction = keyaction

    def handle_events(self, pygame_event):
        """ Handles all game events. """
        for event in pygame_event.get():
            # isinstance(event, Hashable) and
            # Check if key has defined functionality.
            event_type = event.type
            if event_type in self.event_mapping:
                # Callback has supplied arguments.
                event_callback = self.event_mapping[event_type]

                event_callback(event)

    def event_quit(self, event):
        """ Quits the game. """
        return False

    def event_keydown(self, event):
        """ Hanldes key down events. """
        self.keyaction.keydown_action(event)

    def event_keyup(self, event):
        """ Handles key up events. """
        self.keyaction.keyup_action(event)
