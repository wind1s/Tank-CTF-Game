#!/usr/bin/env python3
"""
"""
import pygame
from initgame import *

# -- Import from the ctf framework
import maps
import gameobjects
import images
import ai
import initobjects as iobj


#-- Variables
#   Define the current level
current_map = maps.map0
#   List of all game objects
game_objects = []
tanks = []

# -- Resize the screen to the size of the current level
screen = pygame.display.set_mode(current_map.rect().size)

# -- Generate the background
background = iobj.generate_grass_background(current_map, screen)

game_objects = iobj.create_boxes(current_map, space)
tanks = iobj.create_tanks(current_map, space)
flag = iobj.create_flag(current_map)

#----- Main Loop -----#

# -- Control whether the game run
running = True

skip_update = 0

while running:
    # -- Handle the events
    for event in pygame.event.get():
        # Check if we receive a QUIT event (for instance, if the user press the
        # close button of the wiendow) or if the user press the escape key.
        player_tank = tanks[0]
        if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            player_tank.accelerate()

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            player_tank.decelerate()

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            player_tank.turn_left()

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            player_tank.turn_right()

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

    # -- Update Display

    # Display the background on the screen
    screen.blit(background, (0, 0))

    # <INSERT DISPLAY OBJECTS>
    # Update the display of the game objects on the screen
    for obj in game_objects:
        obj.update_screen(screen)

    # Update the display of the game objects on the screen
    for tank in tanks:
        tank.update_screen(screen)

    flag.update_screen(screen)

    #   Redisplay the entire screen (see double buffer technique)
    pygame.display.flip()

    #   Control the game framerate
    clock.tick(FRAMERATE)
