from lib.obj.tile import Tile


class Stationary(Tile):
    """
    Base class for immobile objects (not exactly tiles though, these
    guys can be activated). All stationary objects inherit from it.
    """

    def __init__(self, *args, **kwargs):
        super(Stationary, self).__init__(*args, **kwargs)
        self.pickupable = False
        self.moveable = False

    def activate(self):
        msg = "You activate the %s, nothing happens..." % self.name
        return msg
