import unittest

from lib.interior.level3d import Level3D as InteriorLevel
from lib.interior.view import InteriorView
from lib.obj.player import Player


class TestInteriorViewGenerate(unittest.TestCase):

    def setUp(self):
        tiles_map = items_map = [
            "#####",
            "#...#",
            "#####",
            "#...#",
            "#####"]
        self.obj_defs = {".": "Floor", "#": "Wall"}
        level = InteriorLevel()
        level.load_char_map(tiles_map, items_map, self.obj_defs)
        mike = Player('Mike')
        mike.set_color((255, 0, 0))
        level.add_player((2, 1), mike)
        self.view = InteriorView(level)

    def test_field_size(self):
        coords, radius, sight = (2, 1), 13, 13
        field, colors = self.view.generate(coords, radius, sight)
        self.assertEqual(len(field), radius * 2 + 1,
                         "returned field height should reflect passed radius")
        self.assertEqual(len(field[0]), radius * 2 + 1,
                         "returned field width should reflect passed radius")

    def test_room_visibility(self):
        coords, radius, sight = (2, 1), 13, 13
        field, colors = self.view.generate(coords, radius, sight)
        for y in xrange(radius - 1, radius + 2):
            for x in xrange(radius - 2, radius + 3):
                self.assertIn(field[y][x], self.obj_defs.keys() + ['@'],
                                    "non-obscured room should be visible")

    def test_sight_influence(self):
        coords, radius, sight = (2, 1), 13, 7
        field, colors = self.view.generate(coords, radius, sight)
        for y, line in enumerate(field, - radius):
            for x, char in enumerate(line, - radius):
                if x > sight or x < - sight or y > sight or y < - sight:
                    self.assertEqual(char, ' ',
                                     ("characters outside the sight area "
                                      "should not be displayed"))

    def test_shadowcasting_and_obscurity(self):
        coords, radius, sight = (2, 1), 13, 13
        field, colors = self.view.generate(coords, radius, sight)
        for y in xrange(3, 5):
            for x in xrange(0, 5):
                self.assertEqual(field[y][x], ' ',
                                 "room behind the wall should not be visible")

    def test_target_being_drawn(self):
        coords, radius, sight, target = (2, 1), 13, 7, (2, 3)
        (x, y), (dx, dy) = coords, target
        x, y = radius + dx - x, radius + dy - y
        field, colors = self.view.generate(coords, radius, sight, target)
        self.assertEqual(field[y][x], 'x',
                         "target should be drawn at specified coordinates")
        count = 0
        for line in field:
            for char in line:
                if char == 'x':
                    count += 1
        self.assertEqual(count, 1,
                         "there should be only one target if any")

    def test_default_color_override(self):
        coords, radius, sight = (2, 1), 13, 13
        field, colors = self.view.generate(coords, radius, sight)
        self.assertEqual(colors[(radius, radius)], (255, 0, 0),
                         "non-standard colored objects should pass color")
