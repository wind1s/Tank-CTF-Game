import pymunk as pym
import random as rand
import math
from utility import (
    get_tile_position, angle_between_vectors, periodic_difference_of_angles,
    seconds_to_ms, reduce_until_zero)
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
    MAX_STUCK_TIME = seconds_to_ms(1.5)

    def __init__(self, tank, game_objects, space, current_map, clock):
        self.space = space
        self.clock = clock

        # Buff tanks.
        tank.max_speed = tank.max_speed*1.3
        tank.bullet_max_speed = tank.bullet_max_speed*1.2
        self.tank = tank

        self.flag = None
        self.game_objects = game_objects

        self.current_map = current_map
        self.updated_boxes = current_map.boxes

        self.MAX_X = current_map.width - 1
        self.MAX_Y = current_map.height - 1

        self.stuck_timeout = self.MAX_STUCK_TIME

        self.path = deque()
        self.move_cycle = self.move_cycle_gen()

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
                    in (Box.WOODBOX_TYPE, )):
                self.tank.shoot(self.game_objects)

    def turn(self, next_coord):
        """ Turns the tank toward a coordinate. """

        target_angle = angle_between_vectors(
            self.tank.get_pos(), next_coord)

        current_diff = periodic_difference_of_angles(
            self.tank.get_angle(), target_angle)

        current_diff -= 2*math.pi if current_diff > math.pi else 0

        if current_diff > 0:
            self.tank.turn_left()
        else:
            self.tank.turn_right()

    def correct_angle(self, next_coord):
        """ Checks if tank is standing close to the same angle as the coord. """
        def angle_diff():
            """ Adds a random value to position diff to make ai more human. """
            return self.MIN_ANGLE_DIF + math.radians(rand.random())

        target_angle = angle_between_vectors(
            self.tank.get_pos(), next_coord)

        current_diff = periodic_difference_of_angles(
            self.tank.get_angle(), target_angle)

        # Add random value to make ai's movement different.
        return abs(current_diff) <= angle_diff()

    def correct_pos(self, next_coord):
        """ Checks if the tank is standing close enought to the coord. """
        def pos_diff():
            """ Adds a random value to position diff to make ai more human. """
            return self.MIN_POS_DIFF + rand.random()/10

        return self.tank.get_pos().get_distance(next_coord) <= pos_diff()

    def move_cycle_gen(self):
        """ A generator that iteratively goes through all the required steps
            to move to our goal.
        """

        while True:
            self.update_box_pos()

            path = self.get_path()

            if not path:
                yield
                continue  # Start from the top of our cycle
            
            path = self.shorten_path(path)
            path.popleft()

            next_coord = path.popleft()
            yield

            self.turn(next_coord)

            while not self.correct_angle(next_coord):
                yield

            self.tank.stop_turning()
            yield

            self.tank.accelerate()

            while not self.correct_pos(next_coord):
                self.stuck_timeout = reduce_until_zero(
                    self.stuck_timeout, self.clock.get_time())
                if self.stuck_timeout <= 0:
                    self.stuck_timeout = self.MAX_STUCK_TIME
                    break
                yield

            self.tank.stop_moving()


    def shorten_path(self, path):
        """ Shortens the path generated from an A* search."""
        new_path = deque()

        def path_tile_is_turn(i):
            return path[i-1].x != path[i+1].x and path[i-1].y != path[i+1].y

        new_path.append(path[0])
        new_path.extend([path[i] for i in range(
            1, len(path) - 1) if path_tile_is_turn(i)])
        new_path.append(path[-1])

        return new_path

    class Node():
        def __init__(self, tile, hcost, gcost, previous = None):
            self.tile = tile
            self.hcost = hcost
            self.gcost = gcost
            self.fcost = hcost + gcost
            self.previous = previous

    def create_node(self, tile, origin, target, previous = None):
        gcost = (target - tile).length
        hcost = (origin - tile).length
        return self.Node(tile, hcost, gcost, previous)

    def tile_not_visited(self, tile, open, closed):
        nodes = open + closed
        for node in nodes:
            if node.tile == tile:
                return False
        return True

    def find_prio_path(self, origin, target):
        path = self.find_shortest_path(origin, target, False)
        if not path:
            path = self.find_shortest_path(origin, target, True)
        return path

    def find_shortest_path(self, origin, target, include_metal):
        target_tile = get_tile_position(target)
        origin = get_tile_position(origin)
        open = [self.create_node(origin, origin, target)]
        closed = []

        while open:
            current = open[0]
            for node in open:
                if (node.fcost < current.fcost or 
                   (node.fcost == current.fcost and
                    node.hcost < current.hcost)):
                    current = node
            open.remove(current)
            closed.append(current)

            if current.tile == target_tile:
                out = deque()
                current.tile = target - pym.Vec2d(0.5, 0.5)
                while True:
                    if current == None:
                        break
                    out.appendleft(current.tile + pym.Vec2d(0.5, 0.5))
                    current = current.previous
                return out
                
            for neighbor in self.get_tile_neighbors(current.tile, include_metal):
                if self.tile_not_visited(neighbor, open, closed):
                    open.append(self.create_node(neighbor, origin, target, current))
        return deque([])


    def update_box_pos(self):
        self.updated_boxes = [[0 for _ in range(self.current_map.width)]
                              for k in range(self.current_map.height)]

        for obj in self.game_objects:
            if isinstance(obj, Box):
                tile_x, tile_y = get_tile_position(obj.get_pos())
                self.updated_boxes[tile_y][tile_x] = obj.box_type

    def find_intercept_path(self):
        self.get_flag()
        flag_path = self.find_prio_path(self.flag.get_pos(),
                                        self.flag.target_base)
        for coord in flag_path:
            if get_tile_position(self.tank.get_pos()) == get_tile_position(coord):
                return self.find_prio_path(self.tank.get_pos(), self.flag.get_pos())
        intercept_point = flag_path[len(flag_path) // 2]
        return self.find_prio_path(self.tank.get_pos(), intercept_point)

    def get_path(self):
        """ Finds target path. Goes to flag if on ground, intecepts tank 
        with flag if picked up. Goes to base if we have flag.
        """
        self.get_flag()
        if self.tank.flag is None:
            if self.flag.is_on_tank:
                return self.find_intercept_path()
            return self.find_prio_path(self.tank.get_pos(), self.flag.get_pos())

        return self.find_prio_path(self.tank.get_pos(),
                                   self.tank.start_position)

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

    def get_tile_neighbors(self, coord_vec, include_metal):
        """ Returns all bordering grid squares of the input coordinate.
            A bordering square is only considered accessible if it is grass
            or a wooden box.
        """
        pos_vec = get_tile_position(coord_vec)
        # Find the coordinates of the tiles' four neighbors
        neighbors = [
            pos_vec + pym.Vec2d(0, -1),
            pos_vec + pym.Vec2d(-1, 0),
            pos_vec + pym.Vec2d(0, 1),
            pos_vec + pym.Vec2d(1, 0)
        ]

        out = []
        for coord in neighbors:
            if self.filter_tile_neighbors(coord, include_metal):
                out.append(coord)
        return out

    def filter_tile_neighbors(self, coord, include_metal_box):
        x_in_bounds = coord.x >= 0 and coord.x <= self.MAX_X
        y_in_bounds = coord.y >= 0 and coord.y <= self.MAX_Y

        if not (x_in_bounds and y_in_bounds):
            return False

        box_type = self.updated_boxes[coord.y][coord.x]
        box_is_wood = box_type == Box.WOODBOX_TYPE
        box_is_grass = box_type == Box.GRASS_TYPE
        box_is_metal = box_type == Box.METALBOX_TYPE

        return box_is_grass or box_is_wood or (
            include_metal_box and box_is_metal)
