from lib.obj.tile import Tile


class Item(Tile):

    def __init__(self, *args, **kwargs):
        """
        >>> Item('}', 'wall')
        <class 'Item'>
        """
        super(Item, self).__init__(*args, **kwargs)
        self.moveable = True
