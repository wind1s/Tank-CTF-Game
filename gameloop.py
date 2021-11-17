import pygame as pyg
from initgame import *

# Import from the ctf framework
import maps
import gameobjects as gameobj
import images as img
import ai


def key_down_event(event, player_tank):
    key_events = {pyg.K_UP: player_tank.accelerate(),
                  pyg.K_DOWN: player_tank.decelerate(),
                  pyg.K_LEFT: player_tank.turn_left(),
                  pyg.K_RIGHT: player_tank.turn_right(),
                  pyg.K_SPACE: player_tank.shoot(space, game_objects)}

    key_events[event.key]()


def game_loop():
    # Main Loop
    # Control whether the game run
    running = True
    skip_update = 0

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
                if event.key == pyg.K_UP:
                    player1_tank.accelerate()

                elif event.key == pyg.K_DOWN:
                    player1_tank.decelerate()

                elif event.key == pyg.K_LEFT:
                    player1_tank.turn_left()

                elif event.key == pyg.K_RIGHT:
                    player1_tank.turn_right()

                elif event.key == pyg.K_SPACE:
                    player1_tank.shoot(space, game_objects)

            elif event.type == pyg.KEYUP:
                if event.key == pyg.K_UP or event.key == pyg.K_DOWN:
                    player1_tank.stop_moving()

                elif event.key == pyg.K_LEFT or event.key == pyg.K_RIGHT:
                    player1_tank.stop_turning()

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
