from lib.utl import bresenham
from lib.interior.level3d import Level3D


class Spaceship(object):

    #--------------------------------------------------------------------------
    # setup

    def __init__(self, char, name, coords, exterior=None):
        """
        >>> Spaceship('@', 'Galactica', (0, 0, 0, 0))
        <class 'Spaceship'> Galactica
        """
        self.char = char
        self.name = name
        self.coords = coords
        self.exterior = exterior
        self.pointers = [(0, -2), (1, -2), (2, -1), (2, 0), (2, 1), (1, 2),
                        (0, 2), (-1, 2), (-2, 1), (-2, 0), (-2, -1), (-1, -2)]
        self.pointer = 0
        self.speed = 0
        self.speed_max = 500
        self.inertia = {}
        self.health = self.health_max = 100
        self.alive = True
        self.interior = None
        self.players = []
        self.spawn_point = (0, 0)
        self.teleport_point = None
        self.control = 5

    def __repr__(self):
        return "<class '%s'> %s" % (self.__class__.__name__, self.name)

    def load_interior(self, level, obj_data):
        self.interior = Level3D(level, obj_data, spaceship=self)

    #--------------------------------------------------------------------------
    # movement

    def accelerate(self, acceleration):
        """
        >>> spaceship = Spaceship('@', 'Galactica', (0, 0, 0, 0))
        >>> spaceship.accelerate(1000)
        >>> spaceship.move()
        [(0, -1)]
        """
        self.speed += acceleration
        if self.speed < 0:
            self.speed = 0
        elif self.speed > self.speed_max:
            self.speed = self.speed_max

    def move(self):
        """
        Returns relative movement.

        >>> spaceship = Spaceship('@', 'Galactica', (0, 0, 0, 0))
        >>> spaceship.accelerate(700)
        >>> spaceship.move()
        []
        >>> spaceship.move()
        [(0, -1)]
        """
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
                x, y = path[1]
                directions.append((x, y))
            self.inertia[pointer][2] = movement
        return directions

    def rotate_pointer(self, reverse=False):
        """
        Pointer is an equivalent of a steering wheel. Reverse is
        counter-clockwise.

        >>> spaceship = Spaceship('@', 'Galactica', (0, 0, 0, 0))
        >>> spaceship.get_pointer()
        (0, -2)
        >>> spaceship.rotate_pointer()
        >>> spaceship.get_pointer()
        (1, -2)
        >>> for _ in xrange(0, 2):
        ...     spaceship.rotate_pointer(True)
        >>> spaceship.get_pointer()
        (-1, -2)
        >>> spaceship.rotate_pointer()
        >>> spaceship.get_pointer()
        (0, -2)
        """
        i = 1 if not reverse else -1
        if self.pointer == len(self.pointers) - 1 and not reverse:
            self.pointer = 0
        elif self.pointer == 0 and reverse:
            self.pointer = len(self.pointers) - 1
        else:
            self.pointer += i

    #--------------------------------------------------------------------------
    # combat

    def receive_damage(self, damage):
        """
        >>> spaceship = Spaceship('@', 'Galactica', (0, 0, 0, 0))
        >>> spaceship.receive_damage(10)
        >>> spaceship.is_alive()
        True
        >>> spaceship.receive_damage(200)
        >>> spaceship.is_alive()
        False
        """
        self.health -= damage
        if self.health <= 0:
            self.alive = False

    #--------------------------------------------------------------------------
    # accessors

    def get_abs_pointer(self):
        dx, dy = self.pointers[self.pointer]
        q, p, x, y = self.coords
        return (q, p, x + dx, y + dy)

    def is_alive(self):
        return self.alive

    def get_char(self):
        return self.char

    def get_coords(self):
        return self.coords

    def get_exterior(self):
        return self.exterior

    def get_interior(self):
        return self.interior

    def get_name(self):
        return self.name

    def get_spawn_point(self):
        return self.spawn_point

    def get_speed(self):
        return self.speed

    def get_teleport_point(self):
        return self.teleport_point

    def get_pointer(self):
        return self.pointers[self.pointer]

    def get_view(self):
        return self.view

    def set_coords(self, (p, q, x, y)):
        self.coords = (p, q, x, y)

    def set_spawn_point(self, (x, y)):
        self.spawn_point = (x, y)

    def set_teleport_point(self, (x, y)):
        self.teleport_point = (x, y)

    def set_view(self, view):
        self.view = view
