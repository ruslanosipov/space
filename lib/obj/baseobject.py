"""Parent for every game object."""

class BaseObject(object):
    """Parent for every game object."""

    def __init__(self):
        self._color = None
        self.is_default_color = True

    def __repr__(self):
        return "<class '%s'>" % self.__class__.__name__

    #--------------------------------------------------------------------------
    # Accessors

    @property
    def color(self):
        """Get non-default object color."""
        return self._color

    @color.setter
    def color(self, color):
        """Override default object color."""
        self.is_default_color = False
        self._color = color
