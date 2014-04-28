"""A taser gun."""

from lib.obj.rangedweapon import RangedWeapon


class TaserGun(RangedWeapon):
    """A taser gun."""

    def __init__(self):
        super(TaserGun, self).__init__(
                char='}',
                name='taser gun',
                damage=(10, 20))
        self.color = (255, 153, 0)
