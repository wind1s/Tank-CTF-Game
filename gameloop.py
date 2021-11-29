import pygame as pyg
from ctfgame import *
import sounds
import sys
import keyevent


def game_loop(mode):
    # Main Loop
    # Control
    # whether the game run

    running = True
    skip_update = 0

    player1_tank = tanks[0]
    player2_tank = None

    if mode == "--multiplayer":
        ai_objects.remove(ai_objects[-1])
        player2_tank = tanks[-1]

    key_down_event_args = {
        pyg.K_UP: [player1_tank],
        pyg.K_DOWN: [player1_tank],
        pyg.K_LEFT: [player1_tank],
        pyg.K_RIGHT: [player1_tank],
        pyg.K_SPACE: [player1_tank, space, game_objects],
        pyg.K_w: [player2_tank],
        pyg.K_s: [player2_tank],
        pyg.K_a: [player2_tank],
        pyg.K_d: [player2_tank],
        pyg.K_x: [player2_tank, space, game_objects]
    }

    key_up_event_args = {
        pyg.K_UP: [player1_tank],
        pyg.K_DOWN: [player1_tank],
        pyg.K_LEFT: [player1_tank],
        pyg.K_RIGHT: [player1_tank],
        pyg.K_w: [player2_tank],
        pyg.K_s: [player2_tank],
        pyg.K_a: [player2_tank],
        pyg.K_d: [player2_tank]
    }

    while running:
        # Handle the events
        for event in pyg.event.get():
            # Check if we receive a QUIT event (for instance, if the user press the
            # close button of the wiendow) or if the user press the escape key.

            if event.type == pyg.QUIT or (
                    event.type == pyg.KEYDOWN and event.key == pyg.K_ESCAPE):
                running = False

            elif event.type == pyg.KEYDOWN:
                keyevent.key_down_event(event.key, key_down_event_args)

            elif event.type == pyg.KEYUP:
                keyevent.key_up_event(event.key, key_up_event_args)

        # Decide what the ai should do.
        for ai_obj in ai_objects:
            ai_obj.decide()

        # Update physics
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

        # Check collisions and update the objects position
        space.step(1 / FRAMERATE)

        # Update object that depends on an other object position (for instance a flag)
        for obj in game_objects:
            obj.post_update(clock)

        for i, tank in enumerate(tanks):
            tank.try_grab_flag(flag)
            if tank.has_won():
                sounds.victory.play()
                print(f"Tank {i} has won!")
                running = False

            tank.post_update(clock)

        # Update Display

        # Display the background on the screen
        screen.blit(background, (0, 0))

        # Update the display of the game objects on the screen
        for obj in game_objects:
            obj.update_screen(screen)

        for tank in tanks:
            tank.update_screen(screen)

        # Redisplay the entire screen (see double buffer technique)
        pyg.display.flip()

        # Control the game framerate
        clock.tick(FRAMERATE)
