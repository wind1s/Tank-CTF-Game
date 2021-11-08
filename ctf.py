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


# -- Variables
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
bases = iobj.create_bases(current_map)
iobj.create_map_bounds(current_map, space)


tanks[2].accelerate()


def collision_bullet_tank(arb, space, data):
    if arb.shapes[0].parent in game_objects:
        game_objects.remove(arb.shapes[0].parent)
    space.remove(arb.shapes[0], arb.shapes[0].body)

    for i in range(0, len(current_map.start_positions)):
        if arb.shapes[1].parent == tanks[i]:
            pos = current_map.start_positions[i]
            tanks[i] = gameobjects.Tank(pos[0], pos[1], pos[2],
                                        images.tanks[i], space)
        space.remove(arb.shapes[1], arb.shapes[1].body)

    return False


def collision_bullet_box(arb, space, data):
    if arb.shapes[0].parent in game_objects:
        game_objects.remove(arb.shapes[0].parent)
    space.remove(arb.shapes[0], arb.shapes[0].body)

    if arb.shapes[1].parent.type == 1:
        game_objects.remove(arb.shapes[1].parent)
        space.remove(arb.shapes[1], arb.shapes[1].body)
    return False


def collision_bullet_wall(arb, space, data):
    if arb.shapes[0].parent in game_objects:
        game_objects.remove(arb.shapes[0].parent)
    space.remove(arb.shapes[0], arb.shapes[0].body)
    return False

#----- Main Loop -----#


# -- Control whether the game run
running = True

skip_update = 0

keys_pressed_h = 0
keys_pressed_v = 0

while running:
    # -- Handle the events
    for event in pygame.event.get():
        # Check if we receive a QUIT event (for instance, if the user press the
        # close button of the wiendow) or if the user press the escape key.
        player_tank = tanks[0]
        if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_tank.accelerate()
                keys_pressed_v += 1

            elif event.key == pygame.K_DOWN:
                player_tank.decelerate()
                keys_pressed_v += 1

            elif event.key == pygame.K_LEFT:
                player_tank.turn_left()
                keys_pressed_h += 1

            elif event.key == pygame.K_RIGHT:
                player_tank.turn_right()
                keys_pressed_h += 1

            elif event.key == pygame.K_SPACE:
                player_tank.shoot(space, game_objects)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                keys_pressed_v -= 1
                if keys_pressed_v == 0:
                    player_tank.stop_moving()

            elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                keys_pressed_h -= 1
                if keys_pressed_h == 0:
                    player_tank.stop_turning()

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

    for tank in tanks:
        tank.try_grab_flag(flag)
        if tank.has_won():
            print(f"Tank {tank} has won!")
            running = False

        tank.post_update()

    handler = space.add_collision_handler(1, 2)
    handler.pre_solve = collision_bullet_tank
    handler = space.add_collision_handler(1, 3)
    handler.pre_solve = collision_bullet_box
    handler = space.add_collision_handler(1, 0)
    handler.pre_solve = collision_bullet_wall

    # -- Update Display

    # Display the background on the screen
    screen.blit(background, (0, 0))

    # <INSERT DISPLAY OBJECTS>
    # Update the display of the game objects on the screen
    for obj in game_objects:
        obj.update_screen(screen)

    # Update the display of the bases on the screen
    for base in bases:
        base.update_screen(screen)

    # Update the display of the tanks on the screen
    for tank in tanks:
        tank.update_screen(screen)

    flag.update_screen(screen)

    #   Redisplay the entire screen (see double buffer technique)
    pygame.display.flip()

    #   Control the game framerate
    clock.tick(FRAMERATE)
