class Mob(object):

    def __init__(self, char, name, sight=11):
        """
        >>> Mob('@', 'Mike')
        <class 'Mob'> Mike
        """
        self.char = char
        self.name = name
        self.sight = sight
        self.alive = True
        self.health = self.health_max = 100
        self.coords = (0, 0)
        self.level = None
        self.default_color = True

    def __repr__(self):
        return "<class '%s'> %s" % (self.__class__.__name__, self.name)

    def receive_damage(self, damage):
        """
        >>> mob = Mob('@', 'Mike')
        >>> mob.receive_damage(50)
        >>> mob.is_alive()
        True
        >>> mob.receive_damage(90)
        >>> mob.is_alive()
        False
        """
        self.health -= damage
        if self.health <= 0:
            self.alive = False

    #--------------------------------------------------------------------------
    # accessors

    def is_alive(self):
        return self.alive

    def is_default_color(self):
        return self.default_color

    def is_path_blocker(self):
        return True

    def is_view_blocker(self):
        return False

    def get_char(self):
        return self.char

    def get_color(self):
        return self.color

    def get_coords(self):
        return self.coords

    def get_level(self):
        return self.level

    def get_name(self):
        return self.name

    def get_sight(self):
        return self.sight

    def set_color(self, color):
        self.default_color = False
        self.color = color

    def set_coords(self, (x, y)):
        self.coords = (x, y)

    def set_level(self, level):
        self.level = level
