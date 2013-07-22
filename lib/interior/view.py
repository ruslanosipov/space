from lib.view import View
from lib.utl import bresenham


class InteriorView(View):

    #--------------------------------------------------------------------------
    # generate

    def generate(self, (x0, y0), r, eyesight, pointer=None):
        """
        >>> from lib.interior.level3d import Level3D
        >>> c = ['.']
        >>> l = [[c, c, c], [c, c, c], [c, c, c]]
        >>> level = Level3D(l, {'.': 'Floor'})
        >>> view = InteriorView(level)
        >>> view.generate((1, 1), 1, 1)
        ['...', '...', '...']
        """
        l = self.level
        view = []
        for _ in xrange(0, r * 2 + 1):
                line = [' ' for _ in xrange(0, r * 2 + 1)]
                view.append(line)
        for y in xrange(y0 - r, y0 + r + 1):
            if y0 - eyesight <= y <= y0 + eyesight \
                    and l.get_height() >= y + 1 and y >= 0:
                for x in xrange(x0 - r, x0 + r + 1):
                    if (x0 - eyesight <= x <= x0 + eyesight) \
                            and l.get_width(y) >= x + 1 and x >= 0:
                        line = bresenham.get_line((x0, y0), (x, y))
                        is_blocker = False
                        for (ix, iy) in line:
                            nx, ny = ix - x0 + r, iy - y0 + r
                            if not is_blocker and view[ny][nx] == ' ':
                                if pointer and (ix, iy) == pointer:
                                    view[ny][nx] = 'x'
                                else:
                                    obj = l.get_objects((ix, iy))[-1]
                                    view[ny][nx] = obj.get_char()
                            if l.is_view_blocker((ix, iy)):
                                is_blocker = True
        for y, line in enumerate(view):
            view[y] = ''.join(line)
        return view
