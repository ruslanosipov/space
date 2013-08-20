from lib.obj.item import Item


class Armor(Item):

    def __init__(self, char, name, damage_absorption, player_char):
        """
        >>> Armor(']', 'armor', 10, 'A')
        <class 'Armor'>
        """
        super(Armor, self).__init__(char, name)
        self.slots.append('torso')
        self.damage_absorption = damage_absorption
        self.player_char = player_char

    #--------------------------------------------------------------------------
    # accessors

    def get_damage_absorption(self):
        return self.damage_absorption

    def get_player_char(self):
        return self.player_char
