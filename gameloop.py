import pygame as pyg
from initengine import *

# Import from the ctf framework
import maps
import gameobjects as gameobj
import images as img
import ai
import initgame as game


def game_loop():
    # Main Loop
    # Control whether the game run
    game.tanks[2].accelerate()
    running = True
    skip_update = 0

    while running:
        # -- Handle the events
        for event in pyg.event.get():
            # Check if we receive a QUIT event (for instance, if the user press the
            # close button of the wiendow) or if the user press the escape key.
            player_tank = game.tanks[0]
            if event.type == pyg.QUIT or (
                    event.type == pyg.KEYDOWN and event.key == pyg.K_ESCAPE):
                running = False

            elif event.type == pyg.KEYDOWN:
                if event.key == pyg.K_UP:
                    player_tank.accelerate()

                elif event.key == pyg.K_DOWN:
                    player_tank.decelerate()

                elif event.key == pyg.K_LEFT:
                    player_tank.turn_left()

                elif event.key == pyg.K_RIGHT:
                    player_tank.turn_right()

                elif event.key == pyg.K_SPACE:
                    player_tank.shoot(space, game.game_objects)

            elif event.type == pyg.KEYUP:
                if event.key == pyg.K_UP or event.key == pyg.K_DOWN:
                    player_tank.stop_moving()

                elif event.key == pyg.K_LEFT or event.key == pyg.K_RIGHT:
                    player_tank.stop_turning()

        # -- Update physics
        if skip_update == 0:
            # Loop over all the game objects and update their speed in function of their
            # acceleration.
            for obj in game.game_objects:
                obj.update()

            for tank in game.tanks:
                tank.update()

            skip_update = 2
        else:
            skip_update -= 1

        #   Check collisions and update the objects position
        space.step(1 / FRAMERATE)

        #   Update object that depends on an other object position (for instance a flag)
        for obj in game.game_objects:
            obj.post_update()

        for tank in game.tanks:
            tank.try_grab_flag(game.flag)
            if tank.has_won():
                print(f"Tank {tank} has won!")
                running = False

            tank.post_update()

        # -- Update Display

        # Display the background on the screen
        game.screen.blit(game.background, (0, 0))

        # <INSERT DISPLAY OBJECTS>
        # Update the display of the game objects on the screen
        for obj in game.game_objects:
            obj.update_screen(game.screen)

        # Update the display of the bases on the screen
        for base in game.bases:
            base.update_screen(game.screen)

        # Update the display of the tanks on the screen
        for tank in game.tanks:
            tank.update_screen(game.screen)

        game.flag.update_screen(game.screen)

        #   Redisplay the entire screen (see double buffer technique)
        pyg.display.flip()

        #   Control the game framerate
        clock.tick(FRAMERATE)
