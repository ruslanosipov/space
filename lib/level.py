class Level:

    def __init__(self, name):
        """
        name -- string, file name without extension or path
        """
        self.map_dir = 'dat/maps/'
        self.map_ext = '.map'
        self.load_objects_data()
        self.level = self.load_level(name)

    def load_level(self, name):
        """
        name -- string, file

        Returns 3-dimensional list
        """
        name = self.map_dir + name
        level = self._load_stationary(name + '0' + self.map_ext)
        level = self._load_items(level, name + '1' + self.map_ext)
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
        stationary = open('dat/objects/stationary.txt', 'rb').read()
        self.stationary = {}
        for line in stationary.split('\n'):
            if line:
                symbol, id, is_blocker = line.split('|')
                self.stationary[symbol] = (id, int(is_blocker))
        items = open('dat/objects/items.txt', 'rb').read()
        self.items = {}
        for line in items.split('\n'):
            if line:
                symbol, id, is_blocker = line.split('|')
                self.items[symbol] = (id, int(is_blocker))

    def is_blocker(self, (x, y)):
        """
        x, y -- int
        """
        for symbol in self.level[y][x]:
            if symbol in self.stationary and self.stationary[symbol][1] or \
                    symbol in self.items and self.items[symbol][1]:
                return True
        return False

    def get_top_item(self, (x, y)):
        """
        x, y -- int
        """
        for i in xrange(1, len(self.level[y][x])):
            if self.level[y][x][- i] in self.items:
                return self.level[y][x][- i]
        return False

    def get_item_name(self, symbol):
        """
        symbol -- char
        """
        return self.items[symbol][0]

    def _load_stationary(self, name):
        """
        name -- filename with relative path and extension
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

    def _load_items(self, level, name):
        """
        level -- list of lists of lists
        name -- filename with relative path and extension
        """
        f = open(name, 'rb')
        y = 0
        while 1:
            line = f.readline()
            if len(line) == 0:
                break
            line = line[:-1]
            x = 0
            for char in line:
                if char not in self.stationary.keys():
                    level[y][x].append(char)
                x += 1
            y += 1
        return level
