"""Base armor class, all armor inherits from it."""

from lib.obj.item import Item


class Armor(Item):
    """Base armor class, all armor inherits from it."""

    def __init__(self, char, name, damage_absorption, player_char):
        super(Armor, self).__init__(char=char, name=name)
        self.damage_absorption = damage_absorption
        self.player_char = player_char
        self.slot = 'torso'
