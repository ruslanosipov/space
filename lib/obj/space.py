import random
from lib.obj.tile import Tile


class Space(Tile):

    def __init__(self):
        """
        >>> Space()
        <class 'Space'>
        """
        stars = ['.', ',']
        char = ' ' if random.randint(0, 10) == 0 else random.choice(stars)
        super(Space, self).__init__(char, 'space')
