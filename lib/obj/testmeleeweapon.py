from lib.obj.meleeweapon import MeleeWeapon


class TestMeleeWeapon(MeleeWeapon):

    def __init__(self):
        super(TestMeleeWeapon, self).__init__(
            ')', 'test melee weapon', (20, 25))
