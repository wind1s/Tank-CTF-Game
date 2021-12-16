import math
from utility import (remove_object, physics_to_display)
import pygame as pyg
import pymunk as pym
from config import DEBUG, TILE_SIZE


class GameObject:
    """ Mostly handles visual aspects (pygame) of an object.
        Subclasses need to implement two functions:
        - screen_position    that will return the position of the object on the screen
        - screen_orientation that will return how much the object is rotated on the screen (in degrees). """

    def __init__(self, sprite):
        self.sprite = sprite

    def update(self):
        """ Placeholder, supposed to be implemented in a subclass.
            Should update the current state (after a tick) of the object."""
        return

    def post_update(self):
        """ Should be implemented in a subclass. Make updates that depend on
            other objects than itself."""

        return

    def update_screen(self, screen):
        """ Updates the visual part of the game. Should NOT need to be changed
            by a subclass."""
        sprite = self.sprite

        p = self.screen_position()  # Get the position of the object (pygame coordinates)
        # Rotate the sprite using the rotation of the object
        sprite = pyg.transform.rotate(sprite, self.screen_orientation())

        # The position of the screen correspond to the center of the object,
        # but the function screen.blit expect to receive the top left corner
        # as argument, so we need to adjust the position p with an offset
        # which is the vector between the center of the sprite and the top left
        # corner of the sprite
        offset = pym.Vec2d(sprite.get_size()) / 2.
        p = p - offset
        screen.blit(sprite, p)  # Copy the sprite on the screen

    def destroy(self, shape, game_objects, space, clock):
        remove_object(game_objects, self, shape, space)
        return True


class GamePhysicsObject(GameObject):
    """ This class extends GameObject and it is used for objects which have a
        physical shape (such as tanks and boxes). This class handle the physical
        interaction of the objects.
    """

    def __init__(self, x, y, orientation, sprite, space, movable):
        """ Takes as parameters the starting coordinate (x,y), the orientation, the sprite (aka the image
            representing the object), the physic engine object (space) and whether the object can be
            moved (movable).
        """

        super().__init__(sprite)

        # Half dimensions of the object converted from screen coordinates to physic coordinates
        half_width = 0.5 * self.sprite.get_width() / TILE_SIZE
        half_height = 0.5 * self.sprite.get_height() / TILE_SIZE

        # Physical objects have a rectangular shape, the points correspond to the corners of that shape.
        self.points = [[-half_width, -half_height],
                       [-half_width, half_height],
                       [half_width, half_height],
                       [half_width, -half_height]]
        # Create a body (which is the physical representation of this game object in the physic engine)
        if(movable):
            # Create a movable object with some mass and moments
            # (considering the game is a top view game, with no gravity,
            # the mass is set to the same value for all objects)."""
            mass = 10
            moment = pym.moment_for_poly(mass, self.points)
            self.body = pym.Body(mass, moment)
        else:
            # Create a non movable (static) object
            self.body = pym.Body(body_type=pym.Body.STATIC)

        self.body.position = x, y
        # orientation is provided in degress, but pymunk expects radians.
        self.body.angle = math.radians(orientation)
        # Create a polygon shape using the corner of the rectangle
        self.shape = pym.Poly(self.body, self.points)
        self.shape.parent = self

        # Set some value for friction and elasticity, which defines interraction in case of a colision
        # self.shape.friction = 0.5
        # self.shape.elasticity = 0.1

        # Add the object to the physic engine
        if(movable):
            space.add(self.body, self.shape)
        else:
            space.add(self.shape)

    def screen_position(self):
        """ Converts the body's position in the physics engine to screen coordinates. """
        return physics_to_display(self.body.position)

    def screen_orientation(self):
        """ Angles are reversed from the engine to the display. """
        return -math.degrees(self.body.angle)

    def update_screen(self, screen):
        super().update_screen(screen)
        # debug draw
        if DEBUG:
            ps = [self.body.position+p for p in self.points]

            ps = [physics_to_display(p) for p in ps]
            ps += [ps[0]]
            pyg.draw.lines(
                screen, pyg.color.THECOLORS["red"],
                False, ps, 1)


class GameVisibleObject(GameObject):
    """ This class extends GameObject for object that are visible on screen but have no physical representation (bases and flag) """

    def __init__(self, x, y, sprite):
        """ It takes argument the coordinates (x,y) and the sprite. """
        self.x = x
        self.y = y
        self.orientation = 0
        super().__init__(sprite)

    def screen_position(self):
        return physics_to_display(pym.Vec2d(self.x, self.y))

    def screen_orientation(self):
        return self.orientation
