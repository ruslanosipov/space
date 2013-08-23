from lib.obj.stationary import Stationary


class Corpse(Stationary):
    """
    Player's corpse.
    """

    def __init__(self, name):
        super(Corpse, self).__init__('%', "corpse of %s" % name)
