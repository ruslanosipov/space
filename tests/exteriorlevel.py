import unittest

from lib.exterior.level5d import Level5D as ExteriorLevel


class TestExteriorLevelUpdate(unittest.TestCase):

    def setUp(self):
        pass

    def test_spaceships_move_over_time(self):
        pass

    def test_fired_projectile_moves_over_time(self):
        pass

    def test_missile_blows_up_after_hitting_spaceship(self):
        pass

    def test_spaceships_render_inoperable_after_collision(self):
        pass

    def test_projectiles_blow_up_after_a_while(self):
        pass

    def test_blown_up_projectiles_are_removed(self):
        pass

    def test_crashed_spaceships_decelerate(self):
        pass


class TestExteriorLevelObjectOperations(unittest.TestCase):

    def setUp(self):
        pass

    def test_malformed_coordinates_are_adjusted(self):
        pass

    def test_exising_object_can_be_retrieved(self):
        pass

    def test_object_can_be_added(self):
        pass

    def test_object_can_be_moved(self):
        pass

    def test_object_can_be_removed(self):
        pass

    def test_projectile_can_be_added(self):
        pass


class TestExteriorLevelSpaceshipOperations(unittest.TestCase):

    def setUp(self):
        pass

    def test_spaceship_can_be_added(self):
        pass

    def test_adjacent_spaceships_are_returned(self):
        pass

    def test_empty_list_returned_if_no_spaceships_adjacent(self):
        pass
