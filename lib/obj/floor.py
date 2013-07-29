from lib.obj.tile import Tile


class Floor(Tile):

    def __init__(self):
        """
        >>> Floor()
        <class 'Floor'>
        """
        super(Floor, self).__init__('.', 'floor')
        self.set_color((120, 120, 120))
