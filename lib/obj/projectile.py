from lib.utl import bresenham


class Projectile:

    def __init__(self, direction, damage, speed, lifespan):
        """
        >>> Projectile((-2, 0), 8, 10, 0.8)
        <class 'Projectile'>
        """
        self.char = '*'
        self.directions = bresenham.get_line((0, 0), direction)[1:]
        self.position = 0
        self.lifestep = 0
        self.lifespan = lifespan
        self.damage = damage
        self.speed = speed
        self.movement = 0.0
        self.alive = True
        self.coords = (0, 0, 0, 0)

    def __repr__(self):
        return "<class '%s'>" % self.__class__.__name__

    def move(self):
        """
        Move projectile by self.speed. Return True if object changes
        coordinates, False otherwise.

        >>> projectile = Projectile((1, 1), 10, 0.8, 2)
        >>> projectile.move()
        (0, 0)
        >>> projectile.move()
        (1, 1)
        >>> projectile.move()
        (1, 1)
        >>> projectile.is_alive()
        False
        """
        self.movement += self.speed
        if self.movement >= 1.0:
            self.lifestep += 1
            self.movement -= 1.0
            if self.lifestep >= self.lifespan:
                self.alive = False
            self._increment_position
            return self.directions[self.position]
        return (0, 0)

    def _increment_position(self):
        if self.position >= len(self.directions) - 1:
            self.position = 0
        else:
            self.position += 1

    #--------------------------------------------------------------------------
    # accessors

    def is_alive(self):
        return self.alive

    def get_char(self):
        return self.char

    def get_coords(self):
        return self.coords

    def get_damage(self):
        return self.damage

    def set_coords(self, (p, q, x, y)):
        self.coords = (p, q, x, y)
