import unittest

from lib import misc


class TestActivateObj(unittest.TestCase):

    def setUp(self):
        pass

    def test_object_can_be_activated(self):
        pass

    def test_wrong_object_returns_corresponding_status_msg(self):
        pass


class TestAddPlayer(unittest.TestCase):

    def test_player_can_be_added(self):
        pass


class TestEquipmentAndInventoryInteraction(unittest.TestCase):

    def setUp(self):
        pass

    def test_drop_item(self):
        pass

    def test_drop_nonexistent_item(self):
        pass

    def test_drop_stacked_item(self):
        pass

    def test_view_equipment(self):
        pass

    def test_view_empty_equipment(self):
        pass

    def test_equip_item_in_default_slot(self):
        pass

    def test_equip_item_in_invalid_slot(self):
        pass

    def test_equip_invalid_item(self):
        pass

    def test_equip_stacked_item(self):
        pass

    def test_equip_item_in_custom_slot(self):
        pass

    def test_view_empty_inventory(self):
        pass

    def test_view_simple_inventory(self):
        pass

    def test_view_stacked_inventory(self):
        pass

    def test_pick_up_existing_object(self):
        pass

    def test_pick_up_nonexistent_object(self):
        pass

    def test_unequip_item_from_default_slot(self):
        pass

    def test_unequip_item_from_custom_slot(self):
        pass

    def test_unequip_item_from_invalid_slot(self):
        pass

    def test_unequip_invalid_item_from_slot(self):
        pass


class TestMoveAndMeleeAttack(unittest.TestCase):

    def setUp(self):
        pass

    def test_moving_is_possible(self):
        pass

    def test_some_objects_obstruct_path(self):
        pass

    def test_moving_into_player_attacks_player(self):
        pass


class TestTargetAndFire(unittest.TestCase):

    def setUp(self):
        pass

    def test_target_can_be_set(self):
        pass

    def test_target_can_not_be_set_if_no_visible_players(self):
        pass

    def test_weapon_is_required_to_fire(self):
        pass

    def test_target_is_required_to_fire(self):
        pass

    def test_can_fire_at_other_player(self):
        pass


class TestLook(unittest.TestCase):

    def setUp(self):
        pass

    def test_look_displays_visible_objects(self):
        pass

    def test_look_hides_invisible_objects(self):
        pass

    def test_look_is_limited_to_visible_area(self):
        pass
