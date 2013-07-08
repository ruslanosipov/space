class ItemTemplate:

    def __init__(self, symbol):
        """
        symbol -- char
        """
        self.symbol = symbol

    def activate(self):
        """
        Interface method
        """
        pass

    def get_symbol(self):
        return self.symbol
