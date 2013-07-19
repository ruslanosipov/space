from lib.obj.mob import Mob


class Player(Mob):

    def __init__(self, name):
        """
        >>> Player('Mike')
        <class 'Player'> Mike
        """
        super(Player, self).__init__('@', name, 11)
        self.inventory = []

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

    def set_pointer(self, pointer):
        self.pointer = pointer

    #--------------------------------------------------------------------------
    # accessors

    def get_inventory(self):
        return self.inventory

    def get_pointer(self):
        return self.pointers
