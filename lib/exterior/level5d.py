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
        remove = []
        for i, projectile in enumerate(self.projectiles):
            coords = projectile.coords
            dx, dy = projectile.move()
            if (dx, dy) != (0, 0):
                p, q, x, y = coords
                coords = self._validate_coordinates(p, q, x + dx, y + dy)
                projectile.coords = coords
                self.move_object((p, q, x, y), coords, projectile)
            for obj in self.get_objects(coords):
                try:
                    if obj == projectile:
                        continue
                    obj.receive_damage(projectile.damage)
                    projectile.receive_damage(1)
                except AttributeError:
                    pass
            if not projectile.is_alive:
                self.remove_object(coords, projectile)
                remove.append(i)
        self.projectiles = \
            [p for i, p in enumerate(self.projectiles) if i not in remove]
        for spaceship in self.spaceships:
            coords = spaceship.coords
            directions = spaceship.move()
            for (dx, dy) in directions:
                if (dx, dy) != (0, 0):
                    p, q, x, y = coords
                    coords = self._validate_coordinates(p, q, x + dx, y + dy)
                    hostile = self.get_spaceship(coords)
                    if hostile:
                        hostile.receive_damage(100)
                        spaceship.receive_damage(100)
                    else:
                        spaceship.coords = coords
                        self.move_object((p, q, x, y), coords, spaceship)

    #--------------------------------------------------------------------------
    # object operations

    @_validate
    def add_object(self, (p, q, x, y), obj):
        return self.levels[(p, q)].add_object((x, y), obj)

    def add_projectile(self, (p, q, x, y), pointer, dmg, spd, rng):
        # TODO: validate coordinates
        projectile = Projectile(pointer, dmg, spd, rng)
        projectile.coords = (p, q, x, y)
        self.projectiles.append(projectile)
        self.add_object((p, q, x, y), projectile)

    def add_spaceship(self, coords, name):
        spaceship = Spaceship('@', name, coords=coords, exterior=self)
        self.spaceships.append(spaceship)
        self.add_object(coords, spaceship)
        return spaceship

    def move_object(self, (p0, q0, x0, y0), (p1, q1, x1, y1), obj):
        self.remove_object((p0, q0, x0, y0), obj)
        self.add_object((p1, q1, x1, y1), obj)

    @_validate
    def remove_object(self, (p, q, x, y), obj):
        return self.levels[(p, q)].remove_object((x, y), obj)

    def teleport_player(self, player, receiver, sender):
        sender.interior.remove_player(player)
        receiver.interior.add_player(
            receiver.teleport_point, player)

    #--------------------------------------------------------------------------
    # bulk object accessors

    @_validate
    def get_adjacent_spaceships(self, (p, q, x0, y0)):
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
