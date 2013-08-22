import unittest

from lib import misc
from lib.interior.level3d import Level3D as InteriorLevel
from lib.exterior.level5d import Level5D as ExteriorLevel
from lib.obj.player import Player
from lib.obj.testitem import TestItem


class TestActivateObj(unittest.TestCase):

    def setUp(self):
        self.level = InteriorLevel()
        self.level.load_converted_char_map(
            [[['.', '/'], ['.']]], {'.': 'TestTile', '/': 'TestStationary'})

    def test_object_can_be_activated(self):
        self.assertEqual(misc.activate_obj((0, 0), self.level),
                         "You activate the test stationary...")

    def test_wrong_object_returns_corresponding_status_msg(self):
        self.assertEqual(misc.activate_obj((1, 0), self.level),
                         "Nothing to activate here...")


class TestAddPlayer(unittest.TestCase):

    def setUp(self):
        level = ExteriorLevel()
        self.spaceship = misc.add_spaceship('TestSpaceship', (0, 0, 0, 0),
                                            (5, 5), level)

    def test_player_can_be_added_with_default_spawn_point(self):
        misc.add_player('Mike', self.spaceship)
        obj = self.spaceship.get_interior().get_objects((5, 5))[-1]
        self.assertTrue(isinstance(obj, Player))

    def test_player_can_be_added_with_custom_spawn_point(self):
        misc.add_player('Mike', self.spaceship, (0, 0))
        obj = self.spaceship.get_interior().get_objects((0, 0))[-1]
        self.assertTrue(isinstance(obj, Player))


class TestEquipmentAndInventoryInteraction(unittest.TestCase):

    def setUp(self):
        level = ExteriorLevel()
        self.spaceship = misc.add_spaceship('TestSpaceship', (0, 0, 0, 0),
                                            (5, 5), level)
        self.player = misc.add_player('Mike', self.spaceship)

    def test_drop_item(self):
        self.player.inventory_add(TestItem())
        self.assertEqual(misc.drop_item(self.player, 'test item'),
                         "You drop a test item.")
        obj = self.spaceship.get_interior().get_objects((5, 5))[-2]
        self.assertTrue(isinstance(obj, TestItem))
        self.assertEqual(len(self.player.get_inventory()), 0)

    def test_drop_nonexistent_item(self):
        self.assertEqual(misc.drop_item(self.player, 'test item'),
                         "You do not have such an item.")
        objects = self.spaceship.get_interior().get_objects((5, 5))
        for obj in objects:
            self.assertFalse(isinstance(obj, TestItem))

    def test_drop_stacked_item(self):
        item = TestItem()
        self.player.inventory_add(item, 3)
        misc.drop_item(self.player, 'test item')
        self.assertEqual(self.player.get_inventory(), {item: 2})
        obj = self.spaceship.get_interior().get_objects((5, 5))[-2]
        self.assertTrue(isinstance(obj, TestItem))

    def test_view_empty_equipment(self):
        self.assertEqual(misc.equipment(self.player),
                         "You do not have anything equipped at the moment.")

    def test_view_equipment(self):
        self.player.inventory_add(TestItem())
        misc.equip_item(self.player, 'test item')
        self.assertEqual(misc.equipment(self.player),
                         "Equipment: test item (hands).")

    def test_equip_item_in_default_slot(self):
        self.player.inventory_add(TestItem())
        self.assertEqual(misc.equip_item(self.player, 'test item'),
                         "You equip a test item.")

    def test_equip_item_in_malformed_slot(self):
        self.player.inventory_add(TestItem())
        self.assertEqual(misc.equip_item(self.player, 'test item', 'invalid'),
                         "Incorrect equipment slot name.")

    def test_equip_item_in_restricted_slot(self):
        self.player.inventory_add(TestItem())
        self.assertEqual(misc.equip_item(self.player, 'test item', 'torso'),
                         "Item can not be equipped in selected slot.")

    def test_equip_invalid_item(self):
        self.assertEqual(misc.equip_item(self.player, 'test item'),
                         "Can not equip a test item, item not in inventory.")

    def test_equip_stacked_item(self):
        item = TestItem()
        self.player.inventory_add(item, 2)
        self.assertEqual(misc.equip_item(self.player, 'test item'),
                         "You equip a test item.")
        self.assertEqual(self.player.get_inventory(), {item: 1})

    def test_equip_item_in_custom_slot(self):
        self.player.inventory_add(TestItem())
        self.assertEqual(misc.equip_item(self.player, 'test item', 'hands'),
                         "You equip a test item.")

    def test_view_empty_inventory(self):
        self.assertEqual(misc.inventory(self.player),
                         "You do not own anything at the moment...")

    def test_view_stacked_inventory(self):
        self.player.inventory_add(TestItem(), 2)
        self.assertEqual(misc.inventory(self.player),
                         "Inventory contents: test item (2).")

    def test_pick_up_existing_object(self):
        item = TestItem()
        self.spaceship.get_interior().add_object((1, 1), item)
        self.assertEqual(
            misc.pick_up_obj(
                self.player, (1, 1), self.spaceship.get_interior()),
            "You pick up a test item...")
        self.assertNotIn(
            item, self.spaceship.get_interior().get_objects((1, 1)))
        self.assertIn(item, self.player.get_inventory().keys())

    def test_pick_up_nonexistent_object(self):
        self.assertEqual(
            misc.pick_up_obj(
                self.player, (1, 1), self.spaceship.get_interior()),
            "Nothing to pick up here...")

    def test_unequip_item(self):
        item = TestItem()
        self.player.inventory_add(item)
        misc.equip_item(self.player, 'test item')
        self.assertEqual(misc.unequip_item(self.player, 'hands'),
                         "You unequip a test item.")
        self.assertEqual(self.player.get_inventory(), {item: 1})

    def test_unequip_item_from_invalid_slot(self):
        item = TestItem()
        self.player.inventory_add(item)
        misc.equip_item(self.player, 'test item')
        self.assertEqual(misc.unequip_item(self.player, 'invalid'),
                         "You do not have an item in this slot.")
        self.assertEqual(self.player.get_inventory(), {})

    def test_attempt_to_unequip_empty_slot(self):
        self.assertEqual(misc.unequip_item(self.player, 'hands'),
                         "You do not have an item in this slot.")


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
