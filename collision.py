from os import remove
import initgame as init
import gameobjects as gameobj
import images as img
import createobjects as cobj


def remove_collision_object(obj, shape, space):
    if obj in init.game_objects:
        init.game_objects.remove(obj)
    space.remove(shape, shape.body)


def add_collision_handlers(game_map, space):
    space.add(*cobj.create_map_bounds(game_map, space.static_body))
    space.add_collision_handler(1, 2).pre_solve = collision_bullet_tank
    space.add_collision_handler(1, 3).pre_solve = collision_bullet_box
    space.add_collision_handler(1, 0).pre_solve = collision_bullet_wall

    return space


def collision_bullet_tank(arb, space, _):
    bullet_shape = arb.shapes[0]
    tank_shape = arb.shapes[1]

    remove_collision_object(bullet_shape.parent, bullet_shape, space)
    tank_shape.parent.respawn()

    return True


def collision_bullet_box(arb, space, _):
    bullet_shape = arb.shapes[0]
    box_shape = arb.shapes[1]

    remove_collision_object(bullet_shape.parent, bullet_shape, space)

    box_collision_type = box_shape.parent.type
    if box_collision_type == 1:
        remove_collision_object(box_shape.parent, box_shape, space)
    # elif box_collision_type ==

    return True


def collision_bullet_wall(arb, space, _):
    bullet_shape = arb.shapes[0]
    remove_collision_object(bullet_shape.parent, bullet_shape, space)

    return True
