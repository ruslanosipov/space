import unittest

from lib.interior.level3d import Level3D as InteriorLevel


class TestInteriorLevelCreation(unittest.TestCase):

    def test_one_tile_level_can_be_loaded(self):
        pass

    def test_tile_and_stationary_level_can_be_loaded(self):
        pass

    def test_raw_level_can_be_loaded_correctly(self):
        pass

    def test_level_with_extras_can_be_loaded(self):
        pass

    def test_missed_obj_definition_raises_error(self):
        pass

    def test_malformed_obj_definitions_raises_error(self):
        pass

    def test_malformed_charmap_raises_error(self):
        pass

    def test_malformed_raw_tiles_map_raises_error(self):
        pass

    def test_malformed_raw_items_map_raises_error(self):
        pass

    def test_malformed_extras_raises_error(self):
        pass


class TestInteriorLevelPlayerOperations(unittest.TestCase):

    def setUp(self):
        pass

    def test_malformed_coordinates_raise_error(self):
        pass

    def test_player_can_be_retrieved(self):
        pass

    def test_player_can_be_added(self):
        pass

    def test_player_can_be_removed(self):
        pass

    def test_nearby_players_show_up(self):
        pass

    def test_only_visible_nearby_players_show_up(self):
        pass

    def test_no_players_show_up_if_no_visible_players(self):
        pass


class TestInteriorLevelObjectOperations(unittest.TestCase):

    def setUp(self):
        pass

    def test_malformed_coordinates_raise_error(self):
        pass

    def test_existing_object_can_be_retrieved(self):
        pass

    def test_object_can_be_moved(self):
        pass

    def test_object_can_be_removed(self):
        pass

    def test_some_objects_block_path(self):
        pass

    def test_some_objects_block_view(self):
        pass
