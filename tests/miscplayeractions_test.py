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
        obj = self.spaceship.interior.get_objects((5, 5))[-1]
        self.assertTrue(isinstance(obj, Player))

    def test_player_can_be_added_with_custom_spawn_point(self):
        misc.add_player('Mike', self.spaceship, (0, 0))
        obj = self.spaceship.interior.get_objects((0, 0))[-1]
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
        obj = self.spaceship.interior.get_objects((5, 5))[-2]
        self.assertTrue(isinstance(obj, TestItem))
        self.assertEqual(len(self.player.inventory), 0)

    def test_drop_nonexistent_item(self):
        self.assertEqual(misc.drop_item(self.player, 'test item'),
                         "You do not have such an item.")
        objects = self.spaceship.interior.get_objects((5, 5))
        for obj in objects:
            self.assertFalse(isinstance(obj, TestItem))

    def test_drop_stacked_item(self):
        item = TestItem()
        self.player.inventory_add(item, 3)
        misc.drop_item(self.player, 'test item')
        self.assertEqual(self.player.inventory, {item: 2})
        obj = self.spaceship.interior.get_objects((5, 5))[-2]
        self.assertTrue(isinstance(obj, TestItem))

    def test_equip_item_without_a_slot(self):
        item = TestItem()
        del item.slot
        item.is_pickupable = True
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
        self.assertEqual(self.player.inventory, {item: 1})

    def test_equip_item(self):
        self.player.inventory_add(TestItem())
        self.assertEqual(misc.equip_item(self.player, 'test item'),
                         "You equip a test item.")

    def test_pick_up_existing_object(self):
        item = TestItem()
        self.spaceship.interior.add_object((1, 1), item)
        self.assertEqual(
            misc.pick_up_obj(
                self.player, (1, 1), self.spaceship.interior),
            "You pick up a test item...")
        self.assertNotIn(
            item, self.spaceship.interior.get_objects((1, 1)))
        self.assertIn(item, self.player.inventory.keys())

    def test_pick_up_nonexistent_object(self):
        self.assertEqual(
            misc.pick_up_obj(
                self.player, (1, 1), self.spaceship.interior),
            "Nothing to pick up here...")

    def test_unequip_item(self):
        item = TestItem()
        self.player.inventory_add(item)
        misc.equip_item(self.player, 'test item')
        self.assertEqual(misc.unequip_item(self.player, 'hands'),
                         "You unequip a test item.")
        self.assertEqual(self.player.inventory, {item: 1})

    def test_unequip_item_from_invalid_slot(self):
        item = TestItem()
        self.player.inventory_add(item)
        misc.equip_item(self.player, 'test item')
        self.assertEqual(misc.unequip_item(self.player, 'invalid'),
                         "You do not have an item in this slot.")
        self.assertEqual(self.player.inventory, {})

    def test_attempt_to_unequip_empty_slot(self):
        self.assertEqual(misc.unequip_item(self.player, 'hands'),
                         "You do not have an item in this slot.")


class TestMoveAndMeleeAttack(unittest.TestCase):

    def setUp(self):
        self.level = InteriorLevel()
        char_map = [
            [['.'], ['.']],
            [['.', '+'], ['.']],
            [['.'], ['.']]]
        obj_defs = {'.': 'TestTile', '+': 'TestStationaryBlocking'}
        self.level.load_converted_char_map(char_map, obj_defs)
        self.player = Player('Mike')
        self.level.add_player((0, 0), self.player)
        self.chatserver = ChatServer()

    def test_moving_is_possible(self):
        self.assertEqual(
            misc.move(self.player, (1, 0), self.level, self.chatserver), '')
        self.assertEqual(self.player.coords, (1, 0))

    def test_moving_updates_other_players_target(self):
        hostile = Player('Tom')
        hostile.target = (0, 0)
        self.level.add_player((0, 2), hostile)
        self.assertEqual(
            misc.move(self.player, (1, 0), self.level, self.chatserver), '')
        self.assertEqual(hostile.target, (1, 0))

    def test_some_objects_obstruct_path(self):
        self.assertEqual(
            misc.move(self.player, (0, 1), self.level, self.chatserver),
            "Your path is obstructed by the test blocking stationary...")
        self.assertEqual(self.player.coords, (0, 0))

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
        self.assertLess(hostile.health, 100)


