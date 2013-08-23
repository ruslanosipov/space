from lib.obj.rangedweapon import RangedWeapon


class TaserGun(RangedWeapon):

    def __init__(self):
        super(TaserGun, self).__init__('}', 'taser gun', (10, 20))
        self.set_color((255, 153, 0))
