import unittest

from lib import misc
from lib.interior.level3d import Level3D as InteriorLevel
from lib.exterior.level5d import Level5D as ExteriorLevel
from lib.chatserver import ChatServer
from lib.obj.player import Player
from lib.obj.testitem import TestItem
from lib.obj.testrangedweapon import TestRangedWeapon


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

    def test_equip_item_without_a_slot(self):
        def method_does_not_exist():
            raise AttributeError
        item = TestItem()
        item.get_slot = method_does_not_exist
        self.player.inventory_add(item)
        self.assertEqual(misc.equip_item(self.player, 'test item'),
                         "Item can not be equipped.")

    def test_equip_invalid_item(self):
        self.assertEqual(misc.equip_item(self.player, 'test item'),
                         "Can not equip a test item, item not in inventory.")

    def test_equip_stacked_item(self):
        item = TestItem()
        self.player.inventory_add(item, 2)
        self.assertEqual(misc.equip_item(self.player, 'test item'),
                         "You equip a test item.")
        self.assertEqual(self.player.get_inventory(), {item: 1})

    def test_equip_item(self):
        self.player.inventory_add(TestItem())
        self.assertEqual(misc.equip_item(self.player, 'test item'),
                         "You equip a test item.")

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
        self.level = InteriorLevel()
        char_map = [[['.'], ['.']], [['.', '+'], ['.']]]
        obj_defs = {'.': 'TestTile', '+': 'TestStationaryBlocking'}
        self.level.load_converted_char_map(char_map, obj_defs)
        self.player = Player('Mike')
        self.level.add_player((0, 0), self.player)
        self.chatserver = ChatServer()

    def test_moving_is_possible(self):
        self.assertEqual(
            misc.move(self.player, (1, 0), self.level, self.chatserver), '')
        self.assertEqual(self.player.get_coords(), (1, 0))

    def test_some_objects_obstruct_path(self):
        self.assertEqual(
            misc.move(self.player, (0, 1), self.level, self.chatserver),
            "Your path is obstructed by the test blocking stationary...")
        self.assertEqual(self.player.get_coords(), (0, 0))

    def test_moving_into_player_attacks_player(self):
        hostile = Player('Josh')
        self.level.add_player((1, 0), hostile)
        self.assertEqual(
            misc.move(self.player, (1, 0), self.level, self.chatserver), '')
        self.assertEqual(
            self.chatserver.get_recent_for_recipient(self.player),
            [('You punch Josh.', 3)])
        self.assertEqual(
            self.chatserver.get_recent_for_recipient(hostile),
            [('Mike punches you!', 3)])
        self.assertLess(hostile.get_health(), 100)


class TestTargetAndFire(unittest.TestCase):

    def setUp(self):
        self.level = InteriorLevel()
        char_map, obj_defs = [[['.'], ['.']]], {'.': 'TestTile'}
        self.level.load_converted_char_map(char_map, obj_defs)
        self.player, self.hostile = Player('Mike'), Player('Josh')
        self.level.add_player((0, 0), self.player)
        self.level.add_player((1, 0), self.hostile)
        self.chatserver = ChatServer()

    def test_target_can_be_set(self):
        self.assertEqual(
            misc.set_target(self.player, self.level, [(0, 0), (1, 0)]), '')
        self.assertEqual(self.player.get_target(), (1, 0))

    def test_target_can_not_be_set_if_no_visible_players(self):
        self.assertEqual(misc.set_target(self.player, self.level, [(0, 0)]),
                         'No suitable target found...')
        self.assertIsNone(self.player.get_target())

    def test_weapon_is_required_to_fire(self):
        self.assertEqual(
            misc.interior_fire(self.player, self.level, self.chatserver),
            "You have no weapon to fire from...")

    def test_target_is_required_to_fire(self):
        self.player.inventory_add(TestRangedWeapon())
        misc.equip_item(self.player, 'test ranged weapon')
        self.assertEqual(
            misc.interior_fire(self.player, self.level, self.chatserver),
            "Target is not set...")

    def test_can_fire_at_other_player(self):
        self.player.inventory_add(TestRangedWeapon())
        misc.equip_item(self.player, 'test ranged weapon')
        misc.set_target(self.player, self.level, [(0, 0), (1, 0)])
        self.assertEqual(
            misc.interior_fire(self.player, self.level, self.chatserver), '')
        self.assertEqual(
            self.chatserver.get_recent_for_recipient(self.player),
            [('You shoot at Josh.', 3)])
        self.assertEqual(
            self.chatserver.get_recent_for_recipient(self.hostile),
            [('Mike shoots at you.', 3)])
        self.assertLess(self.hostile.get_health(), 100)


class TestLook(unittest.TestCase):

    def setUp(self):
        self.level = InteriorLevel()
        char_map = [[['.'], ['.', '?']]]
        obj_defs = {'.': 'TestTile', '?': 'TestItem'}
        self.level.load_converted_char_map(char_map, obj_defs)
        self.player = Player('Mike')
        self.level.add_player((0, 0), self.player)

    def test_look_displays_visible_objects(self):
        self.assertEqual(
            misc.look(self.player, (0, 0), self.level, [(0, 0), (1, 0)]),
            "You see: Mike, test tile.")
        self.assertEqual(
            misc.look(self.player, (1, 0), self.level, [(0, 0), (1, 0)]),
            "You see: test item, test tile.")

    def test_look_hides_invisible_objects(self):
        self.assertEqual(misc.look(self.player, (1, 0), self.level, [(0, 0)]),
                         "You can't see anything there.")

    def test_look_is_limited_to_visible_area(self):
        self.assertIsNone(misc.look(self.player, (20, 20), self.level, []))
