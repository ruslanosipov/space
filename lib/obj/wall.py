"""Wall tile."""

from lib.obj.tile import Tile


class Wall(Tile):
    """Wall tile."""

    def __init__(self):
        super(Wall, self).__init__(
                char='#',
                name='wall',
                is_path_blocker=True,
                is_view_blocker=True)
