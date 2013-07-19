from lib.exterior.randomlevel import RandomLevel
from lib.utl import bresenham
from lib.obj.projectile import Projectile


class Level5D(object):
    """
    >>> level = Level5D()
    >>> from lib.obj.projectile import Projectile
    >>> projectile = Projectile((0, 2), 7, 10, 0.7)
    >>> level.add_object((0, 0, 0, 0), projectile)
    >>> level.get_objects((0, 0, 0, 0))
    [<class 'Space'>, <class 'Projectile'>]
    >>> level.remove_object((0, 0, 0, 0), projectile)
    >>> level.get_objects((0, 0, 0, 0))
    [<class 'Space'>]
    """

    #--------------------------------------------------------------------------
    # decorators

    def _validate(func):

        def wrapper(self, (p, q, x, y), char=None):
            p, q, x, y = self._validate_coordinates(p, q, x, y)
            if char is not None:
                return func(self, (p, q, x, y), char)
            return func(self, (p, q, x, y))

        return wrapper

    #--------------------------------------------------------------------------
    # setup

    def __init__(self):
        """
        >>> Level5D()
        <class 'Level5D'>
        """
        self.levels = {}
        self.projectiles = []
        self._populate_area((0, 0))

    def __repr__(self):
        return "<class '%s'>" % self.__class__.__name__

    def _populate_area(self, (x0, y0)):
        for y in xrange(y0 - 1, y0 + 2):
            for x in xrange(x0 - 1, x0 + 2):
                if (x, y) not in self.levels.keys():
                    self.levels[(x, y)] = RandomLevel(25)

    #--------------------------------------------------------------------------
    # update

    def update(self):
        for i, p in enumerate(self.projectiles):
            coords = p.get_coordinates()
            if p.move():
                self.remove_object(coords, '*')
                self.add_object(p.get_coordinates(), '*')
            if not p.is_alive():
                self.remove_object(coords, '*')
        self.projectiles = [p for p in self.projectiles if p.is_alive()]

    #--------------------------------------------------------------------------
    # object operations

    @_validate
    def add_object(self, (p, q, x, y), obj):
        """
        See class definition for tests (decorated functions and doctest issue).
        """
        return self.levels[(p, q)].add_object((x, y), obj)

    def add_projectile(self, (p, q, x, y), pointer, dmg, spd, rng):
        """
        >>> level = Level5D()
        >>> level.add_projectile((0, 0, 1, 1), (-2, 0), 17, 0.7, 4)
        """
        # TODO: validate coordinates
        self.projectiles.append(Projectile(pointer, dmg, spd, rng))
        self.add_object((p, q, x, y), self.projectiles[-1])

    @_validate
    def remove_object(self, (p, q, x, y), obj):
        """
        See class definition for tests (decorated functions and doctest issue).
        """
        return self.levels[(p, q)].remove_object((x, y), obj)

    #--------------------------------------------------------------------------
    # bulk object accessors

    @_validate
    def get_objects(self, (p, q, x, y)):
        """
        See class definition for tests (decorated functions and doctest issue).
        """
        return self.levels[(p, q)].get_objects((x, y))

    #--------------------------------------------------------------------------
    # validators

    def _validate_coordinates(self, p, q, x, y):
        while True:
            if (p, q) in self.levels.keys():
                if x < 0:
                    x += self.levels[(p, q)].get_width(0)
                    p -= 1
                elif y < 0:
                    y += self.levels[(p, q)].get_height()
                    q -= 1
                elif x >= self.levels[(p, q)].get_width(0):
                    x -= self.levels[(p, q)].get_width(0)
                    p += 1
                elif y >= self.levels[(p, q)].get_height():
                    y -= self.levels[(p, q)].get_height()
                    q += 1
                else:
                    break
            else:
                self.levels[(p, q)] = ShipLevel(25)
        return p, q, x, y
