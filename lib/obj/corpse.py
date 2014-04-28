"""Player's corpse."""

from lib.obj.stationary import Stationary


class Corpse(Stationary):
    """Player's corpse."""

    def __init__(self, name):
        super(Corpse, self).__init__(
                char='%',
                name="corpse of %s" % name)
