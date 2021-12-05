from gameobjects import Tank, Bullet, Explosion, Box
from images import CTFImages


class CollisionHandler():
    def __init__(self, space, game_objects, ai_objects):
        self.space = space
        self.game_objects = game_objects
        self.ai_objects = ai_objects

        self.add_collision_handler(
            Bullet.COLLISION_TYPE, Box.COLLISION_TYPE,
            self.collision_bullet, self.collision_box_bullet)

        self.add_collision_handler(
            Bullet.COLLISION_TYPE, Tank.COLLISION_TYPE,
            self.collision_bullet, self.collision_tank_bullet)

        self.add_collision_handler(
            Bullet.COLLISION_TYPE, 0,
            self.collision_bullet, lambda *_: None)

    def add_collision_handler(self, type1, type2, handler1, handler2):
        self.space.add_collision_handler(
            type1, type2).pre_solve = self.collision_handler_generator(
            handler1, handler2)

    def remove_object(self, obj, shape):
        """ Removes a physics object and it's body. """
        if obj in self.game_objects:
            self.game_objects.remove(obj)
        self.space.remove(shape, shape.body)

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
        self.game_objects.append(Explosion(
            *bullet.get_pos(), CTFImages.explosion, self.game_objects))

        bullet.set_velocity(0)
        self.remove_object(bullet, bullet_shape)

        return True

    def collision_tank_bullet(self, tank_shape):
        """ Handles tank collision with bullets."""
        tank = tank_shape.parent
        tank.hit_points -= 1

        if tank.hit_points <= 0:
            tank.respawn()

            for ai in self.ai_objects:
                if ai.tank is tank:
                    ai.move_cycle = ai.move_cycle_gen()

    def collision_box_bullet(self, box_shape):
        """ Handles box collision with bullets. """
        box = box_shape.parent
        box_collision_type = box.box_type

        if box_collision_type == Box.WOODBOX_TYPE:
            box.hit_points -= 1

            if box.hit_points <= 0:
                self.remove_object(box, box_shape)
