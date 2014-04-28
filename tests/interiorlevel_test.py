import unittest

from lib.interior.level3d import Level3D as InteriorLevel
from lib.level import ObjectDefinitionMissing, NonexistentObjectDefinition
from lib.obj.testtile import TestTile
from lib.obj.teststationary import TestStationary
from lib.obj.teststationaryblocking import TestStationaryBlocking
from lib.obj.space import Space
from lib.obj.player import Player


class TestInteriorLevelCreation(unittest.TestCase):

    def test_one_tile_level_can_be_loaded(self):
        level = InteriorLevel()
        char_map, obj_defs = [[['.']]], {'.': 'TestTile'}
        level.load_converted_char_map(char_map, obj_defs)
        tile = level.get_objects((0, 0))[0]
        self.assertTrue(isinstance(tile, TestTile),
                        "map elements should be game object instances")

    def test_raw_level_can_be_loaded_correctly(self):
        level = InteriorLevel()
        tiles_map, items_map = [['.'], ['.']], [['/'], ['.']]
        obj_defs = {'.': 'TestTile', '/': 'TestStationary'}
        level.load_char_map(tiles_map, items_map, obj_defs)
        tiles = level.get_objects((0, 0))
        self.assertTrue(isinstance(tiles[0], TestTile) and \
                        isinstance(tiles[1], TestStationary),
                        "map elements should be loaded in correct order")
        tiles = level.get_objects((1, 0))
        self.assertEqual(len(tiles), 1, "no duplicate items are allowed")

    def test_level_with_extras_can_be_loaded(self):
        level = InteriorLevel()
        char_map = [[['.']]]
        obj_defs = {'.': 'TestStationary'}
        extras = {(0, 0): ('.', 'TestTile')}
        level.load_converted_char_map(char_map, obj_defs, extras)
        tile = level.get_objects((0, 0))[0]
        self.assertTrue(isinstance(tile, TestTile),
                        "extras should override existing object definitions")

    def test_missed_obj_definition_raises_error(self):
        level = InteriorLevel()
        char_map = [[['.']]]
        obj_defs = {}
        self.assertRaises(ObjectDefinitionMissing,
                          level.load_converted_char_map, char_map, obj_defs)

    def test_nonexistent_obj_definition_raises_error(self):
        level = InteriorLevel()
        char_map = [[['.']]]
        obj_defs = {'.': 'TestTail'}
        self.assertRaises(NonexistentObjectDefinition,
                          level.load_converted_char_map, char_map, obj_defs)


