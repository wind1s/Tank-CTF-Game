from gameobjects import (Tank, Bullet, Box)


class CollisionHandler():
    """ Singleton that initializes collision handlers. """

    def __init__(self, space, game_objects, ai_objects, clock):
        self.space = space
        self.game_objects = game_objects
        self.ai_objects = ai_objects
        self.clock = clock

        handler_data = (
            (Bullet.COLLISION_TYPE, Box.COLLISION_TYPE,
             self.collision_bullet, self.collision_box_bullet),
            (Bullet.COLLISION_TYPE, Tank.COLLISION_TYPE,
             self.collision_bullet, self.collision_tank_bullet),
            (Bullet.COLLISION_TYPE, Bullet.COLLISION_TYPE,
             self.collision_bullet, self.collision_bullet),
            (Bullet.COLLISION_TYPE, 0,
             self.collision_bullet, lambda *_: None)  # Default bullet collision handler.
        )

        for data in handler_data:
            self.add_collision_handler(*data)

    def add_collision_handler(self, type1, type2, handler1, handler2):
        """ Adds a new collision handler to the space. """
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
        bullet.destroy(bullet_shape, self.game_objects, self.space, self.clock)

    def collision_tank_bullet(self, tank_shape):
        """ Handles tank collision with bullets."""
        tank = tank_shape.parent
        tank.get_shot()

        if tank.respawn(self.game_objects):

            # Reset ai move cycle.
            for ai in self.ai_objects:
                if ai.tank is tank:
                    ai.move_cycle = ai.move_cycle_gen()
                    break

    def collision_box_bullet(self, box_shape):
        """ Handles box collision with bullets. """
        box = box_shape.parent

        box.get_shot()
        box.destroy(box_shape, self.game_objects, self.space, self.clock)
