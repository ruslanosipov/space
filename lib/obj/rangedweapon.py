from lib.obj.item import Item


class RangedWeapon(Item):
    """
    Base class for ranged weapons, all ranged weapons inherit from it.
    """

    def __init__(self, char, name, damage):
        super(RangedWeapon, self).__init__(char, name)
        self.ranged_weapon = True
        self.ranged_damage = damage

    #--------------------------------------------------------------------------
    # accessors

    def get_ranged_damage(self):
        return self.ranged_damage
