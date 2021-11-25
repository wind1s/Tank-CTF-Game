from baseobjects import (GamePhysicsObject, GameVisibleObject)
import images as img
import pymunk as pym
import math


def clamp(min_max, value):
    """ Convenient helper function to bound a value to a specific interval. """
    return min(max(-min_max, value), min_max)


class Tank(GamePhysicsObject):
    """ Extends GamePhysicsObject and handles aspects which are specific to our tanks. """

    # Constant values for the tank, acessed like: Tank.ACCELERATION
    # You can add more constants here if needed later
    ACCELERATION = 1
    NORMAL_MAX_SPEED = 4
    FLAG_MAX_SPEED = NORMAL_MAX_SPEED * 0.5
    SHOOT_COOLDOWN_MS = 0.5 * 1000.0

    def __init__(self, x, y, orientation, sprite, space):
        super().__init__(x, y, orientation, sprite, space, True)
        # Define variable used to apply motion to the tanks
        self.acceleration = 0  # 1 forward, 0 for stand still, -1 for backwards
        self.rotation = 0  # 1 clockwise, 0 for no rotation, -1 counter clockwise
        self.body.angular_velocity = 0

        self.flag = None                      # This variable is used to access the flag object, if the current tank is carrying the flag
        self.max_speed = Tank.NORMAL_MAX_SPEED     # Impose a maximum speed to the tank
        # Define the start position, which is also the position where the tank has to return with the flag
        self.start_position = pym.Vec2d(x, y)
        self.start_orientation = orientation

        self.shape.collision_type = 2
        self.shoot_wait = 0

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
            0, self.ACCELERATION * self.acceleration).rotated(self.body.angle)
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
        # If the tank carries the flag, then update the positon of the flag
        if(self.flag != None):
            self.flag.x = self.body.position[0]
            self.flag.y = self.body.position[1]
            self.flag.orientation = -math.degrees(self.body.angle)
        # Else ensure that the tank has its normal max speed
        else:
            self.max_speed = Tank.NORMAL_MAX_SPEED

    def update_cooldown(self, clock):
        # Reduce timers by time this tick took.
        self.shoot_wait -= clock.get_time() if self.shoot_wait >= 0 else 0

    def try_grab_flag(self, flag):
        """ Call this function to try to grab the flag, if the flag is not on other tank
            and it is close to the current tank, then the current tank will grab the flag.
        """
        # Check that the flag is not on other tank
        if(not flag.is_on_tank):
            # Check if the tank is close to the flag
            flag_pos = pym.Vec2d(flag.x, flag.y)
            if((flag_pos - self.body.position).length < 0.5):
                # Grab the flag !
                self.flag = flag
                flag.is_on_tank = True
                self.max_speed = Tank.FLAG_MAX_SPEED

    def try_drop_flag(self):
        if self.flag != None:
            self.flag.is_on_tank = False
            self.flag = None

    def has_won(self):
        """ Check if the current tank has won (if it is has the flag and it is close to its start position). """
        return self.flag != None and (
            self.start_position - self.body.position).length < 0.2

    def shoot(self, space, game_objects):
        """ Call this function to shoot a missile """
        if self.shoot_wait > 0:
            return

        self.shoot_wait = self.SHOOT_COOLDOWN_MS
        offset_vector = pym.Vec2d(0, 0.5).rotated(self.body.angle)
        bullet_x = self.body.position[0] + offset_vector.x
        bullet_y = self.body.position[1] + offset_vector.y
        orientation = self.body.angle

        game_objects.append(
            Bullet(
                self, bullet_x, bullet_y, orientation, 3.5, img.bullet,
                space))

    def get_shot(self):
        pass

    def respawn(self):
        self.try_drop_flag()

        start_x = self.start_position[0]
        start_y = self.start_position[1]
        start_angle = math.radians(self.start_orientation)
        self.stop_moving()
        self.stop_turning()

        self.set_pos(start_x, start_y, start_angle)

    def set_pos(self, x, y, angle):
        self.body.position = pym.Vec2d(x, y)
        self.body.angle = angle

    def get_pos(self):
        return self.body.position

    def get_angle(self):
        return self.body.angle


class Bullet(GamePhysicsObject):

    def __init__(self, tank, x, y, orientation, speed, sprite, space):
        super().__init__(x, y, orientation, sprite, space, True)
        # Define variable used to apply motion to the tanks

        self.tank = tank
        self.speed = speed  # Impose a maximum speed to the tank
        # Define the start position, which is also the position where the tank has to return with the flag
        self.start_position = pym.Vec2d(x, y)
        self.body.angle = orientation

        self.shape.collision_type = 1

    def update(self):
        """ A function to update the objects coordinates. Gets called at every tick of the game. """

        # Creates a vector in the direction we want accelerate / decelerate
        speed_vector = pym.Vec2d(
            0, self.speed).rotated(self.body.angle)
        # Applies the vector to our velocity
        self.body.velocity += speed_vector


class Box(GamePhysicsObject):
    """ This class extends the GamePhysicsObject to handle box objects. """

    GRASS_TYPE = 0
    ROCKBOX_TYPE = 1
    WOODBOX_TYPE = 2
    METALBOX_TYPE = 3

    def __init__(self, x, y, sprite, movable, space, destructable, box_type):
        """ It takes as arguments the coordinate of the starting position of the box (x,y) and the box model (boxmodel). """
        super().__init__(x, y, 0, sprite, space, movable)
        self.destructable = destructable
        self.box_type = box_type
        self.shape.collision_type = 3


def get_box_with_type(x, y, box_type, space):
    (x, y) = (x + 0.5, y + 0.5)  # Offsets the coordinate to the center of the tile
    if box_type == 1:  # Creates a non-movable non-destructable rockbox
        return Box(x, y, img.rockbox, False, space, False, Box.ROCKBOX_TYPE)
    if box_type == 2:  # Creates a movable destructable woodbox
        return Box(x, y, img.woodbox, True, space, True, Box.WOODBOX_TYPE)
    if box_type == 3:  # Creates a movable non-destructable metalbox
        return Box(x, y, img.metalbox, True, space, False, Box.METALBOX_TYPE)


class Flag(GameVisibleObject):
    """ This class extends GameVisibleObject for representing flags."""

    def __init__(self, x, y):
        self.is_on_tank = False
        super().__init__(x, y, img.flag)


class Base(GameVisibleObject):
    def __init__(self, x, y, sprite):
        super().__init__(x, y, sprite)
