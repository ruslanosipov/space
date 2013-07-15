class Level(object):

    def get_level(self):
        """
        Returns list of lists
        """
        return self.level

    def add_object(self, symbol, (x, y)):
        """
        symbol -- char
        x, y -- int
        """
        self.level[y][x].append(symbol)

    def remove_object(self, symbol, (x, y)):
        """
        symbol -- chat
        x, y -- int
        """
        del self.level[y][x][self.level[y][x].index(symbol)]

    def get_top_object(self, (x, y)):
        if len(self.level[y][x]):
            return self.level[y][x][-1]
        return False

    def get_width(self, y):
        if y >= len(self.level):
            return False
        return len(self.level[y])

    def get_height(self):
        return len(self.level)
