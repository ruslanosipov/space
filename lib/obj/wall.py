from lib.obj.tile import Tile


class Wall(Tile):

    def __init__(self):
        """
        >>> Wall()
        <class 'Wall'>
        """
        super(Wall, self).__init__('#', 'wall', True, True)
        self.set_color((120, 120, 120))
