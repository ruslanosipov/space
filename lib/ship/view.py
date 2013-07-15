from lib.view import View
from lib.utl import packet
from lib.utl import bresenham


class ShipView(View):

    def generate(self, (p0, q0, x0, y0), radius, eyesight, target):
        l = self.level
        view_field = []
        for _ in xrange(0, radius * 2 + 1):
                line = [' ' for _ in xrange(0, radius * 2 + 1)]
                view_field.append(line)
        for y in xrange(y0 - radius, y0 + radius + 1):
            if y0 - eyesight <= y <= y0 + eyesight:
                for x in xrange(x0 - radius, x0 + radius + 1):
                    if (x0 - eyesight <= x <= x0 + eyesight):
                        line = bresenham.get_line((x0, y0), (x, y))
                        for (i_x, i_y) in line:
                            n_x, n_y = i_x - x0 + radius, i_y - y0 + radius
                            if target and (p0, q0, i_x, i_y) == target:
                                view_field[n_y][n_x] = 'X'
                            else:
                                view_field[n_y][n_x] = \
                                        l.get_top_object((p0, q0, i_x, i_y))
        for y, line in enumerate(view_field):
            view_field[y] = ''.join(line)
        return packet.encode(view_field)
