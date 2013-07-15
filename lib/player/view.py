from lib.view import View


class PlayerView(View):

    def get_visible_players(self, (x0, y0), eyesight):
        """
        x0, y0 -- int
        eyesight -- int

        Returns list of coordinates, nearest first
        """
        level = self.level.get_level()
        mobs = []
        for y in xrange(y0 - eyesight, y0 + eyesight + 1):
            if len(level) >= y + 1 and y >= 0:
                for x in xrange(x0 - eyesight, x0 + eyesight + 1):
                    if len(level[y]) >= x + 1 and x >= 0 and \
                            not (x == x0 and y == y0) and \
                            self.level.get_mob((x, y)):
                        mobs.append((x, y))
        if len(mobs):
            diffs = [abs(x - x0) + abs(y - y0) for (x, y) in mobs]
            mobs = zip(diffs, mobs)
            mobs.sort()
            _, mobs = zip(*mobs)
        return mobs
