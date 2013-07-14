from lib.utl import packet
from lib.utl import bresenham


class View(object):

    def __init__(self, level):
        """
        level -- Level object
        """
        self.set_level(level)

    def generate(self, (x0, y0), radius, eyesight, target):
        """
        x0, y0 -- int
        radius -- int
        eyesight -- int
        target -- tuple (int, int)
        """
        level = self.level.get_level()
        view_field = []
        for _ in xrange(0, radius * 2 + 1):
                line = [' ' for _ in xrange(0, radius * 2 + 1)]
                view_field.append(line)
        for y in xrange(y0 - radius, y0 + radius + 1):
            if y0 - eyesight <= y <= y0 + eyesight \
                    and len(level) >= y + 1 and y >= 0:
                for x in xrange(x0 - radius, x0 + radius + 1):
                    if (x0 - eyesight <= x <= x0 + eyesight) \
                            and len(level[y]) >= x + 1 and x >= 0:
                        line = bresenham.get_line((x0, y0), (x, y))
                        is_blocker = False
                        for (i_x, i_y) in line:
                            n_x, n_y = i_x - x0 + radius, i_y - y0 + radius
                            if not is_blocker and view_field[n_y][n_x] == ' ':
                                if target and (i_x, i_y) == target:
                                    view_field[n_y][n_x] = 'X'
                                else:
                                    view_field[n_y][n_x] = level[i_y][i_x][-1]
                            if self.level.is_view_obstructor((i_x, i_y)):
                                is_blocker = True
        for y, line in enumerate(view_field):
            view_field[y] = ''.join(line)
        return packet.encode(view_field)

    def set_level(self, level):
        """
        level -- Level object
        """
        self.level = level
