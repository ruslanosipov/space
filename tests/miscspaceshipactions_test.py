import unittest

from lib.misc import add_spaceship, exterior_fire
from lib.exterior.level5d import Level5D as ExteriorLevel
from lib.obj.spaceship import Spaceship
from lib.obj.projectile import Projectile


class TestSpaceshipAdd(unittest.TestCase):

    def test_spaceship_can_be_added(self):
        level = ExteriorLevel()
        spaceship = add_spaceship('TestSpaceship',
                                  (0, 0, 0, 0), (0, 0), level)
        self.assertTrue(isinstance(spaceship, Spaceship),
                        "spaceship should be an instance of a Spaceship")
        self.assertEqual(level.get_objects((0, 0, 0, 0))[-1], spaceship,
                         "spaceship should be added to an external level")


class TestSpaceshipFire(unittest.TestCase):

    def test_spaceship_can_fire_missile(self):
        level = ExteriorLevel()
        spaceship = add_spaceship('TestSpaceship',
                                  (0, 0, 0, 0), (0, 0), level)
        exterior_fire(spaceship.get_coords(), spaceship.get_pointer(), level)
        level.update()
        obj = level.get_objects((0, 0, 0, -1))[-1]
        self.assertTrue(isinstance(obj, Projectile),
                        "projectile should spawn where the pointer points")
