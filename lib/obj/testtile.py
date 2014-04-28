"""Test tile."""

from lib.obj.tile import Tile


class TestTile(Tile):
    """Test tile."""

    def __init__(self):
        super(TestTile, self).__init__(
                char='.',
                name='test tile')
