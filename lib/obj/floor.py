from lib.obj.tile import Tile


class Floor(Tile):

    def __init__(self):
        super(Floor, self).__init__('.', 'floor')
