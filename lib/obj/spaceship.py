"""Spaceship object."""

from lib.interior.level3d import Level3D
from lib.obj.baseobject import BaseObject
from lib.utl import bresenham


class Spaceship(BaseObject):
    """Spaceship object."""

    control = 5
    health_max = 100
    speed_max = 500

    #--------------------------------------------------------------------------
    # Setup.

    def __init__(self, char, name, coords, exterior=None):
        self._color = None
        self.char = char
        self.coords = coords
        self.exterior = exterior
        self.health = self.health_max
        self.inertia = {}
        self.interior = None
        self.is_alive = True
        self.is_default_color = True
        self.name = name
        self.pilot = None
        self.players = []
        self.pointer = 0
        self.pointers = [(0, -2), (1, -2), (2, -1), (2, 0), (2, 1), (1, 2),
                         (0, 2), (-1, 2), (-2, 1), (-2, 0), (-2, -1), (-1, -2)]
        self.spawn_point = (0, 0)
        self.speed = 0
        self.teleport_point = None

    def __repr__(self):
        return "<class '%s'> %s" % (self.__class__.__name__, self.name)

    def load_interior(self, level, obj_data, extras=None):
        """Load ship interior."""
        if extras is None:
            extras = {}
        self.interior = Level3D()
        self.interior.spaceship = self
        self.interior.load_converted_char_map(level, obj_data, extras)

    #--------------------------------------------------------------------------
    # Movement.

    def accelerate(self, acceleration):
        """Accelerate the spaceship."""
        self.speed += acceleration
        if self.speed < 0:
            self.speed = 0
        elif self.speed > self.speed_max:
            self.speed = self.speed_max

    def move(self):
        """Move one tick."""
        directions = []
        if self.pointer not in self.inertia.keys():
            self.inertia[self.pointer] = [self.speed, self.speed, 0]
        for pointer, (speed, inertia, movement) in self.inertia.items():
            speed = self.speed if pointer == self.pointer else 0
            self.inertia[pointer][0] = speed
            if inertia > speed:
                inertia -= self.control
            elif inertia < speed:
                inertia += self.control
            self.inertia[pointer][1] = inertia
            movement += inertia
            if movement >= 1000:
                movement -= 1000
                path = bresenham.get_line((0, 0), self.pointers[pointer])
                directions.append(path[1])
            self.inertia[pointer][2] = movement
        return directions

    def rotate_pointer(self, reverse=False):
        """Rotate direction in which the ship is pointing."""
        i = 1 if not reverse else -1
        if self.pointer == len(self.pointers) - 1 and not reverse:
            self.pointer = 0
        elif self.pointer == 0 and reverse:
            self.pointer = len(self.pointers) - 1
        else:
            self.pointer += i

    #--------------------------------------------------------------------------
    # Combat.

    def receive_damage(self, damage):
        """Receive damage and (possibly) die."""
        self.health -= damage
        if self.health <= 0:
            if self.pilot:
                self.pilot.toggle_pilot()
            self.is_alive = False
            self.color = (50, 50, 50)
            self.speed = 0

    #--------------------------------------------------------------------------
    # Accessors.

    def get_abs_pointer(self):
        """Get absolute pointer value."""
        dx, dy = self.pointers[self.pointer]
        q, p, x, y = self.coords
        return (q, p, x + dx, y + dy)

    def get_pointer(self):
        """Get relative pointer value."""
        return self.pointers[self.pointer]
