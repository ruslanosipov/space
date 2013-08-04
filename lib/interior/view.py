from lib.view import View
from lib.utl import bresenham


class InteriorView(View):

    #--------------------------------------------------------------------------
    # generate

    def generate(self, (x0, y0), r, sight, visible_tiles,
                 pointer=None, look=None):
        l = self.level
        view, colors = [], {}
        for _ in xrange(0, r * 2 + 1):
                line = [' ' for _ in xrange(0, r * 2 + 1)]
                view.append(line)
        for y in xrange(y0 - r, y0 + r + 1):
            if y0 - sight <= y <= y0 + sight:
                for x in xrange(x0 - r, x0 + r + 1):
                    if (x0 - sight <= x <= x0 + sight):
                        nx, ny = x - x0 + r, y - y0 + r
                        if pointer and (x, y) == pointer:
                            view[ny][nx] = 'x'
                        if look and (x, y) == look:
                            view[ny][nx] = 'l'
                        elif (x, y) in visible_tiles:
                            obj = l.get_objects((x, y))[-1]
                            view[ny][nx] = obj.get_char()
                            if not obj.is_default_color():
                                colors[(nx, ny)] = obj.get_color()
        for y, line in enumerate(view):
            view[y] = ''.join(line)
        return view, colors

    def visible_tiles(self, (x0, y0), r, sight):
        l = self.level
        visible = []
        for y in xrange(y0 - r, y0 + r + 1):
            if y0 - sight <= y <= y0 + sight:
                for x in xrange(x0 - r, x0 + r + 1):
                    if (x0 - sight <= x <= x0 + sight):
                        line = bresenham.get_line((x0, y0), (x, y))
                        is_blocker = False
                        for (ix, iy) in line:
                            if not is_blocker and (ix, iy) not in visible:
                                visible.append((ix, iy))
                            if l.is_view_blocker((ix, iy)):
                                is_blocker = True
        return visible
