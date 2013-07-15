from lib.level import Level
import random


class ShipLevel(Level):

    def __init__(self, size):
        """
        size -- int
        """
        self.level = self.generate(size)

    def generate(self, size):
        level = []
        for y in xrange(0, size):
            level.append([])
            for x in xrange(0, size):
                dice = random.randint(0, 10)
                level[y].append(['.'] if dice == 0 else [' '])
        return level

    def is_view_obstructor(self, (x, y)):
        return False
