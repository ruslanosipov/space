"""Base class for ranged weapons, all ranged weapons inherit from it."""

from lib.obj.item import Item


class RangedWeapon(Item):
    """Base class for ranged weapons, all ranged weapons inherit from it."""

    def __init__(self, char, name, damage):
        super(RangedWeapon, self).__init__(char=char, name=name)
        self.ranged_damage = damage
        self.is_ranged_weapon = True
