"""Power armor object."""

from lib.obj.armor import Armor


class PowerArmor(Armor):
    """Power armor object."""

    def __init__(self):
        super(PowerArmor, self).__init__(
                char=']',
                name='power armor',
                damage_absorption=30,
                player_char='P')
