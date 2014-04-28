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

    def load_char_map(self, tiles_map, items_map, obj_defs, extras={}):
        char_map = self._convert_char_map(tiles_map, items_map)
        self._load_level(char_map, obj_defs, extras)

    def load_converted_char_map(self, char_map, obj_defs, extras={}):
        self._load_level(char_map, obj_defs, extras)

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

    def get_nearest_players_coords(self, (x0, y0), eyesight, visible):
        """
        Returns list of coordinates, nearest first
        """
        players = []
        for y in xrange(y0 - eyesight, y0 + eyesight + 1):
            if self.get_height() >= y + 1 and y >= 0:
                for x in xrange(x0 - eyesight, x0 + eyesight + 1):
                    if self.get_width(y) >= x + 1 and x >= 0:
                            if x == x0 and y == y0:
                                continue
                            if (x, y) in visible and self.get_player((x, y)):
                                players.append((x, y))
        if len(players):
            diff = [abs(x - x0) + abs(y - y0) for (x, y) in players]
            players = zip(diff, players)
            players.sort()
            _, players = zip(*players)
        return list(players)

    def get_player(self, (x, y)):
        if not 0 <= y < self.get_height() or not 0 <= x < self.get_width(y):
            raise IndexError("coordinates can not be outside the level")
        for obj in self.level[y][x]:
            if obj.__class__.__name__ == 'Player':
                return obj
        return False

    #--------------------------------------------------------------------------
    # object operations

    def add_player(self, (x, y), player):
        self.add_object((x, y), player)
        self.players.append(player)

    def add_object(self, (x, y), obj, position=0):
        if super(Level3D, self).add_object((x, y), obj, position) is not False:
            obj.coords = (x, y)
            obj.interior = self

    def remove_player(self, player):
        self.remove_object(player.coords, player)
        self.players.remove(player)

    #--------------------------------------------------------------------------
    # bulk object accessors

    def get_objects(self, (x, y)):
        if not 0 <= y < self.get_height() or not 0 <= x < self.get_width(y):
            if (x, y) not in self.extra_tiles.keys():
                self.extra_tiles[(x, y)] = Space()
            return [self.extra_tiles[(x, y)]]
        return self.level[y][x]
