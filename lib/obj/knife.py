"""Knife (a melee weapon)."""

from lib.obj.meleeweapon import MeleeWeapon


class Knife(MeleeWeapon):
    """Knife (a melee weapon)."""

    def __init__(self):
        super(Knife, self).__init__(
                char=')',
                name='knife',
                damage=(15, 25))