class TestTargetAndFire(unittest.TestCase):

    def setUp(self):
        self.level = InteriorLevel()
        char_map, obj_defs = [
            [['.'], ['.'], ['.'], ['.']],
            [['.'], ['.'], ['.'], ['.']],
            [['.'], ['.'], ['.'], ['.']]], {'.': 'TestTile'}
        self.level.load_converted_char_map(char_map, obj_defs)
        self.player, self.hostile = Player('Mike'), Player('Josh')
        self.player.visible_targets = [(1, 0)]
        self.level.add_player((0, 0), self.player)
        self.level.add_player((1, 0), self.hostile)
        self.chatserver = ChatServer()

    def test_target_can_be_set_with_single_foe(self):
        self.assertEqual(misc.set_target(self.player), '')
        self.assertEqual(self.player.target, (1, 0))

    def test_target_is_set_to_closest_foe(self):
        self.second_hostile = Player('Tim')
        self.third_hostile = Player('Steve')
        self.level.add_player((2, 2), self.second_hostile)
        self.level.add_player((3, 0), self.third_hostile)
        self.player.visible_targets = [(1, 0), (2, 2), (3, 0)]

        self.assertEqual(misc.set_target(self.player), '')
        self.assertEqual(self.player.target, (1, 0))

    def test_if_target_is_none_target_is_set_to_closest_foe_when_cycled(self):
        self.second_hostile = Player('Tim')
        self.third_hostile = Player('Steve')
        self.level.add_player((2, 2), self.second_hostile)
        self.level.add_player((3, 0), self.third_hostile)
        self.player.visible_targets = [(1, 0), (2, 2), (3, 0)]

        self.assertEqual(misc.set_target(self.player, use_closest_target=False, shift=1), '')
        self.assertEqual(self.player.target, (1, 0))

        self.player.target = None
        self.assertEqual(misc.set_target(self.player, use_closest_target=False, shift=-1), '')
        self.assertEqual(self.player.target, (1, 0))

    def test_cycle_target_closer(self):
        self.second_hostile = Player('Tim')
        self.third_hostile = Player('Steve')
        self.level.add_player((2, 2), self.second_hostile)
        self.level.add_player((3, 0), self.third_hostile)
        self.player.visible_targets = [(1, 0), (2, 2), (3, 0)]
        self.player.target = (2, 2)

        self.assertEqual(misc.set_target(self.player, use_closest_target=False, shift=-1), '')
        self.assertEqual(self.player.target, (1, 0))

    def test_cycle_target_further(self):
        self.second_hostile = Player('Tim')
        self.third_hostile = Player('Steve')
        self.level.add_player((2, 2), self.second_hostile)
        self.level.add_player((3, 0), self.third_hostile)
        self.player.visible_targets = [(1, 0), (2, 2), (3, 0)]
        self.player.target = (2, 2)

        self.assertEqual(misc.set_target(self.player, use_closest_target=False, shift=1), '')
        self.assertEqual(self.player.target, (3, 0))

    def test_cycle_target_to_beggining(self):
        self.second_hostile = Player('Tim')
        self.level.add_player((2, 2), self.second_hostile)
        self.player.visible_targets = [(1, 0), (2, 2)]
        self.player.target = (2, 2)

        self.assertEqual(misc.set_target(self.player, use_closest_target=False, shift=1), '')
        self.assertEqual(self.player.target, (1, 0))

    def test_cycle_target_to_end(self):
        self.second_hostile = Player('Tim')
        self.level.add_player((2, 2), self.second_hostile)
        self.player.visible_targets = [(1, 0), (2, 2)]
        self.player.target = (1, 0)

        self.assertEqual(misc.set_target(self.player, use_closest_target=False, shift=-1), '')
        self.assertEqual(self.player.target, (2, 2))

    def test_target_can_not_be_set_if_no_visible_players(self):
        self.player.visible_targets = []

        self.assertEqual(misc.set_target(self.player),
                         'No suitable target found...')
        self.assertIsNone(self.player.target)

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

    def test_can_fire_at_other_player_with_100_accuracy(self):
        weapon = TestRangedWeapon()
        weapon.ranged_accuracy = 100
        self.player.inventory_add(weapon)
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
        self.assertLess(self.hostile.health, 100)

    def test_fire_and_miss_with_0_accuracy(self):
        weapon = TestRangedWeapon()
        weapon.ranged_accuracy = 0
        self.player.inventory_add(weapon)
        misc.equip_item(self.player, 'test ranged weapon')
        misc.set_target(self.player, self.level, [(0, 0), (1, 0)])
        self.assertEqual(
            misc.interior_fire(self.player, self.level, self.chatserver), '')
        self.assertEqual(
            self.chatserver.get_recent_for_recipient(self.player),
            [('You shoot at Josh. You miss.', 3)])
        self.assertEqual(
            self.chatserver.get_recent_for_recipient(self.hostile),
            [('Mike shoots at you. Mike misses.', 3)])
        self.assertEquals(self.hostile.health, 100)


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
