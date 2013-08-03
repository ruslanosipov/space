class Tile(object):

    def __init__(self, char, name, block_path=False, block_view=False):
        """
        >>> Tile('#', 'wall', True, True)
        <class 'Tile'>
        """
        self.char = char
        self.name = name
        self.block_path = block_path
        self.block_view = block_view
        self.pickupable = False
        self.moveable = False
        self.interior = None
        self.coords = None
        self.default_color = True

    def __repr__(self):
        return "<class '%s'>" % self.__class__.__name__

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    #--------------------------------------------------------------------------
    # accessors

    def get_char(self):
        return self.char

    def get_color(self):
        return self.color

    def get_coords(self):
        return self.coords

    def get_interior(self):
        return self.interior

    def get_name(self):
        return self.name

    def is_default_color(self):
        return self.default_color

    def is_moveable(self):
        return self.moveable

    def is_path_blocker(self):
        return self.block_path

    def is_pickupable(self):
        return self.pickupable

    def is_view_blocker(self):
        return self.block_view

    def set_color(self, color):
        self.default_color = False
        self.color = color

    def set_coords(self, coords):
        self.coords = coords

    def set_interior(self, interior):
        self.interior = interior
