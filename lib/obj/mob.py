"""Base class for players and alike."""

from lib.obj.baseobject import BaseObject


class Mob(BaseObject):
    """Base class for players and alike."""

    health_max = 100

    def __init__(self, char, name, sight=11):
        super(Mob, self).__init__()
        self._color = None
        self.char = char
        self.coords = (0, 0)
        self.equipment = {
            'hands': None,
            'head': None,
            'torso': None,
        }
        self.health = self.health_max
        self.is_alive = True
        self.is_default_color = True
        self.is_path_blocker = True
        self.is_view_blocker = False
        self.level = None  # What level is object on currently.
        self.name = name
        self.sight = sight

    def __repr__(self):
        return "<class '%s'> %s" % (self.__class__.__name__, self.name)

    def receive_damage(self, damage):
        """Receive damage, lowered by worn armor damage absorption."""
        for slot in ['torso', 'head']:
            if self.equipment[slot] is not None:
                try:
                    damage -= self.equipment[slot].damage_absorption
                    if damage < 0:
                        damage = 0
                except AttributeError:
                    pass
        self.health -= damage
        if self.health <= 0:
            self.is_alive = False
