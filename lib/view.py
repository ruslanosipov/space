class View(object):

    #--------------------------------------------------------------------------
    # setup

    def __init__(self, level):
        """
        >>> from lib.level import Level
        >>> level = Level([[['.']]], {'.': 'Floor'})
        >>> View(level)
        <class 'View'>

        level -- Level object
        """
        self._set_level(level)

    def __repr__(self):
        return "<class '%s'>" % (self.__class__.__name__)

    def _set_level(self, level):
        """
        level -- Level object
        """
        self.level = level
