import unittest

from lib.misc import load_extras, load_interior_level, load_obj_definitions


class TestWorldSetup(unittest.TestCase):

    def test_interior_level_can_be_loaded_from_file(self):
        tiles_map = '###\n#.#\n#.#'
        items_map = '###\n#.#\n#+#'
        self.assertEqual(
            load_interior_level(tiles_map, items_map),
            [
                [['#'], ['#'], ['#']],
                [['#'], ['.'], ['#']],
                [['#'], ['.', '+'], ['#']]],
            "tiles and items maps should be transformed")

    def test_obj_defs_can_be_loaded(self):
        obj_defs = '.|Floor\n#|Wall\n+|Door\n'
        self.assertEqual(
            load_obj_definitions(obj_defs),
            {'.': 'Floor', '#': 'Wall', '+': 'Door'},
            "object definitions should be parsed correctly")

    def test_extras_can_be_loaded(self):
        extras = '.|Foo|(0, 0)\n#|Bar|(0, 1), (1, 0)\n'
        self.assertEqual(
            load_extras(extras),
            {(0, 0): ('.', 'Foo'), (0, 1): ('#', 'Bar'), (1, 0): ('#', 'Bar')},
            "extras should be parsed correctly")
