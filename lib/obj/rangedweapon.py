from lib.obj.item import Item


class RangedWeapon(Item):

    def __init__(self, char, name, damage):
        """
        >>> RangedWeapon('}', 'handgun', (10, 20))
        <class 'RangedWeapon'>
        """
        super(RangedWeapon, self).__init__(char, name)
        self.ranged_weapon = True
        self.ranged_damage = damage

    #--------------------------------------------------------------------------
    # accessors

    def get_ranged_damage(self):
        return self.ranged_damage
