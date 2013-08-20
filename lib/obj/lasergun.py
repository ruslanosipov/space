from lib.obj.rangedweapon import RangedWeapon


class LaserGun(RangedWeapon):

    def __init__(self):
        """
        >>> LaserGun()
        <class 'LaserGun'>
        """
        super(LaserGun, self).__init__('}', 'laser gun', (25, 40))
        self.set_color((255, 0, 0))
