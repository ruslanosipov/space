class View(object):

    #--------------------------------------------------------------------------
    # setup

    def __init__(self, level):
        self._set_level(level)

    def __repr__(self):
        return "<class '%s'>" % (self.__class__.__name__)

    #--------------------------------------------------------------------------
    # accessors

    def _set_level(self, level):
        self.level = level
