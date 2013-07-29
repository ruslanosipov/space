from lib.obj.tile import Tile


class Glass(Tile):

    def __init__(self):
        """
        >>> Glass()
        <class 'Glass'>
        """
        super(Glass, self).__init__('0', 'glass', True, False)
