from lib.obj.item import Item


class MeleeWeapon(Item):

    def __init__(self, char, name, damage):
        """
        >>> MeleeWeapon(')', 'knife', (20, 30))
        <class 'MeleeWeapon'>
        """
        super(MeleeWeapon, self).__init__(char, name)
        self.melee_damage = damage

    #--------------------------------------------------------------------------
    # accessors

    def get_melee_damage(self):
        return self.melee_damage
