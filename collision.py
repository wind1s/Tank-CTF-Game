from os import remove

from pymunk.vec2d import Vec2d
import ctfgame as init
import gameobjects as gameobj
import images as img
import createobjects as cobj


def remove_collision_object(obj, shape, space):
    if obj in init.game_objects:
        init.game_objects.remove(obj)
    space.remove(shape, shape.body)


def collision_bullet_tank(arb, space, _):
    bullet_shape = arb.shapes[0]
    tank_shape = arb.shapes[1]

    bullet_shape.parent.body.velocity = Vec2d(0, 0)
    remove_collision_object(bullet_shape.parent, bullet_shape, space)
    tank_shape.parent.respawn()

    for ai in init.ai_objects:
        if ai.tank is tank_shape.parent:
            ai.move_cycle = ai.move_cycle_gen()

    return True


def collision_bullet_box(arb, space, _):
    bullet_shape = arb.shapes[0]
    box_shape = arb.shapes[1]

    remove_collision_object(bullet_shape.parent, bullet_shape, space)

    box_collision_type = box_shape.parent.box_type
    if box_collision_type == gameobj.Box.WOODBOX_TYPE:
        remove_collision_object(box_shape.parent, box_shape, space)

    return True


def collision_bullet_wall(arb, space, _):
    bullet_shape = arb.shapes[0]
    remove_collision_object(bullet_shape.parent, bullet_shape, space)

    return True


def add_collision_handlers(game_map, space):
    space.add(*cobj.create_map_bounds(game_map, space.static_body))
    space.add_collision_handler(1, 2).pre_solve = collision_bullet_tank
    space.add_collision_handler(1, 3).pre_solve = collision_bullet_box
    space.add_collision_handler(1, 0).pre_solve = collision_bullet_wall

    return space
