from lib.obj.meleeweapon import MeleeWeapon


class Knife(MeleeWeapon):

    def __init__(self):
        """
        >>> Knife()
        <class 'Knife'>
        """
        super(Knife, self).__init__(')', 'knife', (15, 25))
