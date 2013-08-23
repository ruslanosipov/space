from lib.obj.tile import Tile


class Wall(Tile):

    def __init__(self):
        super(Wall, self).__init__('#', 'wall', True, True)
