from lib.utl import bresenham


class Spaceship(object):

    def __init__(self, (map_x, map_y, x, y)):
        self.map_x, self.map_y, self.x, self.y = map_x, map_y, x, y
        self.movement_fraction = 0
        self.targets = [
            (0, -2),
            (1, -2),
            (2, -1),
            (2, 0),
            (2, 1),
            (1, 2),
            (0, 2),
            (-1, 2),
            (-2, 1),
            (-2, 0),
            (-2, -1),
            (-1, -2)]
        self.target = self.targets[0]
        self.target_index = 0
        self.acceleration = 0
        self.acceleration_limit = 1
        self.health = self.max_health = 100
        self.alive = True

    def accelerate(self, acceleration):
        self.acceleration += acceleration * 0.1
        if self.acceleration < 0:
            self.acceleration = 0
        elif self.acceleration > self.acceleration_limit:
            self.acceleration = self.acceleration_limit

    def rotate_target(self, reverse=False):
        i = 1 if not reverse else -1
        if self.target_index == len(self.targets) - 1 and not reverse:
            self.target_index = 0
        elif self.target_index == 0 and reverse:
            self.target_index = len(self.targets) - 1
        else:
            self.target_index += i
        self.target = self.targets[self.target_index]

    def update(self):
        self.movement_fraction += self.acceleration
        if self.movement_fraction >= 1:
            self.movement_fraction -= 1
            (dx, dy), (x, y) = self.target, (self.x, self.y)
            x, y = bresenham.get_line((x, y), (x + dx, y + dy))[1]
            self.x, self.y = x, y

    def take_damage(self, damage):
        """
        >>> s = Spaceship((0, 0, 0, 0))
        >>> s.take_damage(10)
        >>> s.is_alive()
        True
        >>> s.take_damage(100)
        >>> s.is_alive()
        False
        """
        self.health -= damage
        if self.health <= 0:
            self.alive = False

    def is_alive(self):
        return self.alive

    def get_coordinates(self):
        return (self.map_x, self.map_y, self.x, self.y)

    def get_target(self):
        dx, dy = self.target
        return (self.map_x, self.map_y, self.x + dx, self.y + dy)
