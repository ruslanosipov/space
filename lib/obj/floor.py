"""Floor tile."""

from lib.obj.tile import Tile


class Floor(Tile):
    """Floor tile."""

    def __init__(self):
        super(Floor, self).__init__(char='.', name='floor')
