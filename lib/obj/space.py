import random
from lib.obj.tile import Tile


class Space(Tile):

    def __init__(self):
        stars = ['.', ',']
        char = random.choice(stars) if random.randint(0, 50) == 0 else ' '
        super(Space, self).__init__(char, 'space')
        if char == '.':
            self.set_color((255, 255, 255))
