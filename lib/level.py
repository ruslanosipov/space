class Level:
    def __init__(self, name):
        """
        name -- string, file
        """
        self.level = self.readfile(name)

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
