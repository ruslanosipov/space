"""Test ranged weapon instance."""

from lib.obj.rangedweapon import RangedWeapon


class TestRangedWeapon(RangedWeapon):
    """Test ranged weapon instance."""

    def __init__(self):
        super(TestRangedWeapon, self).__init__(
            char='}',
            name='test ranged weapon',
            damage=(10, 20),
            accuracy=100)
