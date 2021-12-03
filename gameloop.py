from ctfgame import *
import pygame as pyg
import sounds


def game_loop(mode):
    # Main Loop
    # Control
    # whether the game run

    running = True
    skip_update = 0

    player1_tank = None
    player2_tank = None

    if mode == "--singleplayer":
        player1_tank = tanks[0]

    elif mode == "--multiplayer":
        ai_objects.remove(ai_objects[-1])
        player2_tank = tanks[-1]

    # Init event handler and keyboard bindings.
    keyaction = KeyAction(
        mode, (player1_tank, player2_tank),
        game_objects, space)
    event_handler = EventHandler(mode, keyaction)

    while running:
        event_handler.handle_events(pyg.event)

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
