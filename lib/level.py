class Level:

    def __init__(self, name):
        """
        name -- string, file
        """
        self.level = self.readfile(name)
        self.load_objects_data()

    def readfile(self, name):
        """
        name -- string, file

        Returns list of lists
        """
        f = open(name, 'rb')
        level = []
        length = 0
        while 1:
            line = f.readline()
            if len(line) == 0:
                break
            if len(line) > length:
                length = len(line)
            line = line[:-1]
            level.append([])
            for char in line:
                level[-1].append([char])
        for y, line in enumerate(level):
            if len(line) < length:
                appendix = [[' '] for i in xrange(0, length - len(line) + 1)]
                level[y] = line + appendix
        return level

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

    def load_objects_data(self):
        stationary = open('dat/objects/stationary.txt', 'r').read()
        self.stationary = {}
        for line in stationary.split('\n'):
            if line:
                symbol, id, is_blocker = line.split('|')
                self.stationary[symbol] = (id, int(is_blocker))

    def is_blocker(self, (x, y)):
        """
        x, y -- int
        """
        for symbol in self.level[y][x]:
            if self.stationary[symbol][1]:
                return True
        return False
