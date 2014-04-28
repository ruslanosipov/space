"""Parent for every game tile, stationary or item."""

from lib.obj.baseobject import BaseObject

class Tile(BaseObject):
    """Parent for every game tile, stationary or item."""

    def __init__(
            self,
            char,
            name,
            is_path_blocker=False,
            is_view_blocker=False):
        super(Tile, self).__init__()
        self._interior = None
        self.char = char
        self.coords = None
        self.is_moveable = False
        self.is_path_blocker = is_path_blocker
        self.is_pickupable = False
        self.is_view_blocker = is_view_blocker
        self.name = name

    #--------------------------------------------------------------------------
    # Accessors.

    @property
    def interior(self):
        return self._interior

    @interior.setter
    def interior(self, interior):
        self._interior = interior
