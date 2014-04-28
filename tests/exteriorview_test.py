import unittest

from lib.exterior.level5d import Level5D as ExteriorLevel
from lib.exterior.view import ExteriorView


class TestExteriorViewGenerate(unittest.TestCase):

    def setUp(self):
        level = ExteriorLevel()
        spaceship = level.add_spaceship((0, 0, 0, 0), 'USS Enterprise')
        spaceship.color = (255, 0, 0)
        self.view = ExteriorView(level)

    def test_field_size(self):
        coords, radius, sight = (0, 0, 0, 0), 13, 13
        field, colors = self.view.generate(coords, radius, sight)
        self.assertEqual(len(field), radius * 2 + 1,
                         "returned field height should reflect passed radius")
        self.assertEqual(len(field[0]), radius * 2 + 1,
                         "returned field width should reflect passed radius")

    def test_sight_influence(self):
        coords, radius, sight = (0, 0, 0, 0), 13, 7
        field, colors = self.view.generate(coords, radius, sight)
        for y, line in enumerate(field, - radius):
            for x, char in enumerate(line, - radius):
                if x > sight or x < - sight or y > sight or y < - sight:
                    self.assertEqual(char, ' ',
                                     ("characters outside the sight area "
                                      "should not be displayed"))

    def test_pointer_being_drawn(self):
        coords, radius, sight, pointer = (0, 0, 0, 0), 13, 13, (0, 0, 2, 0)
        (_, _, x, y), (_, _, dx, dy) = coords, pointer
        x, y = radius + dx - x, radius + dy - y
        field, colors = self.view.generate(coords, radius, sight, pointer)
        self.assertEqual(field[y][x], '+',
                         "pointer should be drawn at specified coordinates")
        count = 0
        for line in field:
            for char in line:
                if char == '+':
                    count += 1
        self.assertEqual(count, 1,
                         "there should be only one pointer if any")

    def test_default_color_override(self):
        coords, radius, sight = (0, 0, 0, 0), 13, 13
        field, colors = self.view.generate(coords, radius, sight)
        self.assertEqual(colors[(radius, radius)], (255, 0, 0),
                         "non-standard colored objects should pass color")
