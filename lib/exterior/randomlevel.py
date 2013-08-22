from lib.level import Level
from lib.obj.space import Space


class RandomLevel(Level):

    #--------------------------------------------------------------------------
    # setup

    def __init__(self, size):
        self._generate(size)

    def _generate(self, size):
        level = []
        for y in xrange(0, size):
            level.append([])
            for x in xrange(0, size):
                level[y].append([Space()])
        self.level = level
