from lib.level import Level
from lib.obj.space import Space


class RandomLevel(Level):

    #--------------------------------------------------------------------------
    # setup

    def __init__(self, size):
        """
        >>> level = RandomLevel(3)
        >>> level
        <class 'RandomLevel'>
        >>> level.get_height()
        3
        >>> level.get_width(0)
        3
        """
        self._generate(size)

    def _generate(self, size):
        level = []
        for y in xrange(0, size):
            level.append([])
            for x in xrange(0, size):
                level[y].append([Space()])
        self.level = level
