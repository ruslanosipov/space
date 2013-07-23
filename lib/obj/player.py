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
        self.spaceship = None
        self.pilot = False

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

    def get_spaceship(self):
        return self.spaceship

    def get_target(self):
        return self.target

    def set_pilot(self):
        self.pilot = False if self.pilot else True

    def set_spaceship(self, spaceship=None):
        self.spaceship = spaceship

    def set_target(self, target=None):
        self.target = target