class TestInteriorLevelObjectOperations(unittest.TestCase):

    def setUp(self):
        self.level = InteriorLevel()
        char_map = [[['.', '/'], ['.']]]
        obj_defs = {'.': 'TestTile', '/': 'TestStationary'}
        self.level.load_converted_char_map(char_map, obj_defs)

    def test_malformed_coordinates_raise_error(self):
        self.assertRaises(IndexError, self.level.add_object, (-9, -9), None)
        self.assertRaises(IndexError, self.level.add_object, (9, 9), None)
        tile = self.level.get_objects((1, 0))[0]
        self.assertRaises(IndexError, self.level.move_object,
                          (0, 0), (9, 9), tile)
        self.assertRaises(IndexError, self.level.remove_object, (9, 9), None)
        self.assertRaises(IndexError, self.level.is_path_blocker, (9, 9))
        self.assertRaises(IndexError, self.level.is_view_blocker, (9, 9))

    def test_existing_object_can_be_retrieved(self):
        tile = self.level.get_objects((1, 0))[0]
        self.assertTrue(isinstance(tile, TestTile),
                        "existing object should be retrievable")

    def test_object_can_be_added(self):
        stationary = TestStationary()
        self.level.add_object((1, 0), stationary)
        obj = self.level.get_objects((1, 0))[-1]
        self.assertEqual(obj, stationary,
                         "same object should be retreived")
        self.assertEqual(obj.coords, (1, 0),
                         "object should have coordinates set")
        self.assertEqual(obj.interior, self.level,
                         "level should be set as interior attribute")

    def test_object_can_be_added_at_index(self):
        stationary = TestStationary()
        self.level.add_object((1, 0), stationary, 1)
        obj = self.level.get_objects((1, 0))[-2]
        self.assertEqual(obj, stationary,
                         "same object should be retreived")
        self.assertEqual(obj.coords, (1, 0),
                         "object should have coordinates set")
        self.assertEqual(obj.interior, self.level,
                         "level should be set as interior attribute")

    def test_object_can_be_moved(self):
        stationary = self.level.get_objects((0, 0))[-1]
        self.level.move_object((0, 0), (1, 0), stationary)
        obj = self.level.get_objects((1, 0))[-1]
        self.assertEqual(obj, stationary,
                         "same object should be retreived")
        self.assertEqual(obj.coords, (1, 0),
                         "object should have correct coordinates set")

    def test_nonexistent_object_movement_raises_exception(self):
        self.assertRaises(ValueError, self.level.move_object,
                          (0, 0), (1, 0), TestStationary())

    def test_object_can_be_removed(self):
        stationary = self.level.get_objects((0, 0))[-1]
        self.level.remove_object((0, 0), stationary)
        objects = self.level.get_objects((0, 0))
        self.assertNotIn(stationary, objects,
                         "removed object should not be returned")

    def test_nonexistent_object_removal_raises_exception(self):
        self.assertRaises(ValueError, self.level.remove_object,
                          (0, 0), TestStationary())

    def test_some_objects_block_path(self):
        self.assertFalse(self.level.is_path_blocker((1, 0)),
                         "no path blocking objects at these coordinates")
        self.level.add_object((1, 0), TestStationaryBlocking())
        self.level.is_path_blocker((1, 0))
        self.assertTrue(self.level.is_path_blocker((1, 0)),
                        "TestStationaryBlocking should block the path")

    def test_some_objects_block_view(self):
        self.assertFalse(self.level.is_view_blocker((1, 0)),
                         "no view blocking objects at these coordinates")
        self.level.add_object((1, 0), TestStationaryBlocking())
        self.level.is_path_blocker((1, 0))
        self.assertTrue(self.level.is_view_blocker((1, 0)),
                        "TestStationaryBlocking should block the view")

    def test_objects_outside_level_boundaries_return_space(self):
        tile = self.level.get_objects((9, 9))[0]
        self.assertTrue(isinstance(tile, Space), ("if object does not exist "
                        "on the map - create Space object"))


class TestInteriorLevelPlayerOperations(unittest.TestCase):

    def setUp(self):
        self.level = InteriorLevel()
        char_map = [[['.', '/'], ['.'], ['.']]]
        obj_defs = {'.': 'TestTile', '/': 'TestStationary'}
        self.level.load_converted_char_map(char_map, obj_defs)

    def test_malformed_coordinates(self):
        self.assertRaises(IndexError, self.level.get_player, (9, 9))
        self.assertRaises(IndexError, self.level.add_player, (9, 9), None)

    def test_player_can_be_added_and_retrieved(self):
        self.assertFalse(self.level.get_player((0, 0)),
                         "nonexistent player should not be retrievable")
        player = Player('Mike')
        self.level.add_player((0, 0), player)
        self.assertEqual(self.level.get_player((0, 0)), player,
                         "added player should be retrievable")

    def test_player_can_be_removed(self):
        player = Player('Mike')
        self.level.add_player((0, 0), player)
        self.level.remove_player(player)
        self.assertFalse(self.level.get_player((0, 0)),
                         "player should be removed")

    def test_nearest_players_show_up(self):
        player = Player('Mike')
        self.level.add_player((0, 0), player)
        self.level.add_player((1, 0), Player('Josh'))
        self.level.add_player((2, 0), Player('Tosh'))
        self.assertEqual(self.level.get_nearest_players_coords((0, 0),
                         player.sight, [(0, 0), (1, 0), (2, 0)]),
                         [(1, 0), (2, 0)], ("coordinates should be returned "
                         "in correct order"))

    def test_only_visible_nearest_players_show_up(self):
        player = Player('Mike')
        self.level.add_player((0, 0), player)
        self.level.add_object((1, 0), TestStationaryBlocking())
        self.level.add_player((2, 0), Player('Josh'))
        self.assertEqual(self.level.get_nearest_players_coords((0, 0),
                         player.sight, [(0, 0), (1, 0)]), [],
                         "invisible players should not be returned")

    def test_no_players_show_up_if_no_visible_players(self):
        player = Player('Mike')
        self.level.add_player((0, 0), player)
        self.assertEqual(self.level.get_nearest_players_coords((0, 0), 
                         player.sight, [(0, 0), (1, 0), (2, 0)]), [],
                         ("no players should be returned with no surrounding "
                         "players"))
