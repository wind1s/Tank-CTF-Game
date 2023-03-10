import math
import pymunk as pym
from utility import (reduce_until_zero, seconds_to_ms,
                     clamp, get_tile_position, add_object, remove_object)
from baseobjects import (GamePhysicsObject, GameVisibleObject)
from sounds import CTFSounds
from images import CTFImages


class Tank(GamePhysicsObject):
    """ Extends GamePhysicsObject and handles aspects which are specific to our tanks. """

    COLLISION_TYPE = 2
    ACCELERATION = 1
    NORMAL_MAX_SPEED = 2.5
    FLAG_SPEED_REDUCTION = 0.7
    HIT_POINTS = 3
    SHOOT_COOLDOWN_MS = seconds_to_ms(0.8)
    SPAWN_PROTECTION_MS = seconds_to_ms(2)

    def __init__(
            self, name, x, y, orientation, sprite, space, clock, hit_points,
            speed):
        super().__init__(x, y, orientation, sprite, space, True)

        self.acceleration = 0  # 1 forward, 0 for stand still, -1 for backwards
        self.rotation = 0  # 1 clockwise, 0 for no rotation, -1 counter clockwise
        self.body.angular_velocity = 0
        self.space = space
        self.clock = clock
        self.shape.collision_type = self.COLLISION_TYPE

        # This variable is used to access the flag object, if the current tank is carrying the flag
        self.flag = None
        self.max_speed = speed
        self.bullet_max_speed = Bullet.MAX_SPEED
        assert self.max_speed < self.bullet_max_speed, "Tank speed greater than bullet speed! Possible to drive into own bullets."

        # Define the start position, which is also the position where the tank has to return with the flag
        self.start_position = pym.Vec2d(x, y)
        self.start_orientation = orientation

        self.shoot_cooldown = 0
        self.protection_time = self.SPAWN_PROTECTION_MS  # Time in ms
        self.max_hit_points = hit_points
        self.hit_points = hit_points
        self.name = name

    def accelerate(self):
        """ Call this function to make the tank move forward. """
        self.acceleration = 1

    def stop_moving(self):
        """ Call this function to make the tank stop moving. """
        self.acceleration = 0
        self.body.velocity = pym.Vec2d.zero()

    def decelerate(self):
        """ Call this function to make the tank move backward. """
        self.acceleration = -1

    def turn_left(self):
        """ Makes the tank turn left (counter clock-wise). """
        self.rotation = -1

    def turn_right(self):
        """ Makes the tank turn right (clock-wise). """
        self.rotation = 1

    def stop_turning(self):
        """ Call this function to make the tank stop turning. """
        self.rotation = 0
        self.body.angular_velocity = 0

    def update(self):
        """ A function to update the objects coordinates. Gets called at every tick of the game. """

        # Creates a vector in the direction we want accelerate / decelerate
        acceleration_vector = pym.Vec2d(
            0, self.ACCELERATION * self.acceleration).rotated(self.get_angle())
        # Applies the vector to our velocity
        self.body.velocity += acceleration_vector

        # Makes sure that we dont exceed our speed limit
        velocity = clamp(self.max_speed, self.body.velocity.length)
        self.body.velocity = pym.Vec2d(
            velocity, 0).rotated(
            self.body.velocity.angle)

        # Updates the rotation
        self.body.angular_velocity += self.rotation * self.ACCELERATION
        self.body.angular_velocity = clamp(
            self.max_speed, self.body.angular_velocity)

    def post_update(self):
        """ Updates things tha depends on the tanks state. Such as the flags position. """
        # If the tank carries the flag, then update the positon of the flag
        self.update_timers()

        if self.flag != None:
            self.flag.target_base = self.start_position
            self.flag.x, self.flag.y = self.get_pos()
            self.flag.orientation = -math.degrees(self.get_angle())

    def update_timers(self):
        # Reduce timers by time this tick took.
        time_passed = self.clock.get_time()

        self.shoot_cooldown = reduce_until_zero(
            self.shoot_cooldown, time_passed)
        self.protection_time = reduce_until_zero(
            self.protection_time, time_passed)

    def try_grab_flag(self, flag):
        """ Call this function to try to grab the flag, if the flag is not on other tank
            and it is close to the current tank, then the current tank will grab the flag.
        """
        # Check that the flag is not on other tank
        if not flag.is_on_tank:
            # Check if the tank is close to the flag
            flag_pos = pym.Vec2d(flag.x, flag.y)
            if (flag_pos - self.get_pos()).length < 0.5:
                # Grab the flag !
                self.flag = flag
                flag.is_on_tank = True
                self.max_speed *= self.FLAG_SPEED_REDUCTION

    def try_drop_flag(self):
        """ If tank has the flag, drop it."""
        if self.flag is not None:
            self.flag.x, self.flag.y = get_tile_position(
                self.get_pos()) + pym.Vec2d(0.5, 0.5)
            self.flag.is_on_tank = False
            self.flag = None
            self.max_speed /= self.FLAG_SPEED_REDUCTION

    def has_won(self):
        """ Check if the current tank has won (if it is has the flag and it is close to its start position). """
        return self.flag is not None and (
            self.start_position - self.body.position).length < 0.2

    def shoot(self, game_objects):
        """ Call this function to shoot a missile """
        if self.shoot_cooldown > 0:
            return

        CTFSounds.tank_shoot.play()

        self.shoot_cooldown = self.SHOOT_COOLDOWN_MS
        tank_angle = self.get_angle()
        offset_vector = pym.Vec2d(0, 0.5).rotated(tank_angle)
        bullet_vec = self.get_pos() + offset_vector

        add_object(game_objects, Bullet.create_bullet(
            *bullet_vec, tank_angle, self.bullet_max_speed, self.space))

    def get_shot(self):
        """ Reduces hitpoints if the tank has no protection. """
        # Spawn protection timer.
        if self.protection_time > 0:
            return

        self.hit_points -= 1

    def respawn(self, game_objects):
        """ Respawns the tank if it's hitpoints are 0. Returns if tank respawned. """
        if self.hit_points > 0:
            return False

        CTFSounds.tank_death.play()

        add_object(
            game_objects, Explosion.create_explosion(
                *self.get_pos(),
                CTFImages.regular_explosion, game_objects, self.clock))

        self.hit_points = self.max_hit_points
        self.shoot_cooldown = 0
        # Give tank respawn protection.
        self.protection_time = self.SPAWN_PROTECTION_MS

        self.try_drop_flag()

        # Reset tank movement and move it to its starting positions
        start_x = self.start_position[0]
        start_y = self.start_position[1]
        start_angle = math.radians(self.start_orientation)
        self.stop_moving()
        self.stop_turning()

        self.set_pos(start_x, start_y)
        self.set_angle(start_angle)

        return True

    def set_pos(self, x, y):
        """ Setter function for the tank position. """
        self.body.position = pym.Vec2d(x, y)

    def set_angle(self, angle):
        """ Setter function for the tank angle. """
        self.body.angle = angle

    def get_pos(self):
        """ Getter function for the tank position. """
        return self.body.position

    def get_angle(self):
        """ Getter function for the tank angle. """
        return self.body.angle


