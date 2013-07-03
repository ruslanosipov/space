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
                symbol, id, is_blocker, view_obstr = line.split('|')
                self.stationary[symbol] = (id, int(is_blocker),
                                           int(view_obstr))
        items = open('dat/objects/items.txt', 'rb').read()
        self.items = {}
        for line in items.split('\n'):
            if line:
                symbol, id, is_blocker, view_obstr, stationary = \
                        line.split('|')
                self.items[symbol] = (id, int(is_blocker),
                                      int(view_obstr), int(stationary))
        mobs = open('dat/objects/mobs.txt', 'rb').read()
        self.mobs = {}
        for line in mobs.split('\n'):
            if line:
                symbol, id = line.split('|')
                self.mobs[symbol] = (id, )

    def is_blocker(self, (x, y)):
        """
        x, y -- int
        """
        for symbol in self.level[y][x]:
            if symbol in self.stationary and self.stationary[symbol][1] or \
                    symbol in self.items and self.items[symbol][1] or \
                    symbol in self.mobs:
                return True
        return False

    def is_view_obstructor(self, (x, y)):
        """
        x, y -- int
        """
        for symbol in self.level[y][x]:
            if symbol in self.stationary and self.stationary[symbol][2] or \
                    symbol in self.items and self.items[symbol][2]:
                return True
        return False

    def can_be_picked_up(self, symbol):
        """
        symbol -- char
        """
        if symbol in self.items.keys() and not self.items[symbol][3]:
            return True
        return False


    def get_top_item(self, (x, y)):
        """
        x, y -- int
        """
        for i in xrange(1, len(self.level[y][x])):
            i = - i
            if self.level[y][x][i] in self.items:
                return self.level[y][x][i]
        return False

    def get_object_ids(self, (x, y)):
        """
        x, y -- int

        Returns list of object IDs
        """
        names = []
        for obj in self.level[y][x]:
            if obj in self.stationary.keys():
                names.append(self.stationary[obj][0])
            if obj in self.items:
                names.append(self.items[obj][0])
            if obj in self.mobs:
                names.append(self.mobs[obj][0])
        return names

    def get_mob(self, (x, y)):
        """
        x, y -- int
        """
        for obj in self.level[y][x]:
            if obj in self.mobs.keys():
                return self.mobs[obj]
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
