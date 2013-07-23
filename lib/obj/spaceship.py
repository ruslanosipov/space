from lib.utl import bresenham


class Spaceship(object):

    def __init__(self, char, name):
        """
        >>> Spaceship('@', 'Enterprise')
        <class 'Spaceship'> Enterprise
        """
        self.char = char
        self.name = name
        self.movement = 0.0
        self.pointers = [(0, -2), (1, -2), (2, -1), (2, 0), (2, 1), (1, 2),
                        (0, 2), (-1, 2), (-2, 1), (-2, 0), (-2, -1), (-1, -2)]
        self.pointer = 0
        self.speed = 0.0
        self.speed_max = 1.0
        self.health = self.health_max = 100
        self.alive = True
        self.coords = (0, 0, 0, 0)
        self.interior = None
        self.players = []

    def __repr__(self):
        return "<class '%s'> %s" % (self.__class__.__name__, self.name)

    def accelerate(self, acceleration):
        """
        >>> spaceship = Spaceship('@', 'Enterprise')
        >>> spaceship.accelerate(1.0)
        >>> spaceship.move()
        (0, -1)
        """
        self.speed += acceleration
        if self.speed < 0:
            self.speed = 0
        elif self.speed > self.speed_max:
            self.speed = self.speed_max

    def move(self):
        """
        Returns relative movement.

        >>> spaceship = Spaceship('@', 'Enterprise')
        >>> spaceship.accelerate(0.7)
        >>> spaceship.move()
        (0, 0)
        >>> spaceship.move()
        (0, -1)
        """
        self.movement += self.speed
        if self.movement >= 1.0:
            self.movement -= 1.0
            x, y = bresenham.get_line((0, 0), self.pointers[self.pointer])[1]
            return (x, y)
        return (0, 0)

    def receive_damage(self, damage):
        """
        >>> spaceship = Spaceship('@', 'Enterprise')
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

    def rotate_pointer(self, reverse=False):
        """
        Pointer is an equivalent of a steering wheel. Reverse is
        counter-clockwise.

        >>> spaceship = Spaceship('@', 'Enterprise')
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
    # players operations

    def add_player(self, player, (x, y)):
        self.players.append(player)
        self.interior.add_object((x, y), player)
        player.set_coords((x, y))
        player.set_spaceship(self)

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

    def get_interior(self):
        return self.interior

    def get_name(self):
        return self.name

    def get_players(self):
        return self.players

    def get_pointer(self):
        return self.pointers[self.pointer]

    def get_view(self):
        return self.view

    def set_coords(self, (p, q, x, y)):
        self.coords = (p, q, x, y)

    def set_interior(self, interior):
        self.interior = interior

    def set_view(self, view):
        self.view = view
