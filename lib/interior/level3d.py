from lib.level import Level
from lib.obj.space import Space


class Level3D(Level):
    """
    The interior Level class.
    """

    #--------------------------------------------------------------------------
    # setup

    def __init__(self):
        self.players = []
        self.extra_tiles = {}
        self.spaceship = None

    def load_char_map(self, tiles_map, items_map, obj_defs):
        char_map = self._convert_char_map(tiles_map, items_map)
        self._load_level(char_map, obj_defs)

    def load_converted_char_map(self, char_map, obj_defs):
        self._load_level(char_map, obj_defs)

    def _convert_char_map(self, tiles_map, items_map):
        char_map = []
        for y, line in enumerate(tiles_map):
            char_map.append([])
            for x, tile in enumerate(line):
                char_map[y].append([tile])
                if items_map[y][x] != tile:
                    char_map[y][x].append(items_map[y][x])
        return char_map

    #--------------------------------------------------------------------------
    # bulk object accessors

    def get_nearest_mobs_coords(self, (x0, y0), eyesight):
        """
        >>> o = {'.': 'Floor'}
        >>> l = [[['.'], ['.']], [['.'], ['.']], [['.'], ['.']]]
        >>> level = Level3D()
        >>> level.load_converted_char_map(l, o)
        >>> from lib.obj.player import Player
        >>> mike = Player('Mike')
        >>> josh = Player('Josh')
        >>> level.add_object((0, 1), mike)
        >>> level.add_object((1, 2), josh)
        >>> level.get_nearest_mobs_coords((0, 0), 2)
        ((0, 1), (1, 2))

        Returns list of coordinates, nearest first
        """
        mobs = []
        for y in xrange(y0 - eyesight, y0 + eyesight + 1):
            if self.get_height() >= y + 1 and y >= 0:
                for x in xrange(x0 - eyesight, x0 + eyesight + 1):
                    if self.get_width(y) >= x + 1 and x >= 0:
                            if x == x0 and y == y0:
                                continue
                            if self.get_player((x, y)):
                                mobs.append((x, y))
        if len(mobs):
            diff = [abs(x - x0) + abs(y - y0) for (x, y) in mobs]
            mobs = zip(diff, mobs)
            mobs.sort()
            _, mobs = zip(*mobs)
        return mobs

    def get_player(self, (x, y)):
        """
        >>> level = Level3D()
        >>> level.load_converted_char_map([[['.'], ['.']]], {'.': 'Floor'})
        >>> from lib.obj.player import Player
        >>> mike = Player('Mike')
        >>> level.add_object((0, 0), mike)
        >>> level.get_player((0, 0))
        <class 'Player'> Mike
        >>> level.get_player((7, 9))
        False
        >>> level.get_player((1, 0))
        False
        """
        if not 0 <= y < self.get_height() or not 0 <= x < self.get_width(y):
            return False
        for obj in self.level[y][x]:
            if obj.__class__.__name__ == 'Player':
                return obj
        return False

    #--------------------------------------------------------------------------
    # object operations

    def add_player(self, (x, y), player):
        self.players.append(player)
        self.add_object((x, y), player)

    def add_object(self, (x, y), obj):
        if super(Level3D, self).add_object((x, y), obj) is not False:
            obj.set_coords((x, y))
            obj.set_interior(self)

    def remove_player(self, player):
        self.players.remove(player)
        self.remove_object(player.get_coords(), player)

    #--------------------------------------------------------------------------
    # bulk object accessors

    def get_objects(self, (x, y)):
        """
        >>> level = Level3D()
        >>> level.load_converted_char_map([[['.', '+']]],
        ...                               {'.': 'Floor', '+': 'Door'})
        >>> level.get_objects((0, 0))
        [<class 'Floor'>, <class 'Door'>]
        >>> level.get_objects((7, 9))
        [<class 'Space'>]
        """
        if not 0 <= y < self.get_height() or not 0 <= x < self.get_width(y):
            if (x, y) not in self.extra_tiles.keys():
                self.extra_tiles[(x, y)] = Space()
            return [self.extra_tiles[(x, y)]]
        if len(self.level[y][x]):
            return self.level[y][x]
        return False

    #--------------------------------------------------------------------------
    # accessors

    def get_players(self):
        return self.players

    def get_spaceship(self):
        return self.spaceship

    def set_spaceship(self, spaceship):
        self.spaceship = spaceship
