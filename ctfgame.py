"""
"""
import pygame as pyg
import pymunk as pym
import createobjects as cobj
import collision
from utility import lookup_call
from keyaction import KeyAction
from eventhandler import EventHandler
from sounds import CTFSounds
from gameobjects import (Tank, Flag)
from config import (SINGLEPLAYER_MODE, HOT_MULTIPLAYER_MODE,
                    CO_OP_MODE, FRAMERATE)


class CTFGame:
    """ Main game class. Handles all major functionality. """

    def __init__(self, game_mode, game_map, score_board, difficulty):
        self.running = True
        self.game_mode = game_mode
        self.current_map = game_map
        self.difficulty = difficulty

        # Initialise the clock
        self.clock = pyg.time.Clock()

        # Init screen and create background.
        self.screen = pyg.display.set_mode(game_map.rect().size)
        self.background = cobj.create_grass_background(
            self.current_map, self.screen)

        # Initialise the physics engine
        self.space = pym.Space()
        self.space.gravity = (0.0,  0.0)
        self.space.damping = 0.05  # Adds friction to the ground for all objects
        self.space.add(
            *cobj.create_map_bounds(game_map, self.space.static_body))
        self.skip_update = 0

        # Create game objects.
        self.boxes = cobj.create_boxes(self.current_map, self.space)
        self.bases = cobj.create_bases(self.current_map)
        self.tanks = cobj.create_tanks(
            self.current_map, self.space, self.clock)
        self.flag = Flag.create_flag(*self.current_map.flag_position)

        self.game_objects = self.bases + self.boxes + self.tanks + [self.flag]

        # Create ai's.
        self.ai_objects = cobj.create_ai(
            self.tanks[1:],
            self.game_objects, self.space, self.current_map, self.clock,
            difficulty)
        # Setup score board.
        self.score_board = score_board

        if not score_board:
            self.score_board = {tank.name: 0 for tank in self.tanks}

        # Set game mode.
        self.player1_tank = None
        self.player2_tank = None

        def set_singleplayer():
            self.player1_tank = self.tanks[0]

        def set_hot_multiplayer():
            self.ai_objects.remove(self.ai_objects[-1])
            self.player1_tank = self.tanks[0]
            self.player2_tank = self.tanks[-1]

        def set_co_op():
            assert False, "co-op not implemented!"

        lookup_call(
            self.game_mode,
            {SINGLEPLAYER_MODE: set_singleplayer,
             HOT_MULTIPLAYER_MODE: set_hot_multiplayer,
             CO_OP_MODE: set_co_op})

        # Init event handler, keyboard bindings and collision handler.
        keyaction = KeyAction(
            game_mode, (self.player1_tank, self.player2_tank),
            self.game_objects, self.space, self.quit)
        self.event_handler = EventHandler(game_mode, keyaction, self.quit)

        collision.CollisionHandler(
            self.space, self.game_objects, self.ai_objects, self.clock)

    def quit(self):
        self.running = False

    def restart(self):
        self.__init__(self.game_mode, self.current_map,
                      self.score_board, self.difficulty)

    def run_loop(self):
        """ Main game loop. """
        while self.running:
            self.event_handler.handle_events(pyg.event)

            # Update the ai to take a new decision.
            self.update_ai_decision()

            # Update physics of objects. Change speed, pos, acceleration etc.
            self.update_objects()

            # Check collisions and update the objects position
            self.space.step(1 / FRAMERATE)

            # Update object that depends on an other object position (for instance a flag)
            self.post_update_objects()

            # Update Display
            # Display the background on the screen
            self.screen.blit(self.background, (0, 0))

            # Update the display of the game objects on the screen
            self.screen_update_objects()

            # Redisplay the entire screen (see double buffer technique)
            pyg.display.flip()

            # Control the game framerate
            self.clock.tick(FRAMERATE)

    def update_objects(self):
        """ Updates the physics of all objects. """
        if self.skip_update == 0:
            for obj in self.game_objects:
                obj.update()

            self.skip_update = 2
        else:
            self.skip_update -= 1

    def post_update_objects(self):
        """ Does post updating of all objects. """

        for obj in self.game_objects:

            if isinstance(obj, Tank):
                obj.try_grab_flag(self.flag)

                if obj.has_won():
                    CTFSounds.score.play()
                    print(f"{obj.name} won this round!")
                    self.score_board[obj.name] += 1

                    self.print_score_board()
                    self.restart()

            obj.post_update()

    def screen_update_objects(self):
        """ Updates the screen with changes to all objects. """
        for obj in self.game_objects:
            obj.update_screen(self.screen)

    def update_ai_decision(self):
        """ Updated the next decision of ai's. """
        for ai_obj in self.ai_objects:
            ai_obj.decide()

    def print_score_board(self):
        print("Score board:")
        for key, val in self.score_board.items():
            print(key, " - ", val, sep="")