class Bullet(GamePhysicsObject):
    """ Extends GamePhysicsObject to represent a bullet object. """
    COLLISION_TYPE = 1
    MAX_SPEED = 4

    def __init__(self, x, y, orientation, speed, sprite, space):
        super().__init__(x, y, orientation, sprite, space, True)

        self.speed = speed
        self.start_position = pym.Vec2d(x, y)
        self.body.angle = orientation
        self.shape.collision_type = Bullet.COLLISION_TYPE

    def update(self):
        """ A function to update the objects coordinates. Gets called at every tick of the game. """

        # Creates a vector in the direction we want accelerate / decelerate
        speed_vector = pym.Vec2d(
            0, self.speed).rotated(self.body.angle)

        self.body.velocity += speed_vector

    def set_velocity(self, velocity):
        """ Setter function for the bullets velocity. """
        self.body.velocity = pym.Vec2d(0, velocity)

    def get_pos(self):
        """ Getter function for the bullets position. """
        return self.body.position

    @staticmethod
    def create_bullet(x, y, orientation, speed, space):
        """ Factory function for creating a bullet object. """
        return Bullet(x, y, orientation, speed, CTFImages.bullet, space)

    def destroy(self, shape, game_objects, space, clock):
        # Remove bullets velocity to remove knockback effect on other objects.
        self.set_velocity(0)
        remove_object(game_objects, self, shape, space)
        add_object(game_objects, Explosion.create_explosion(
            *self.get_pos(), CTFImages.small_explosion, game_objects, clock))
        return True


