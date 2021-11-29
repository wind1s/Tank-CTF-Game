import ctfgame
import gameobjects as gobj
import images as img
import createobjects as cobj


def remove_object(obj, shape, space):
    """ Removes a game object and it's body. """
    if obj in ctfgame.game_objects:
        ctfgame.game_objects.remove(obj)
    space.remove(shape, shape.body)


def collision_handler_generator(obj1_handler, obj2_handler):
    """ Generates a collison handler for two objects using respective object collision handler. """
    def collision_handler(arb, space, _):
        shape1 = arb.shapes[0]
        shape2 = arb.shapes[1]
        obj1_handler(shape1, space)
        obj2_handler(shape2, space)

        return True

    return collision_handler


def collision_bullet(bullet_shape, space):
    """ Handles bullet collisions. """
    bullet = bullet_shape.parent
    ctfgame.game_objects.append(gobj.Explosion(
        *bullet.get_pos(), img.explosion_img, ctfgame.game_objects))

    bullet.set_velocity(0)
    remove_object(bullet, bullet_shape, space)

    return True


def collision_tank_bullet(tank_shape, *_):
    """ Handles tank collision with bullets."""
    tank = tank_shape.parent

    tank.hit_points -= 1
    if tank.hit_points <= 0:
        tank.respawn()

        for ai in ctfgame.ai_objects:
            if ai.tank is tank:
                ai.move_cycle = ai.move_cycle_gen()


def collision_box_bullet(box_shape, space):
    """ Handles box collision with bullets. """
    box = box_shape.parent
    box_collision_type = box.box_type

    if box_collision_type == gobj.Box.WOODBOX_TYPE:
        box.hit_points -= 1
        
        if box.hit_points <= 0:
            remove_object(box, box_shape, space)


def add_collision_handlers(game_map, space):
    space.add(*cobj.create_map_bounds(game_map, space.static_body))
    space.add_collision_handler(
        gobj.Bullet.COLLISION_TYPE, gobj.Box.COLLISION_TYPE).pre_solve = collision_handler_generator(
        collision_bullet, collision_box_bullet)
    space.add_collision_handler(
        gobj.Bullet.COLLISION_TYPE, gobj.Tank.COLLISION_TYPE).pre_solve = collision_handler_generator(
        collision_bullet, collision_tank_bullet)

    # Handler for map bounds.
    space.add_collision_handler(
        gobj.Bullet.COLLISION_TYPE, 0).pre_solve = collision_handler_generator(
        collision_bullet, lambda *_: None)

    return space
