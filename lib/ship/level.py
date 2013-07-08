class Level:

    def __init__(self, name):
        """
        name -- string, file name without extension or path
        """
        self.map_dir = 'dat/maps/space/'
        self.map_ext = '.map'
        self.level = self.load_level(name)

    def load_level(self, name):
        """
        name -- string, file

        Returns 3-dimensional list
        """
        name = self.map_dir + name + self.map_ext
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

    def is_view_obstructor(self, (x, y)):
        return False

    # def load_objects_data(self):
    #     stationary = open('dat/objects/stationary.txt', 'rb').read()
    #     self.stationary = {}
    #     for line in stationary.split('\n'):
    #         if line:
    #             symbol, id, is_blocker, view_obstr = line.split('|')
    #             self.stationary[symbol] = (id, int(is_blocker),
    #                                        int(view_obstr))
    #     items = open('dat/objects/items.txt', 'rb').read()
    #     self.items = {}
    #     for line in items.split('\n'):
    #         if line:
    #             symbol, id, is_blocker, view_obstr, stationary = \
    #                     line.split('|')
    #             self.items[symbol] = (id, int(is_blocker),
    #                                   int(view_obstr), int(stationary))
    #     mobs = open('dat/objects/mobs.txt', 'rb').read()
    #     self.mobs = {}
    #     for line in mobs.split('\n'):
    #         if line:
    #             symbol, id = line.split('|')
    #             self.mobs[symbol] = (id, )
