import unittest

from lib.exterior.level5d import Level5D as ExteriorLevel
from lib.obj.projectile import Projectile
from lib.obj.space import Space


class TestExteriorLevelUpdate(unittest.TestCase):

    def setUp(self):
        self.level = ExteriorLevel()
        self.enterprise = self.level.add_spaceship((0, 0, 0, 0),
                                                   'USS Enterprise')
        self.galactica = self.level.add_spaceship((0, 0, 0, 2),
                                                  'Battlestar Galactica')

    def test_spaceships_move_over_time(self):
        self.galactica.accelerate(500)
        self.level.update()
        self.level.update()
        self.assertEqual(self.level.get_spaceship((0, 0, 0, 1)),
                         self.galactica, "spaceship should move over time")
        self.assertEqual(self.galactica.get_coords(), (0, 0, 0, 1),
                         "spaceship coords should update after moving")

    def test_fired_projectile_moves_over_time(self):
        self.level.add_projectile((0, 0, 0, 9), (0, -2), 50, 700, 10)
        self.level.update()
        self.level.update()
        projectile = self.level.get_objects((0, 0, 0, 8))[-1]
        self.assertTrue(isinstance(projectile, Projectile),
                        "projectile should move after being fired")
        self.assertEqual(projectile.get_coords(), (0, 0, 0, 8),
                         "coords should change after moving")

    def test_missile_blows_up_after_hitting_spaceship(self):
        self.level.add_projectile((0, 0, 0, 1), (0, -2), 50, 1000, 10)
        projectile = self.level.get_objects((0, 0, 0, 1))[-1]
        self.level.update()
        self.assertNotIn(projectile, self.level.get_objects((0, 0, 0, 0)),
                         "projectile should be removed after collision")
        self.assertLess(self.enterprise.get_health(), 100,
                        "spaceship's health level should lower after a hit")

    def test_projectile_blows_up_after_collision_with_other_projectile(self):
        projectiles = []
        for y, dy in [(8, 2), (9, -2)]:
            self.level.add_projectile((0, 0, 0, y), (0, dy), 50, 1000, 10)
            projectiles.append(self.level.get_objects((0, 0, 0, y))[-1])
        self.level.update()
        for projectile in projectiles:
            self.assertFalse(projectile.is_alive(), ("both projectiles "
                             "must be destroyed"))

    def test_spaceships_render_inoperable_after_collision(self):
        self.galactica.accelerate(500)
        [self.level.update() for x in xrange(0, 4)]
        for spaceship in [self.galactica, self.enterprise]:
            self.assertFalse(spaceship.is_alive(),
                             "both spaceships should be rendered inoperable")

    def test_collided_spaceships_do_not_overlap(self):
        self.galactica.accelerate(1000)
        [self.level.update() for x in xrange(0, 4)]
        self.assertEqual(self.level.get_objects((0, 0, 0, 1))[-1],
                         self.galactica, ("collided spaceships do not move "
                         "to space occupied by other spaceships"))

    def test_projectiles_blow_up_and_are_removed_after_a_while(self):
        self.level.add_projectile((0, 0, 0, 9), (0, -2), 50, 1000, 2)
        projectile = self.level.get_objects((0, 0, 0, 9))[-1]
        self.level.update()
        self.level.update()
        self.assertFalse(projectile.is_alive(), "should not be alive")
        space = self.level.get_objects((0, 0, 0, 7))[-1]
        self.assertTrue(isinstance(space, Space), "no projectile on the map")


class TestExteriorLevelObjectOperations(unittest.TestCase):

    def setUp(self):
        self.level = ExteriorLevel()

    def test_malformed_coordinates_are_adjusted(self):
        enterprise = self.level.add_spaceship((0, 0, 24, 24), 'USS Enterprise')
        self.assertEqual(self.level.get_objects((0, 0, 24, 24))[-1],
                         enterprise, "the object should be retrievable")
        self.assertEqual(self.level.get_objects((1, 1, -1, -1))[-1],
                         enterprise, "exterior level should adjust the coords")


class TestExteriorLevelSpaceshipOperations(unittest.TestCase):

    def setUp(self):
        self.level = ExteriorLevel()
        self.galactica = self.level.add_spaceship((0, 0, 0, 1),
                                                  'Battlestar Galactica')

    def test_single_adjacent_spaceship_is_returned(self):
        enterprise = self.level.add_spaceship((0, 0, 0, 0), 'USS Enterprise')
        self.assertEqual(self.level.get_adjacent_spaceships((0, 0, 0, 1)),
                         [enterprise], ("adjacent spaceship must be "
                         "returned"))

    def test_empty_list_returned_if_no_spaceships_adjacent(self):
        self.assertEqual(self.level.get_adjacent_spaceships((0, 0, 0, 1)), [],
                         "no adjacent spaceships should be returned")
