import math
from pymunk import Vec2d
import gameobjects
from collections import deque
from random import random

# NOTE: use only 'map0' during development!

# 3 degrees, a bit more than we can turn each tick
MIN_ANGLE_DIF = math.radians(2)
MIN_POS_DIFF = 0.1


def angle_between_vectors(vec1, vec2):
    """ Since Vec2d operates in a cartesian coordinate space we have to
        convert the resulting vector to get the correct angle for our space.
    """
    vec = vec1 - vec2
    vec = vec.perpendicular()
    return vec.angle


def periodic_difference_of_angles(angle1, angle2):
    return (angle1 % (2*math.pi)) - (angle2 % (2*math.pi))


class Ai:
    """ A simple ai that finds the shortest path to the target using 
    a breadth first search. Also capable of shooting other tanks and or wooden
    boxes. """

    def __init__(self, tank,  game_objects_list, tanks_list, space, currentmap):
        self.tank = tank
        self.game_objects_list = game_objects_list
        self.tanks_list = tanks_list
        self.space = space
        self.currentmap = currentmap
        self.flag = None
        self.MAX_X = currentmap.width - 1
        self.MAX_Y = currentmap.height - 1

        self.path = deque()
        self.move_cycle = self.move_cycle_gen()
        self.update_grid_pos()

    def update_grid_pos(self):
        """ This should only be called in the beginning, or at the end of a move_cycle. """
        self.grid_pos = self.get_tile_of_position(self.tank.body.position)

    def decide(self):
        """ Main decision function that gets called on every tick of the game. """
        next(self.move_cycle)

    def maybe_shoot(self):
        """ Makes a raycast query in front of the tank. If another tank
            or a wooden box is found, then we shoot. 
        """
        pass  # To be implemented

    def turn(self, next_coord):
        """"""

        target_angle = angle_between_vectors(
            self.tank.get_pos(), next_coord)

        current_diff = periodic_difference_of_angles(
            self.tank.get_angle(), target_angle)

        if current_diff > 0:
            self.tank.turn_left()
        else:
            self.tank.turn_right()

    def correct_angle(self, next_coord):
        target_angle = angle_between_vectors(
            self.tank.get_pos(), next_coord)

        current_diff = periodic_difference_of_angles(
            self.tank.get_angle(), target_angle)

        # Add random value to make ai's movement different.
        return abs(current_diff) <= (MIN_ANGLE_DIF + math.radians(random()))

    def correct_pos(self, next_coord):
        # Add random value to make ai's movement different.
        return self.tank.body.position.get_distance(next_coord) <= (
            MIN_POS_DIFF + random()/10)

    def move_cycle_gen(self):
        """ A generator that iteratively goes through all the required steps
            to move to our goal.
        """

        while True:
            path = self.find_shortest_path(
                self.tank.get_pos(), Vec2d(4, 4))
            path = self.shorten_path(path)
            path.popleft()

            if not path:
                yield
                continue  # Start from the top of our cycle

            next_coord = path.popleft() + Vec2d(0.5, 0.5)
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
        new_path = deque()
        new_path.append(path[0])
        for i in range(1, len(path) - 1):
            if path[i-1].x != path[i+1].x and path[i-1].y != path[i+1].y:
                new_path.append(path[i])

        new_path.append(path[-1])
        return new_path

    def find_shortest_path(self, origin, target):
        """ A simple Breadth First Search using integer coordinates as our nodes.
            Edges are calculated as we go, using an external function.
        """
        # To be implemented
        origin = self.get_tile_of_position(origin)
        shortest_path = []
        paths = [[origin]]
        queue = deque([origin])
        visited = set()

        while queue:
            node = queue.popleft()
            nodepath = []

            for path in paths:
                if path[-1] == node:
                    nodepath = path
            paths.remove(nodepath)

            if node == target:
                shortest_path = nodepath
                break

            for neighbor in self.get_tile_neighbors(node):
                if neighbor.int_tuple not in visited:
                    queue.append(neighbor)
                    visited.add(neighbor.int_tuple)
                    paths.append(nodepath + [neighbor])

        return deque(shortest_path)

    def get_target_tile(self):
        """ Returns position of the flag if we don't have it. If we do have the flag,
            return the position of our home base.
        """
        if self.tank.flag != None:
            x, y = self.tank.start_position
        else:
            self.get_flag()  # Ensure that we have initialized it.
            x, y = self.flag.x, self.flag.y
        return Vec2d(int(x), int(y))

    def get_flag(self):
        """ This has to be called to get the flag, since we don't know
            where it is when the Ai object is initialized.
        """
        if self.flag == None:
            # Find the flag in the game objects list
            for obj in self.game_objects_list:
                if isinstance(obj, gameobjects.Flag):
                    self.flag = obj
                    break
        return self.flag

    def get_tile_of_position(self, position_vector):
        """ Converts and returns the float position of our tank to an integer position. """
        x, y = position_vector
        return Vec2d(int(x), int(y))

    def get_tile_neighbors(self, coord_vec):
        """ Returns all bordering grid squares of the input coordinate.
            A bordering square is only considered accessible if it is grass
            or a wooden box.
        """
        pos_vec = self.get_tile_of_position(coord_vec)
        # Find the coordinates of the tiles' four neighbors
        neighbors = [
            pos_vec + Vec2d(0, -1),
            pos_vec + Vec2d(-1, 0),
            pos_vec + Vec2d(0, 1),
            pos_vec + Vec2d(1, 0)]

        return filter(self.filter_tile_neighbors, neighbors)

    def filter_tile_neighbors(self, coord):
        x_in_bounds = coord.x >= 0 and coord.x <= self.MAX_X
        y_in_bounds = coord.y >= 0 and coord.y <= self.MAX_Y

        if not (x_in_bounds and y_in_bounds):
            return False

        box_is_grass = self.currentmap.boxAt(coord.x, coord.y) == 0
        return box_is_grass


SimpleAi = Ai  # Legacy
