from lib.obj.item import Item


class Armor(Item):
    """
    Base armor class, all armor inherits from it.
    """

    def __init__(self, char, name, damage_absorption, player_char):
        super(Armor, self).__init__(char, name)
        self.slot = 'torso'
        self.damage_absorption = damage_absorption
        self.player_char = player_char

    #--------------------------------------------------------------------------
    # accessors

    def get_damage_absorption(self):
        return self.damage_absorption

    def get_player_char(self):
        return self.player_char
