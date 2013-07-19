from lib.obj.tile import Tile


class Stationary(Tile):

    def __init__(self, *args, **kwargs):
        super(Stationary, self).__init__(*args, **kwargs)
        self.moveable = False

    def activate(self):
        """
        >>> s = Stationary('c', 'console', True)
        >>> msg = "You activate the %s, nothing happens..." % s.get_name()
        >>> s.activate() == msg
        True
        """
        msg = "You activate the %s, nothing happens..." % self.name
        return msg
