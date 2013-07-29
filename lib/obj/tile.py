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
        self.color = (255, 255, 255)

    def __repr__(self):
        return "<class '%s'>" % self.__class__.__name__

    #--------------------------------------------------------------------------
    # accessors

    def get_char(self):
        return self.char

    def get_coords(self):
        return self.coords

    def get_color(self):
        return self.color

    def get_interior(self):
        return self.interior

    def get_name(self):
        return self.name

    def is_moveable(self):
        return self.moveable

    def is_path_blocker(self):
        return self.block_path

    def is_pickupable(self):
        return self.pickupable

    def is_view_blocker(self):
        return self.block_view

    def set_coords(self, coords):
        self.coords = coords

    def set_color(self, color):
        self.color = color

    def set_interior(self, interior):
        self.interior = interior
