from lib.obj.item import Item


class Gun(Item):

    def __init__(self):
        """
        >>> Gun()
        <class 'Gun'>
        """
        super(Gun, self).__init__('}', 'gun')
        self.ranged_weapon = True
        self.ranged_damage = (25, 40)

    #--------------------------------------------------------------------------
    # accessors

    def get_ranged_damage(self):
        return self.ranged_damage
