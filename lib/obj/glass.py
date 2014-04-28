"""Glass tile."""

from lib.obj.tile import Tile


class Glass(Tile):
    """Glass tile."""

    def __init__(self):
        super(Glass, self).__init__(
                char='0',
                name='glass',
                is_path_blocker=True,
                is_view_blocker=False)
