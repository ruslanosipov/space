import unittest

from lib.interior.level3d import Level3D as InteriorLevel
from lib.interior import view as interior_view
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
        self.level = InteriorLevel()
        self.level.load_char_map(tiles_map, items_map, self.obj_defs)
        mike = Player('Mike')
        mike.color = (255, 0, 0)
        self.level.add_player((2, 1), mike)

    def test_field_size(self):
        coords, radius, sight = (2, 1), 13, 13
        visible_tiles = interior_view.find_visible_tiles(
                self.level, coords, radius, sight)
        field, colors, _, _ = interior_view.generate_interior_view(
                self.level, coords, radius, sight, visible_tiles)
        self.assertEqual(len(field), radius * 2 + 1)
        self.assertEqual(len(field[0]), radius * 2 + 1)

    def test_room_visibility(self):
        coords, radius, sight = (2, 1), 13, 13
        visible_tiles = interior_view.find_visible_tiles(
                self.level, coords, radius, sight)
        field, colors, _, _ = interior_view.generate_interior_view(
                self.level, coords, radius, sight, visible_tiles)
        for y in xrange(radius - 1, radius + 2):
            for x in xrange(radius - 2, radius + 3):
                self.assertIn(field[y][x], self.obj_defs.keys() + ['@'])

    def test_sight_influence(self):
        coords, radius, sight = (2, 1), 13, 7
        visible_tiles = interior_view.find_visible_tiles(
                self.level, coords, radius, sight)
        field, colors, _, _ = interior_view.generate_interior_view(
                self.level, coords, radius, sight, visible_tiles)
        for y, line in enumerate(field, - radius):
            for x, char in enumerate(line, - radius):
                if x > sight or x < - sight or y > sight or y < - sight:
                    self.assertEqual(char, ' ')

    def test_shadowcasting_and_obscurity(self):
        coords, radius, sight = (2, 1), 13, 13
        visible_tiles = interior_view.find_visible_tiles(
                self.level, coords, radius, sight)
        field, colors, _, _ = interior_view.generate_interior_view(
                self.level, coords, radius, sight, visible_tiles)
        for y in xrange(3, 5):
            for x in xrange(0, 5):
                self.assertEqual(field[y][x], ' ')

    def test_target_being_drawn(self):
        coords, radius, sight, target = (2, 1), 13, 7, (2, 3)
        (x, y), (dx, dy) = coords, target
        x, y = radius + dx - x, radius + dy - y
        visible_tiles = interior_view.find_visible_tiles(
                self.level, coords, radius, sight)
        field, colors, target, _ = interior_view.generate_interior_view(
                self.level, coords, radius, sight, visible_tiles, target)
        self.assertEqual(target, (x, y))

    def test_default_color_override(self):
        coords, radius, sight = (2, 1), 13, 13
        visible_tiles = interior_view.find_visible_tiles(
                self.level, coords, radius, sight)
        field, colors, _, _ = interior_view.generate_interior_view(
                self.level, coords, radius, sight, visible_tiles)
        self.assertEqual(colors[(radius, radius)], (255, 0, 0))
