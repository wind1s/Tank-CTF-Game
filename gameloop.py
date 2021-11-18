import pygame as pyg
from initgame import *

# Import from the ctf framework
import maps
import gameobjects as gameobj
import images as img
import ai


def key_down_event(event_key, player_tank, args_lookup):
    key_events = {pyg.K_UP: player_tank.accelerate,
                  pyg.K_DOWN: player_tank.decelerate,
                  pyg.K_LEFT: player_tank.turn_left,
                  pyg.K_RIGHT: player_tank.turn_right,
                  pyg.K_SPACE: player_tank.shoot}

    if event_key in args_lookup:
        key_events[event_key](*args_lookup[event_key])
    else:
        key_events[event_key]()


def key_up_event(event_key, player_tank, args_lookup):
    key_events = {pyg.K_UP: player_tank.stop_moving,
                  pyg.K_DOWN: player_tank.stop_moving,
                  pyg.K_LEFT: player_tank.stop_turning,
                  pyg.K_RIGHT: player_tank.stop_turning}

    if event_key in args_lookup:
        key_events[event_key](*args_lookup[event_key])
    else:
        key_events[event_key]()


def game_loop():
    # Main Loop
    # Control whether the game run
    running = True
    skip_update = 0

    key_down_event_args = {pyg.K_SPACE: (space, game_objects)}
    key_up_event_args = {}

    while running:
        # -- Handle the events
        for event in pyg.event.get():
            # Check if we receive a QUIT event (for instance, if the user press the
            # close button of the wiendow) or if the user press the escape key.
            player1_tank = tanks[0]
            player2_tank = tanks[1]
            if event.type == pyg.QUIT or (
                    event.type == pyg.KEYDOWN and event.key == pyg.K_ESCAPE):
                running = False

            elif event.type == pyg.KEYDOWN:
                key_down_event(event.key, player1_tank, key_down_event_args)

            elif event.type == pyg.KEYUP:
                key_up_event(event.key, player1_tank, key_up_event_args)

        # Decide what the ai should do.
        for ai_obj in ai_objects:
            ai_obj.decide()

        # -- Update physics
        if skip_update == 0:
            # Loop over all the game objects and update their speed in function of their
            # acceleration.
            for obj in game_objects:
                obj.update()

            for tank in tanks:
                tank.update()

            skip_update = 2
        else:
            skip_update -= 1

        #   Check collisions and update the objects position
        space.step(1 / FRAMERATE)

        #   Update object that depends on an other object position (for instance a flag)
        for obj in game_objects:
            obj.post_update()

        for i, tank in enumerate(tanks):
            tank.try_grab_flag(flag)
            if tank.has_won():
                print(f"Tank {i} has won!")
                running = False

            tank.post_update()

        # -- Update Display

        # Display the background on the screen
        screen.blit(background, (0, 0))

        # <INSERT DISPLAY OBJECTS>
        # Update the display of the game objects on the screen
        for obj in game_objects:
            obj.update_screen(screen)

        for tank in tanks:
            tank.update_screen(screen)

        #   Redisplay the entire screen (see double buffer technique)
        pyg.display.flip()

        #   Control the game framerate
        clock.tick(FRAMERATE)
