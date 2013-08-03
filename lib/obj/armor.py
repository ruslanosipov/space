from lib.obj.item import Item


class Armor(Item):

    def __init__(self):
        """
        >>> Armor()
        <class 'Armor'>
        """
        super(Armor, self).__init__(']', 'armor')
        self.slots.append('torso')
        self.damage_absorption = 10
        self.player_char = 'A'

    #--------------------------------------------------------------------------
    # accessors

    def get_damage_absorption(self):
        return self.damage_absorption

    def get_player_char(self):
        return self.player_char
