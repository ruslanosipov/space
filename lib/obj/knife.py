from lib.obj.meleeweapon import MeleeWeapon


class Knife(MeleeWeapon):

    def __init__(self):
        super(Knife, self).__init__(')', 'knife', (15, 25))
