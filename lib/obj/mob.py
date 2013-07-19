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

    def get_char(self):
        return self.char

    def get_name(self):
        return self.name

    def get_sight(self):
        return self.sight
