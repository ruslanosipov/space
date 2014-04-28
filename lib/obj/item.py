"""Base item class. All items inherit from it."""

from lib.obj.tile import Tile


class Item(Tile):
    """Base item class. All items inherit from it."""

    def __init__(self, *args, **kwargs):
        super(Item, self).__init__(*args, **kwargs)
        self.is_moveable = False
        self.is_pickupable = True
        self.is_ranged_weapon = False
        self.melee_damage = 5
        self.slot = 'hands'

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
