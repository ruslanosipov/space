"""Test melee weapon instance."""

from lib.obj.meleeweapon import MeleeWeapon


class TestMeleeWeapon(MeleeWeapon):
    """Test melee weapon instance."""

    def __init__(self):
        super(TestMeleeWeapon, self).__init__(
                char=')',
                name='test melee weapon',
                damage=(20, 25))
