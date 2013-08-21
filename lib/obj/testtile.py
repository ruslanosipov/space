from lib.obj.tile import Tile


class TestTile(Tile):

    def __init__(self):
        super(TestTile, self).__init__('.', 'test tile')
