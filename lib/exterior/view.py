from lib.view import View
from lib.utl import bresenham


class ExteriorView(View):

    #--------------------------------------------------------------------------
    # generate

    def generate(self, (p, q, x0, y0), r, eyesight, pointer=None):
        """
        >>> from lib.exterior.level5d import Level5D
        >>> level = Level5D()
        >>> view = ExteriorView(level)
        >>> field = view.generate((0, 0, 0, 0), 1, 1)
        >>> import re
        >>> re.compile(r'.{9}').search(''.join(field)) is not None
        True
        """
        l = self.level
        view = []
        for _ in xrange(0, r * 2 + 1):
                line = [' ' for _ in xrange(0, r * 2 + 1)]
                view.append(line)
        for y in xrange(y0 - r, y0 + r + 1):
            if y0 - eyesight <= y <= y0 + eyesight:
                for x in xrange(x0 - r, x0 + r + 1):
                    if (x0 - eyesight <= x <= x0 + eyesight):
                        line = bresenham.get_line((x0, y0), (x, y))
                        for (ix, iy) in line:
                            nx, ny = ix - x0 + r, iy - y0 + r
                            if pointer and (p, q, ix, iy) == pointer:
                                view[ny][nx] = '+'
                            else:
                                obj = l.get_objects((p, q, ix, iy))[-1]
                                view[ny][nx] = obj.get_char()
        for y, line in enumerate(view):
            view[y] = ''.join(line)
        return view
