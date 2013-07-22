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
        for y in xrange(y0 - r, y0 + r + 1):
            if y0 - eyesight <= y <= y0 + eyesight:
                view.append('')
                for x in xrange(x0 - r, x0 + r + 1):
                    if x0 - eyesight <= x <= x0 + eyesight:
                        if pointer and (p, q, x, y) == pointer:
                            view[-1] += '+'
                        else:
                            obj = l.get_objects((p, q, x, y))[-1]
                            view[-1] += obj.get_char()
        for y, line in enumerate(view):
            view[y] = ''.join(line)
        return view
