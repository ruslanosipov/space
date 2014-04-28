"""Spaceships shoot using these missiles."""

from lib.obj.baseobject import BaseObject
from lib.utl import bresenham


class Projectile(BaseObject):
    """Spaceships shoot using these missiles."""

    def __init__(self, direction, damage, speed, lifespan):
        self._color = None
        self.char = '*'
        self.coords = (0, 0, 0, 0)
        self.damage = damage
        self.directions = bresenham.get_line((0, 0), direction)[1:]
        self.health = 1
        self.is_alive = True
        self.is_default_color = True
        self.lifespan = lifespan
        self.lifestep = 0
        self.movement = 0
        self.position = 0
        self.speed = speed

    def __repr__(self):
        return "<class '%s'>" % self.__class__.__name__

    def move(self):
        """Move one step."""
        self.movement += self.speed
        if self.movement >= 1000:
            self.lifestep += 1
            self.movement -= 1000
            if self.lifestep >= self.lifespan:
                self.is_alive = False
            return self.directions[self.position]
        return (0, 0)

    def receive_damage(self, damage):
        """Receive damage."""
        self.health -= damage
        if self.health <= 0:
            self.is_alive = False
