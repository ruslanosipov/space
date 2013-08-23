import unittest

from lib.obj.player import Player
from lib.obj.testrangedweapon import TestRangedWeapon
from lib.obj.testmeleeweapon import TestMeleeWeapon
from lib.obj.testarmor import TestArmor


class TestPlayerInventory(unittest.TestCase):

    def setUp(self):
        self.player = Player('Mike')

    def test_duplicate_items_stack(self):
        self.player.inventory_add(TestRangedWeapon())
        self.player.inventory_add(TestRangedWeapon(), 3)
        inv = self.player.get_inventory()
        self.assertEqual(dict([(k.get_name(), v) for k, v in inv.items()]),
                         {'test ranged weapon': 4})

    def test_removing_item_from_inventory(self):
        self.player.inventory_add(TestRangedWeapon(), 2)
        item = self.player.inventory_remove_by_name('test ranged weapon')
        self.assertEqual(item.get_name(), 'test ranged weapon')
        self.assertFalse(self.player.inventory_remove_by_name('sword'),
                         "non existent item should yield False")
        inv = self.player.get_inventory()
        self.assertEqual(dict([(k.get_name(), v) for k, v in inv.items()]),
                         {'test ranged weapon': 1})
        item = self.player.inventory_remove_by_name('test ranged weapon')
        self.assertEqual(self.player.get_inventory(), {})

    def test_melee_weapon_affects_damage(self):
        unarmed_damage = self.player.get_melee_damage()
        self.player.equip(TestMeleeWeapon())
        self.assertGreater(self.player.get_melee_damage(),
                           unarmed_damage)

    def test_ranged_weapon_required_to_shoot(self):
        self.assertFalse(self.player.is_gunman(),
                         "player should not be able to shoot without a gun")
        self.assertFalse(self.player.get_ranged_damage())
        self.player.equip(TestRangedWeapon())
        self.assertTrue(self.player.is_gunman(),
                        "player should be able to shoot after equiping a gun")
        self.assertGreater(self.player.get_ranged_damage(), 0,
                           "damage should be non-negative integer")

    def test_unarmored_player_does_not_alter_damage(self):
        self.player.receive_damage(100)
        self.assertFalse(self.player.is_alive(),
                         "player without armor should not alter damage")

    def test_armor_affects_received_damage(self):
        self.player.equip(TestArmor(), 'torso')
        self.player.receive_damage(100)
        self.assertTrue(self.player.is_alive(),
                        "armor should reduce received damage")

    def test_armor_changes_player_char(self):
        default_char = self.player.get_char()
        armor = TestArmor()
        self.player.equip(armor, 'torso')
        self.assertEqual(self.player.get_char(), armor.get_player_char(),
                         "equipping armor should change player char")
        self.player.unequip('torso')
        self.assertEqual(self.player.get_char(), default_char,
                         ("player char should reset after unequipping the "
                          "armor: %s" % self.player.get_char()))
