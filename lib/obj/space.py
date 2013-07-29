import random
from lib.obj.tile import Tile


class Space(Tile):

    def __init__(self):
        """
        >>> Space()
        <class 'Space'>
        """
        stars = ['.', ',']
        char = random.choice(stars) if random.randint(0, 50) == 0 else ' '
        super(Space, self).__init__(char, 'space')
        colors = [
            (255, 255, 255),
            (255, 255, 122),
            (0, 255, 255)]
        self.set_color(random.choice(colors))
