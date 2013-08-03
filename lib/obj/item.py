from lib.obj.tile import Tile


class Item(Tile):

    def __init__(self, *args, **kwargs):
        """
        >>> Item('}', 'wall')
        <class 'Item'>
        """
        super(Item, self).__init__(*args, **kwargs)
        self.pickupable = True
        self.moveable = False
        self.melee_damage = 5
        self.ranged_weapon = False

    #--------------------------------------------------------------------------
    # accessors

    def is_ranged_weapon(self):
        return self.ranged_weapon

    def get_melee_damage(self):
        return self.damage
