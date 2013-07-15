from lib.ship.level import ShipLevel


class LevelsMap(object):

    def _validate(func):

        def wrapper(self, (p, q, x, y), symbol=None):
            if symbol is not None:
                symbol = self._validate_symbol(symbol)
            p, q, x, y = self._validate_coordinates(p, q, x, y)
            if symbol is not None:
                return func(self, (p, q, x, y), symbol)
            return func(self, (p, q, x, y))

        return wrapper

    def __init__(self):
        self.levels = {}
        self.populate_area((0, 0))

    def populate_area(self, (x0, y0)):
        for y in xrange(y0 - 1, y0 + 2):
            for x in xrange(x0 - 1, x0 + 2):
                if (x, y) not in self.levels.keys():
                    self.levels[(x, y)] = ShipLevel(25)

    @_validate
    def add_object(self, (p, q, x, y), symbol):
        return self.levels[(p, q)].add_object(symbol, (x, y))

    @_validate
    def remove_object(self, (p, q, x, y), symbol):
        return self.levels[(p, q)].remove_object(symbol, (x, y))

    @_validate
    def get_top_object(self, (p, q, x, y)):
        return self.levels[(p, q)].get_top_object((x, y))

    def archive_unused_areas(self):
        # TODO: implement
        pass

    def _validate_symbol(self, symbol):
        # TODO: add validator
        return symbol

    def _validate_coordinates(self, p, q, x, y):
        while True:
            if (p, q) in self.levels.keys():
                if x < 0:
                    x += self.levels[(p, q)].get_width(0)
                    p -= 1
                elif y < 0:
                    y += self.levels[(p, q)].get_height()
                    q -= 1
                elif x >= self.levels[(p, q)].get_width(0):
                    x -= self.levels[(p, q)].get_width(0)
                    p += 1
                elif y >= self.levels[(p, q)].get_height():
                    y -= self.levels[(p, q)].get_height()
                    q += 1
                else:
                    break
            else:
                self.levels[(p, q)] = ShipLevel(25)
        return p, q, x, y
