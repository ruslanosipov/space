"""Main characters."""

import copy
import random

from lib.obj.mob import Mob


class ItemCanNotBeEquipped(Exception):
    """Item can not be equipped."""


class Player(Mob):
    """
    Main characters: happy '@'s running around the screen.
    """

    unarmed_damage = (5, 15)

    def __init__(self, name):
        super(Player, self).__init__('@', name, 11)
        self.color = (147, 112, 219)
        self.interior = None  # Ship interior player belongs to.
        self.inventory = {}
        self.is_looking = False
        self.is_pilot = False
        self.look_coords = None
        self.target = None

    #--------------------------------------------------------------------------
    # Equipment and inventory.

    def equip(self, item):
        """Equip an item."""
        try:
            slot = item.slot
        except AttributeError:
            raise ItemCanNotBeEquipped
        if self.equipment[slot] is not None:
            self.inventory_add(self.equipment[slot])
        self.equipment[slot] = item
        if slot == 'torso':
            self.char = item.player_char

    def inventory_add(self, item, qty=1):
        """Add item to an inventory."""
        for obj in self.inventory:
            if item == obj:
                self.inventory[obj] += qty
                break
        else:
            self.inventory[item] = qty

    def inventory_remove_by_name(self, name):
        """Remove item from inventory."""
        for item, qty in self.inventory.items():
            if item.name == name:
                if qty > 1:
                    self.inventory[item] -= 1
                    return copy.deepcopy(item)
                else:
                    del self.inventory[item]
                    return item
        return False

    def unequip(self, slot='hands'):
        """Unequip item in a given slot."""
        if slot not in self.equipment.keys() or self.equipment[slot] is None:
            return False
        item = self.equipment[slot]
        self.equipment[slot] = None
        if slot == 'torso':
            self.char = '@'
        return item

    #--------------------------------------------------------------------------
    # Messages.

    def get_melee_attack_messages(self, target):
        """Return attack messages for player and hostile."""
        if self.equipment['hands'] is None:
            player_msg = "You punch %s." % target
            hostile_msg = "%s punches you!" % self.name
        else:
            weapon = self.equipment['hands'].name
            player_msg = "You hit %s with a %s." % (target, weapon)
            hostile_msg = "%s hits you with a %s." % (self.name, weapon)
        return player_msg, hostile_msg

    #--------------------------------------------------------------------------
    # Accessors.

    def get_equipment_slot(self, slot):
        """Get equipment slot value."""
        try:
            return self.equipment[slot]
        except KeyError:
            return False

    def get_melee_damage(self):
        """Random damage within player's/weapon's damage values."""
        if self.equipment['hands'] is None:
            dmg_min, dmg_max = self.unarmed_damage
        else:
            try:
                dmg_min, dmg_max = self.equipment['hands'].melee_damage
            except AttributeError:
                dmg_min, dmg_max = [dmg + 5 for dmg in self.unarmed_damage]
        return random.randint(dmg_min, dmg_max)

    def get_ranged_damage(self):
        """Random damage within weapon's min/max damage values."""
        try:
            dmg_min, dmg_max = self.equipment['hands'].ranged_damage
        except AttributeError:
            return False
        return random.randint(dmg_min, dmg_max)

    def is_gunman(self):
        """Check if player is wielding a gun."""
        if self.equipment['hands'] is None:
            return False
        try:
            return self.equipment['hands'].is_ranged_weapon
        except AttributeError:
            return False

    def toggle_looking(self):
        """Toggle if player is in a looking mode."""
        self.is_looking = False if self.is_looking else True
        if not self.is_looking:
            self.look_coords = None

    def toggle_pilot(self):
        """Toggle if player is in a pilot mode."""
        if self.is_pilot:
            self.is_pilot = False
            self.interior.spaceship.pilot = None
        else:
            self.is_pilot = True
            self.interior.spaceship.pilot = self
