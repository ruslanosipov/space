class Player(object):

    def __init__(self, (x, y), name, symbol, eyesight=11):
        """
        x, y -- int
        name -- str
        symbol -- char
        eyesight -- int
        """
        self.x, self.y = x, y
        self.eyesight = eyesight
        self.name = name
        self.set_symbol(symbol)
        self.health_max = self.health = 100
        self.alive = 1
        self.mode = 'attack'
        self.target = None
        self.under_target = 0
        self.inventory = {}
        self.set_game_mode('player')

    def move(self, (x, y)):
        """
        x, y -- int
        """
        self.x += x
        self.y += y
        if self.under_target:
            self.under_target.set_target((self.x, self.y))

    def validate_movement(self, (x, y)):
        """
        Movement is allowed only in 4 directions.

        >>> player = Player((9, 9), 'foo', '@')
        >>> player.validate_movement((-1, 0))
        True
        >>> player.validate_movement((1, 1))
        False

        x, y -- int
        """
        if x == 0 and (y == 1 or y == -1) or \
                y == 0 and (x == 1 or x == -1):
            return True
        return False

    def take_damage(self, x):
        """
        x -- int

        Take x points of damage
        """
        self.health -= x
        if self.health <= 0:
            self.alive = 0

    def is_alive(self):
        return self.alive

    def become_target(self, player):
        """
        player -- Player obj, become target of...
        """
        self.under_target = player

    def add_to_inventory(self, (item_id, quantity)):
        if item_id in self.inventory:
            self.inventory[item_id] += quantity
        else:
            self.inventory[item_id] = quantity

    #--------------------------------------------------------------------------
    # getters and setters

    def get_coordinates(self):
        return (self.x, self.y)

    def get_eyesight(self):
        return self.eyesight

    def get_game_mode(self):
        return self.game_mode

    def get_inventory(self):
        return self.inventory

    def get_mode(self):
        return self.mode

    def get_name(self):
        return self.name

    def get_symbol(self):
        return self.symbol

    def get_target(self):
        return self.target

    def set_game_mode(self, game_mode):
        """
        game_mode -- str; foot or ship
        """
        self.game_mode = game_mode

    def set_mode(self, mode):
        """
        mode -- str
        """
        self.mode = mode

    def set_symbol(self, symbol):
        """
        symbol -- char
        """
        self.symbol = symbol

    def set_target(self, coord):
        """
        coord -- tuple (int, int) or None
        """
        self.target = coord
