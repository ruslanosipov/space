from lib.obj.rangedweapon import RangedWeapon


class TestRangedWeapon(RangedWeapon):

    def __init__(self):
        super(TestRangedWeapon, self).__init__(
            '}', 'test ranged weapon', (10, 20))
