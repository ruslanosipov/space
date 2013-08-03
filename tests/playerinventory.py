import unittest

from lib.obj.player import Player
from lib.obj.gun import Gun
from lib.obj.knife import Knife


class TestPlayerInventory(unittest.TestCase):

    def setUp(self):
        self.player = Player('Mike')

    def test_duplicate_items_stack(self):
        self.player.inventory_add(Gun())
        self.player.inventory_add(Gun(), 3)
        inv = self.player.get_inventory()
        self.assertEqual(dict([(k.get_name(), v) for k, v in inv.items()]),
                         {'gun': 4}, "items of the same type must stack")

    def test_removing_item_from_inventory(self):
        self.player.inventory_add(Gun(), 2)
        item = self.player.inventory_remove_by_name('gun')
        self.assertEqual(item.get_name(), 'gun',
                         "correct item should be returned")
        self.assertFalse(self.player.inventory_remove_by_name('sword'),
                         "non existent item should yield False")
        inv = self.player.get_inventory()
        self.assertEqual(dict([(k.get_name(), v) for k, v in inv.items()]),
                         {'gun': 1}, "items stack should decrease")
        item = self.player.inventory_remove_by_name('gun')
        self.assertEqual(self.player.get_inventory(), {},
                         "last item in stack should be removed from inventory")

    def test_melee_weapon_affects_damage(self):
        unarmed_damage = self.player.get_melee_damage()
        self.player.equip(Knife())
        self.assertGreaterEqual(self.player.get_melee_damage(),
                                unarmed_damage,
                                "melee weapon should affect damage")
        self.player.equip()
        self.assertEqual(self.player.get_melee_damage(), unarmed_damage,
                         "unwielding melee weapon should reset unarmed damage")

    def test_ranged_weapon_required_to_shoot(self):
        self.assertFalse(self.player.is_gunman(),
                         "player should not be able to shoot without a gun")
        self.assertFalse(self.player.get_ranged_damage())
        self.player.equip(Gun())
        self.assertTrue(self.player.is_gunman(),
                        "player should be able to shoot after equiping a gun")
        self.assertGreater(self.player.get_ranged_damage(), 0,
                           "damage should be non-negative integer")
