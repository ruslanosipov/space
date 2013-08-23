from lib.obj.item import Item


class MeleeWeapon(Item):
    """
    Base melee weapon class. All melee weapons inherit from it.
    """

    def __init__(self, char, name, damage):
        super(MeleeWeapon, self).__init__(char, name)
        self.melee_damage = damage

    #--------------------------------------------------------------------------
    # accessors

    def get_melee_damage(self):
        return self.melee_damage