class Box(GamePhysicsObject):
    """ This class extends the GamePhysicsObject to handle box objects. """
    COLLISION_TYPE = 3
    GRASS_TYPE = 0
    ROCKBOX_TYPE = 1
    WOODBOX_TYPE = 2
    METALBOX_TYPE = 3
    MAX_HIT_POINTS = 2

    def __init__(
            self, x, y, sprite, movable, space, destructable, box_type):
        """ It takes as arguments the coordinate of the starting position of the box (x,y) and the box model (boxmodel). """
        super().__init__(x, y, 0, sprite, space, movable)
        self.destructable = destructable
        self.box_type = box_type
        self.hit_points = Box.MAX_HIT_POINTS
        self.shape.collision_type = Box.COLLISION_TYPE

    def get_pos(self):
        return self.body.position

    @ staticmethod
    def create_box(x, y, box_type, space):
        """ Creates a box instance with specified type. """
        # Offsets the coordinate to the center of the tile
        (x, y) = (x + 0.5, y + 0.5)

        if box_type == Box.ROCKBOX_TYPE:  # Creates a non-movable non-destructable rockbox
            return Box(
                x, y, CTFImages.rockbox, False, space, False, Box.ROCKBOX_TYPE)

        if box_type == Box.WOODBOX_TYPE:  # Creates a movable destructable woodbox
            return Box(
                x, y, CTFImages.woodbox, True, space, True, Box.WOODBOX_TYPE)

        if box_type == Box.METALBOX_TYPE:  # Creates a movable non-destructable metalbox
            return Box(
                x, y, CTFImages.metalbox, True, space, False, Box.METALBOX_TYPE)

    def get_shot(self):
        """ Performs logic when box gets shot. """
        if self.box_type != Box.WOODBOX_TYPE:
            return

        self.hit_points -= 1

    def destroy(self, shape, game_objects, space, clock):
        if self.hit_points > 0:
            return False

        CTFSounds.box_break.play()
        add_object(game_objects, Explosion.create_explosion(
            *self.get_pos(), CTFImages.regular_explosion, game_objects, clock))
        remove_object(game_objects, self, shape, space)

        return True


class Flag(GameVisibleObject):
    """ This class extends GameVisibleObject for representing flags."""

    def __init__(self, x, y, sprite):
        super().__init__(x, y, sprite)
        self.is_on_tank = False
        self.target_base = pym.Vec2d(0, 0)

    @ staticmethod
    def create_flag(x, y):
        """ Factory function for creating a flag object. """
        return Flag(x, y, CTFImages.flag)

    def get_pos(self):
        """ Getter function for the flags position. """
        return pym.Vec2d(self.x, self.y)


class Base(GameVisibleObject):
    def __init__(self, x, y, sprite):
        super().__init__(x, y, sprite)

    @ staticmethod
    def create_base(x, y, sprite):
        """ Factory function for creating a base object. """
        return Base(x, y, sprite)


class Explosion(GameVisibleObject):
    def __init__(self, x, y, sprite, game_objects, clock):
        super().__init__(x, y, sprite)
        self.explosion_time = 0.7 * 1000  # time in milliseconds
        self.game_objects = game_objects
        self.clock = clock

    def post_update(self):
        """ post_update override for updating the explosion object. """
        self.update_explosion()

    def update_explosion(self):
        """ Updates the explosion timer and removes it if timer expires. """
        # Reduce timers by time this tick took.
        self.explosion_time = reduce_until_zero(
            self.explosion_time, self.clock.get_time())

        if self.explosion_time < 0:
            self.game_objects.remove(self)

    @ staticmethod
    def create_explosion(x, y, sprite, game_objects, clock):
        """ Factory function for creating a explosion object. """
        return Explosion(x, y, sprite, game_objects, clock)
