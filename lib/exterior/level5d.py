from functools import wraps

from lib.exterior.randomlevel import RandomLevel
from lib.obj.projectile import Projectile
from lib.obj.spaceship import Spaceship


class Level5D(object):

    #--------------------------------------------------------------------------
    # decorators

    def _validate(func):

        @wraps(func)
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
        self.spaceships = []
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
        """
        >>> level = Level5D()
        >>> level.add_projectile((0, 0, 12, 13), (2, 0), 100, 800, 2)
        >>> _ = level.add_spaceship('USS Enterprise', (0, 0, 13, 13))
        >>> level.get_objects((0, 0, 12, 13))
        [<class 'Space'>, <class 'Projectile'>]
        >>> level.update()
        >>> level.get_objects((0, 0, 12, 13))
        [<class 'Space'>, <class 'Projectile'>]
        >>> level.get_objects((0, 0, 13, 13))
        [<class 'Space'>, <class 'Spaceship'> USS Enterprise]
        >>> level.update()
        >>> level.get_objects((0, 0, 13, 13))[-1].is_alive()
        False
        """
        remove = []
        for i, projectile in enumerate(self.projectiles):
            coords = projectile.get_coords()
            dx, dy = projectile.move()
            if (dx, dy) != (0, 0):
                p, q, x, y = coords
                coords = self._validate_coordinates(p, q, x + dx, y + dy)
                projectile.set_coords(coords)
                self.move_object((p, q, x, y), coords, projectile)
            spaceship = self.get_spaceship(coords)
            if spaceship:
                spaceship.receive_damage(projectile.get_damage())
                if not spaceship.is_alive():
                    spaceship.accelerate(-10)
            if not projectile.is_alive() or spaceship:
                self.remove_object(coords, projectile)
                remove.append(i)
        self.projectiles = \
            [p for i, p in enumerate(self.projectiles) if i not in remove]
        for spaceship in self.spaceships:
            coords = spaceship.get_coords()
            directions = spaceship.move()
            for (dx, dy) in directions:
                if (dx, dy) != (0, 0):
                    p, q, x, y = coords
                    coords = self._validate_coordinates(p, q, x + dx, y + dy)
                    spaceship.set_coords(coords)
                    self.move_object((p, q, x, y), coords, spaceship)

    #--------------------------------------------------------------------------
    # object operations

    @_validate
    def add_object(self, (p, q, x, y), obj):
        """
        >>> level = Level5D()
        >>> from lib.obj.projectile import Projectile
        >>> projectile = Projectile((0, 2), 7, 10, 700)
        >>> level.add_object((0, 0, 0, 0), projectile)
        >>> level.get_objects((0, 0, 0, 0))
        [<class 'Space'>, <class 'Projectile'>]
        """
        return self.levels[(p, q)].add_object((x, y), obj)

    def add_projectile(self, (p, q, x, y), pointer, dmg, spd, rng):
        """
        >>> level = Level5D()
        >>> level.add_projectile((0, 0, 1, 1), (-2, 0), 17, 700, 4)
        >>> level.get_objects((0, 0, 1, 1))
        [<class 'Space'>, <class 'Projectile'>]
        """
        # TODO: validate coordinates
        projectile = Projectile(pointer, dmg, spd, rng)
        projectile.set_coords((p, q, x, y))
        self.projectiles.append(projectile)
        self.add_object((p, q, x, y), projectile)

    def add_spaceship(self, name, coords):
        """
        >>> Level5D().add_spaceship('Enterprise', (0, 0, 0, 0))
        <class 'Spaceship'> Enterprise
        """
        spaceship = Spaceship('@', name, coords=coords, exterior=self)
        self.spaceships.append(spaceship)
        self.add_object(coords, spaceship)
        return spaceship

    def move_object(self, (p0, q0, x0, y0), (p1, q1, x1, y1), obj):
        """
        >>> level = Level5D()
        >>> from lib.obj.projectile import Projectile
        >>> projectile = Projectile((0, 2), 7, 10, 700)
        >>> level.add_object((0, 0, 0, 0), projectile)
        >>> level.move_object((0, 0, 0, 0), (0, 0, 1, 1), projectile)
        >>> level.get_objects((0, 0, 1, 1))
        [<class 'Space'>, <class 'Projectile'>]
        """
        self.remove_object((p0, q0, x0, y0), obj)
        self.add_object((p1, q1, x1, y1), obj)

    @_validate
    def remove_object(self, (p, q, x, y), obj):
        """
        >>> level = Level5D()
        >>> from lib.obj.projectile import Projectile
        >>> projectile = Projectile((0, 2), 7, 10, 700)
        >>> level.add_object((0, 0, 0, 0), projectile)
        >>> level.get_objects((0, 0, 0, 0))
        [<class 'Space'>, <class 'Projectile'>]
        >>> level.remove_object((0, 0, 0, 0), projectile)
        >>> level.get_objects((0, 0, 0, 0))
        [<class 'Space'>]
        """
        return self.levels[(p, q)].remove_object((x, y), obj)

    def teleport_player(self, player, receiver, sender):
        sender.get_interior().remove_player(player)
        receiver.get_interior().add_player(
            player, receiver.get_teleport_point())

    #--------------------------------------------------------------------------
    # bulk object accessors

    @_validate
    def get_adjacent_spaceships(self, (p, q, x0, y0)):
        """
        >>> exterior = Level5D()
        >>> _ = exterior.add_spaceship('Enterprise', (0, -1, 0, 24))
        >>> _ = exterior.add_spaceship('Galactica', (0, 0, 1, 0))
        >>> exterior.get_adjacent_spaceships((0, 0, 0, 0))
        [<class 'Spaceship'> Enterprise, <class 'Spaceship'> Galactica]
        """
        spaceships = []
        for y in xrange(y0 - 1, y0 + 2):
            for x in xrange(x0 - 1, x0 + 2):
                if x == x0 and y == y0:
                    continue
                spaceship = self.get_spaceship((p, q, x, y))
                if spaceship:
                    spaceships.append(spaceship)
        return spaceships

    @_validate
    def get_objects(self, (p, q, x, y)):
        """
        >>> Level5D().get_objects((0, 0, 0, 0))
        [<class 'Space'>]
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
                self.levels[(p, q)] = RandomLevel(25)
        return p, q, x, y

    #--------------------------------------------------------------------------
    # accessors

    def get_spaceship(self, (p, q, x, y)):
        for obj in self.get_objects((p, q, x, y))[::-1]:
            if obj.__class__.__name__ == 'Spaceship':
                return obj
        return False

    def get_spaceships(self):
        return self.spaceships
