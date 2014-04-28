"""Test armor instance."""

from lib.obj.armor import Armor


class TestArmor(Armor):
    """Test armor instance."""

    def __init__(self):
        super(TestArmor, self).__init__(
                char=']',
                name='test armor',
                damage_absorption=10,
                player_char='A')
