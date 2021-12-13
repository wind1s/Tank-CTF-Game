from gameobjects import Tank, Bullet, Explosion, Box
from utility import remove_object, add_object
from sounds import *


class CollisionHandler():
    def __init__(self, space, game_objects, ai_objects, clock):
        self.space = space
        self.game_objects = game_objects
        self.ai_objects = ai_objects
        self.clock = clock

        self.add_collision_handler(
            Bullet.COLLISION_TYPE, Box.COLLISION_TYPE,
            self.collision_bullet, self.collision_box_bullet)

        self.add_collision_handler(
            Bullet.COLLISION_TYPE, Tank.COLLISION_TYPE,
            self.collision_bullet, self.collision_tank_bullet)

        # Default collision handler.
        self.add_collision_handler(
            Bullet.COLLISION_TYPE, 0,
            self.collision_bullet, lambda *_: None)

    def add_collision_handler(self, type1, type2, handler1, handler2):
        self.space.add_collision_handler(
            type1, type2).pre_solve = self.collision_handler_generator(
            handler1, handler2)

    def collision_handler_generator(self, obj1_handler, obj2_handler):
        """ Generates a collison handler for two objects using respective object collision handler. """
        def collision_handler(arb, *_):
            shape1 = arb.shapes[0]
            shape2 = arb.shapes[1]
            obj1_handler(shape1)
            obj2_handler(shape2)

            return True

        return collision_handler

    def collision_bullet(self, bullet_shape):
        """ Handles bullet collisions. """
        bullet = bullet_shape.parent

        # Remove bullets velocity to remove knockback effect on other objects.
        bullet.set_velocity(0)
        remove_object(self.game_objects, bullet, bullet_shape, self.space)

        return True

    def collision_tank_bullet(self, tank_shape):
        """ Handles tank collision with bullets."""
        tank = tank_shape.parent
        tank.get_shot()

        if tank.respawn(self.game_objects):
            for ai in self.ai_objects:
                if ai.tank is tank:
                    ai.move_cycle = ai.move_cycle_gen()

    def collision_box_bullet(self, box_shape):
        """ Handles box collision with bullets. """
        box = box_shape.parent
        box_collision_type = box.box_type

        if box_collision_type == Box.WOODBOX_TYPE:
            box.get_shot()

            if box.hit_points <= 0:
                CTFSounds.box_break.play()
                add_object(self.game_objects, Explosion.create_explosion(
                    *box.get_pos(), self.game_objects, self.clock))
                remove_object(self.game_objects, box, box_shape, self.space)
