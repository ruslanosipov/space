class Projectile:

    def __init__(self, (p, q), path, damage, speed):
        """
        path -- list of coordinates (x, y)
        """
        self.p, self.q = p, q
        self.path = path
        self.damage = damage
        self.speed = speed
        self.pos = 0
        self.movement = 0.0
        self.alive = True

    def move(self):
        """
        Move projectile by self.speed. Return True if object changes
        coordinates, False otherwise.

        >>> (p, q), (x0, y0), (x1, y1)  = (0, 0), (0, 0), (1, 1)
        >>> projectile = Projectile((p, q), [(x0, y0), (x1, y1)], 10, 0.8)
        >>> projectile.move()
        False
        >>> projectile.get_coordinates() == (p, q, x0, y0)
        True
        >>> projectile.move()
        True
        >>> projectile.get_coordinates() == (p, q, x1, y1)
        True
        >>> projectile.move()
        True
        >>> projectile.is_alive()
        False
        """
        self.movement += self.speed
        if self.movement >= 1.0:
            self.movement -= 1.0
            if self.pos == len(self.path) - 1:
                self.alive = False
                return True
            self.pos += 1
            return True
        return False

    #--------------------------------------------------------------------------
    # accessors

    def is_alive(self):
        return self.alive

    def get_coordinates(self):
        x, y = self.path[self.pos]
        return (self.p, self.q, x, y)

    def get_damage(self):
        return self.damage
