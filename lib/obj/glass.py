from lib.obj.tile import Tile


class Glass(Tile):

    def __init__(self):
        super(Glass, self).__init__('0', 'glass', True, False)
