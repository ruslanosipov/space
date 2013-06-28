class Player:

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

    def move(self, (x, y)):
        """
        x, y -- int
        """
        self.x += x
        self.y += y

    def get_coordinates(self):
        return (self.x, self.y)

    def get_eyesight(self):
        return self.eyesight

    def set_symbol(self, symbol):
        """
        symbol -- char
        """
        self.symbol = symbol

    def get_symbol(self):
        return self.symbol

    def get_name(self):
        return self.name
