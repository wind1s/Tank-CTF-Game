import pymunk as pym
import random as rand
import math
import utility
from collections import deque
from gameobjects import (Tank, Flag, Box)


class Ai:
    """ 
    A simple ai that finds the shortest path to the target using
    a breadth first search. Also capable of shooting other tanks and or wooden
    boxes. 
    """

    MIN_ANGLE_DIF = math.radians(1.5)
    MIN_POS_DIFF = 0.1

    def __init__(self, tank, game_objects, space, current_map):
        self.tank = tank
        self.game_objects = game_objects
        self.space = space
        self.current_map = current_map
        self.flag = None
        self.MAX_X = current_map.width - 1
        self.MAX_Y = current_map.height - 1

        self.path = deque()
        self.move_cycle = self.move_cycle_gen()

        # Buff tanks.
        self.tank.max_speed = self.tank.max_speed*1.3
        self.tank.bullet_max_speed = self.tank.bullet_max_speed*1.5

    def decide(self):
        """ Main decision function that gets called on every tick of the game. """
        next(self.move_cycle)
        self.maybe_shoot()

    def find_target_point(self, origin, angle, length):
        offset = pym.Vec2d(0, length).rotated(angle)
        return origin + offset

    def maybe_shoot(self):
        """ Makes a raycast query in front of the tank. If another tank
            or a wooden box is found, then we shoot.
        """
        start = self.find_target_point(
            self.tank.get_pos(), self.tank.get_angle(), 0.5)
        end = self.find_target_point(
            start, self.tank.get_angle(),
            max(self.MAX_X, self.MAX_Y))
        type_hit = self.space.segment_query_first(
            start, end, 0, pym.ShapeFilter())

        if hasattr(
                type_hit, "shape") and hasattr(
                type_hit.shape, "parent"):

            parent = type_hit.shape.parent

            if isinstance(parent, Tank) or (
                    isinstance(parent, Box) and parent.box_type
                    in (Box.WOODBOX_TYPE, Box.METALBOX_TYPE)):
                self.tank.shoot(self.space, self.game_objects)

    def turn(self, next_coord):
        """ Turns the tank toward a coordinate. """

        target_angle = utility.angle_between_vectors(
            self.tank.get_pos(), next_coord)

        current_diff = utility.periodic_difference_of_angles(
            self.tank.get_angle(), target_angle)

        if 0 <= current_diff <= math.pi:
            self.tank.turn_left()
        else:
            self.tank.turn_right()

    def correct_angle(self, next_coord):
        """ Checks if tank is standing close to the same angle as the coord. """
        def angle_diff():
            """ Adds a random value to position diff to make ai more human. """
            return Ai.MIN_ANGLE_DIF + math.radians(rand.random())

        target_angle = utility.angle_between_vectors(
            self.tank.get_pos(), next_coord)

        current_diff = utility.periodic_difference_of_angles(
            self.tank.get_angle(), target_angle)

        # Add random value to make ai's movement different.
        return abs(current_diff) <= angle_diff()

    def correct_pos(self, next_coord):
        """ Checks if the tank is standing close enought to the coord. """
        def pos_diff():
            """ Adds a random value to position diff to make ai more human. """
            return Ai.MIN_POS_DIFF + rand.random()/10

        return self.tank.get_pos().get_distance(next_coord) <= pos_diff()

    def move_cycle_gen(self):
        """ A generator that iteratively goes through all the required steps
            to move to our goal.
        """

        while True:
            path = self.find_shortest_path(
                self.tank.get_pos(),
                self.get_target_tile())
            if not path:
                yield
                continue  # Start from the top of our cycle

            path = self.shorten_path(path)
            path.popleft()

            next_coord = path.popleft() + pym.Vec2d(0.5, 0.5)
            self.tank.stop_moving()
            yield

            self.turn(next_coord)

            while not self.correct_angle(next_coord):
                yield

            self.tank.stop_turning()
            yield

            self.tank.accelerate()

            while not self.correct_pos(next_coord):
                yield

            self.tank.stop_moving()

    def shorten_path(self, path):
        """ Shortens the path generated from a BFS search."""
        new_path = deque()

        def path_tile_is_turn(i):
            return path[i-1].x != path[i+1].x and path[i-1].y != path[i+1].y

        new_path.append(path[0])
        new_path.extend([path[i] for i in range(
            1, len(path) - 1) if path_tile_is_turn(i)])
        new_path.append(path[-1])

        return new_path

    def find_shortest_path(self, origin, target):
        """ 
        A simple Breadth First Search using integer coordinates as our nodes.
        Edges are calculated as we go, using an external function.
        """
        origin = utility.get_tile_position(origin)
        paths = {origin.int_tuple: [origin]}
        queue = deque([origin])
        visited = set()

        while queue:
            node = queue.popleft()

            if node == target:
                shortest_path = paths[node.int_tuple].copy()
                shortest_path.append(node)
                return deque(shortest_path)

            for neighbor in self.get_tile_neighbors(node):
                if neighbor.int_tuple not in visited:
                    queue.append(neighbor)
                    visited.add(neighbor.int_tuple)
                    paths[neighbor.int_tuple] = paths[node.int_tuple].copy()
                    paths[neighbor.int_tuple].append(neighbor)

            del paths[node.int_tuple]

        return deque([])

    def get_target_tile(self):
        """ Returns position of the flag if we don't have it. If we do have the flag,
            return the position of our home base.
        """
        if self.tank.flag is not None:
            x, y = self.tank.start_position
        else:
            self.get_flag()  # Ensure that we have initialized it.
            x, y = self.flag.x, self.flag.y
        return pym.Vec2d(int(x), int(y))

    def get_flag(self):
        """ This has to be called to get the flag, since we don't know
            where it is when the Ai object is initialized.
        """
        if self.flag is None:
            # Find the flag in the game objects list
            for obj in self.game_objects:
                if isinstance(obj, Flag):
                    self.flag = obj
                    break
        return self.flag

    def get_tile_neighbors(self, coord_vec):
        """ Returns all bordering grid squares of the input coordinate.
            A bordering square is only considered accessible if it is grass
            or a wooden box.
        """
        pos_vec = utility.get_tile_position(coord_vec)
        # Find the coordinates of the tiles' four neighbors
        neighbors = [
            pos_vec + pym.Vec2d(0, -1),
            pos_vec + pym.Vec2d(-1, 0),
            pos_vec + pym.Vec2d(0, 1),
            pos_vec + pym.Vec2d(1, 0)]

        return filter(self.filter_tile_neighbors, neighbors)

    def filter_tile_neighbors(self, coord):
        """ Checks if the neighbor tile is ok to travel to. """
        x_in_bounds = coord.x >= 0 and coord.x <= self.MAX_X
        y_in_bounds = coord.y >= 0 and coord.y <= self.MAX_Y

        if not (x_in_bounds and y_in_bounds):
            return False

        box_type = self.current_map.box_at(coord.x, coord.y)
        box_is_wood = box_type == Box.WOODBOX_TYPE
        box_is_grass = box_type == Box.GRASS_TYPE
        box_is_metal = box_type == Box.METALBOX_TYPE

        return box_is_grass or box_is_wood or box_is_metal
