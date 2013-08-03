import random
import copy

from lib.obj.mob import Mob


class IncorrectSlotName(Exception):
    pass


class ItemCanNotBeEquippedInSlot(Exception):
    pass


class Player(Mob):

    def __init__(self, name):
        """
        >>> Player('Mike')
        <class 'Player'> Mike
        """
        super(Player, self).__init__('@', name, 11)
        self.inventory = {}
        self.target = None
        self.pilot = False
        self.interior = None
        self.unarmed_damage = (5, 15)
        self.equipment = {
            'hands': None,
            'torso': None,
            'head': None}
        self.set_color((147, 112, 219))

    #--------------------------------------------------------------------------
    # equipment and inventory

    def equip(self, item, slot='hands'):
        if slot not in self.equipment.keys():
            raise IncorrectSlotName
        if self.equipment[slot] is not None:
            self.inventory_add(self.equipment[slot])
        if slot not in item.get_slots():
            raise ItemCanNotBeEquippedInSlot
        self.equipment[slot] = item
        if slot == 'torso':
            self.char = item.get_player_char()

    def inventory_add(self, item, qty=1):
        for obj in self.inventory:
            if item == obj:
                self.inventory[obj] += qty
                break
        else:
            self.inventory[item] = qty

    def inventory_remove_by_name(self, name):
        for item, qty in self.inventory.items():
            if item.get_name() == name:
                if qty > 1:
                    self.inventory[item] -= 1
                    return copy.deepcopy(item)
                else:
                    del self.inventory[item]
                    return item
        return False

    def unequip(self, slot='hands'):
        if slot not in self.equipment.keys() or self.equipment[slot] is None:
            return False
        item = self.equipment[slot]
        self.equipment[slot] = None
        if slot == 'torso':
            self.char = '@'
        return item

    #--------------------------------------------------------------------------
    # messages

    def get_melee_attack_messages(self, target):
        if self.equipment['hands'] is None:
            player_msg = "You punch %s." % target
            hostile_msg = "%s punches you!" % self
        else:
            weapon = self.equipment['hands'].get_name()
            player_msg = "You hit %s with a %s." % (target, weapon)
            hostile_msg = "%s hits you with a %s." % (target, weapon)
        return player_msg, hostile_msg

    #--------------------------------------------------------------------------
    # accessors

    def is_pilot(self):
        return self.pilot

    def get_equipment(self):
        return self.equipment

    def get_inventory(self):
        return self.inventory

    def get_interior(self):
        return self.interior

    def get_melee_damage(self):
        if self.equipment['hands'] is None:
            dmg_min, dmg_max = self.unarmed_damage
        else:
            try:
                dmg_min, dmg_max = self.equipment['hands'].get_melee_damage()
            except AttributeError:
                dmg_min, dmg_max = map(lambda x: x + 5, self.unarmed_damage)
        return random.randint(dmg_min, dmg_max)

    def get_ranged_damage(self):
        try:
            dmg_min, dmg_max = self.equipment['hands'].get_ranged_damage()
            return random.randint(dmg_min, dmg_max)
        except AttributeError:
            return False

    def get_target(self):
        return self.target

    def is_gunman(self):
        if self.equipment['hands'] is None:
            return False
        try:
            return self.equipment['hands'].is_ranged_weapon()
        except AttributeError:
            return False

    def set_pilot(self):
        if self.pilot:
            self.pilot = False
            self.get_interior().get_spaceship().set_pilot()
        else:
            self.pilot = True
            self.get_interior().get_spaceship().set_pilot(self)

    def set_interior(self, interior=None):
        self.interior = interior

    def set_target(self, target=None):
        self.target = target
