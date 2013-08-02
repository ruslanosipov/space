from lib.obj.mob import Mob


class Player(Mob):

    def __init__(self, name):
        """
        >>> Player('Mike')
        <class 'Player'> Mike
        """
        super(Player, self).__init__('@', name, 11)
        self.inventory = []
        self.target = None
        self.pilot = False
        self.interior = None

    def inventory_add(self, item):
        """
        >>> from lib.obj.gun import Gun
        >>> player = Player('Mike')
        >>> player.inventory_add(Gun())
        >>> player.get_inventory()
        [<class 'Gun'>]
        >>> player.inventory_add(Gun())
        >>> player.get_inventory()
        [<class 'Gun'>, <class 'Gun'>]
        """
        self.inventory.append(item)

    #--------------------------------------------------------------------------
    # accessors

    def is_pilot(self):
        return self.pilot

    def get_inventory(self):
        return self.inventory

    def get_interior(self):
        return self.interior

    def get_target(self):
        return self.target

    def set_pilot(self):
        if self.pilot:
            self.pilot = False
            self.get_interior().get_spaceship().set_pilot()
        else:
            self.pilot = True
            self.get_interior().get_spaceship().set_pilot(self)

    def set_interior(self, interior=None):
        self.interior = interior

    def set_target(self, target=None):
        self.target = target
