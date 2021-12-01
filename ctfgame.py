"""
"""
from initdisplay import *
from keyaction import KeyAction
from eventhandler import EventHandler
import pygame as pyg
import pymunk as pym
import createobjects as cobj
import collision
import maps
import utility
import sounds
import gameobjects as gobj

FRAMERATE = 45

# Initialise the clock
clock = pyg.time.Clock()

# Initialise the physics engine
space = pym.Space()
space.gravity = (0.0,  0.0)
space.damping = 0.1  # Adds friction to the ground for all objects

current_map = maps.map0
screen = pyg.display.set_mode(current_map.rect().size)
background = cobj.create_grass_background(current_map, screen)

boxes = cobj.create_boxes(current_map, space)
tanks = cobj.create_tanks(current_map, space)
flag = cobj.create_flag(current_map)
bases = cobj.create_bases(current_map)

game_objects = [*boxes, *bases, flag]

space.add(*cobj.create_map_bounds(current_map, space.static_body))
space = collision.add_collision_handlers(game_objects, space)

ai_objects = cobj.create_ai(tanks[1:], game_objects, space, current_map)


class CTFGame:
    FRAMERATE = 45

    def __init__(self, game_mode, game_map):
        # Initialise the display
        pyg.init()
        pyg.display.set_mode()

        self.running = True
        self.game_mode = game_mode
        self.current_map = game_map
        # Initialise the clock
        self.clock = pyg.time.Clock()

        # Init screen and create background.
        self.screen = pyg.display.set_mode(self.current_map.rect().size)
        self.background = cobj.create_grass_background(
            self.current_map, self.screen)

        # Initialise the physics engine
        self.space = pym.Space()
        self.space.gravity = (0.0,  0.0)
        self.space.damping = 0.1  # Adds friction to the ground for all objects

        # Create game objects.
        self.boxes = cobj.create_boxes(self.current_map, self.space)
        self.tanks = cobj.create_tanks(self.current_map, self.space)
        self.flag = cobj.create_flag(self.current_map)
        self.bases = cobj.create_bases(self.current_map)
        self.physics_objects = [*self.boxes, *self.tanks]
        self.visible_objects = [*self.bases, self.flag]

        # Init collison handlers.
        self.space = collision.add_collision_handlers(
            self.physics_objects, self.space)

        # Create ai's.
        self.ai_objects = cobj.create_ai(
            self.tanks[1:],
            self.physics_objects, self.space, self.current_map)

        # Set game mode.
        self.player1_tank = None
        self.player2_tank = None

        def set_singleplayer():
            self.player1_tank = tanks[0]

        def set_hot_multiplayer():
            self.ai_objects.remove(ai_objects[-1])
            self.player2_tank = tanks[-1]

        def set_co_op():
            assert False, "co-op not implemented!"

        utility.lookup_call(
            self.game_mode,
            {"--single_player": set_singleplayer,
             "--multiplayer": set_hot_multiplayer,
             "--co-op:": set_co_op})

        # Init event handler and keyboard bindings.
        keyaction = KeyAction(
            game_mode, (self.player1_tank, self.player2_tank),
            self.physics_objects, self.space)
        self.event_handler = EventHandler(game_mode, keyaction)

    def quit_game(self):
        self.running = False

    def run_loop(self):
        skip_update = 0

        def update_objects(objects):
            # Update physics.
            if skip_update == 0:
                # Loop over all the physics objects and update their speed in function of their
                # acceleration.
                for obj in objects:
                    obj.update()

                skip_update = 2
            else:
                skip_update -= 1

        def post_update_objects(objects):
            for index, obj in enumerate(objects):

                if isinstance(obj, gobj.Tank):
                    obj.try_grab_flag(flag)

                    if obj.has_won():
                        sounds.victory.play()
                        print(f"Tank {index} has won!")
                        self.quit_game()

                obj.post_update(clock)

        def screen_update_objects(objects):
            for obj in objects:
                obj.update_screen(obj)

        while self.running:
            self.event_handler.handle_events(pyg.event)

            # Decide what the ai should do.
            for ai_obj in ai_objects:
                ai_obj.decide()

            update_objects(self.physics_objects + self.visible_objects)

            # Check collisions and update the objects position
            space.step(1 / FRAMERATE)

            # Update object that depends on an other object position (for instance a flag)
            post_update_objects(self.physics_objects + self.visible_objects)

            # Update Display
            # Display the background on the screen
            screen.blit(background, (0, 0))

            # Update the display of the game objects on the screen
            screen_update_objects(self.physics_objects + self.visible_objects)

            # Redisplay the entire screen (see double buffer technique)
            pyg.display.flip()

            # Control the game framerate
            clock.tick(FRAMERATE)
