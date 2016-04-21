"""Laser gun."""

from lib.obj.rangedweapon import RangedWeapon


class LaserGun(RangedWeapon):
    """Laser gun."""

    def __init__(self):
        super(LaserGun, self).__init__(
                char='}',
                name='laser gun',
                damage=(25, 40),
                accuracy=50)
        self.color = (255, 0, 0)
