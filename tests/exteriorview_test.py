import unittest

from lib.exterior.level5d import Level5D as ExteriorLevel
from lib.exterior import view as exterior_view


class TestExteriorViewgenerate_exterior_view(unittest.TestCase):

    def setUp(self):
        self.level = ExteriorLevel()
        spaceship = self.level.add_spaceship((0, 0, 0, 0), 'USS Enterprise')
        spaceship.color = (255, 0, 0)

    def test_field_size(self):
        coords, radius, sight = (0, 0, 0, 0), 13, 13
        field, colors = exterior_view.generate_exterior_view(
                self.level, coords, radius, sight)
        self.assertEqual(len(field), radius * 2 + 1)
        self.assertEqual(len(field[0]), radius * 2 + 1)

    def test_sight_influence(self):
        coords, radius, sight = (0, 0, 0, 0), 13, 7
        field, colors = exterior_view.generate_exterior_view(
                self.level, coords, radius, sight)
        for y, line in enumerate(field, - radius):
            for x, char in enumerate(line, - radius):
                if x > sight or x < - sight or y > sight or y < - sight:
                    self.assertEqual(char, ' ')

    def test_pointer_being_drawn(self):
        coords, radius, sight, pointer = (0, 0, 0, 0), 13, 13, (0, 0, 2, 0)
        (_, _, x, y), (_, _, dx, dy) = coords, pointer
        x, y = radius + dx - x, radius + dy - y
        field, colors = exterior_view.generate_exterior_view(
                self.level, coords, radius, sight, pointer)
        self.assertEqual(field[y][x], '+')
        count = 0
        for line in field:
            for char in line:
                if char == '+':
                    count += 1
        self.assertEqual(count, 1)

    def test_default_color_override(self):
        coords, radius, sight = (0, 0, 0, 0), 13, 13
        field, colors = exterior_view.generate_exterior_view(
                self.level, coords, radius, sight)
        self.assertEqual(colors[(radius, radius)], (255, 0, 0))
