from lib.view import View


class ExteriorView(View):

    #--------------------------------------------------------------------------
    # generate

    def generate(self, (p, q, x0, y0), r, sight, pointer=None):
        l = self.level
        view, colors = [], {}
        for _ in xrange(0, r * 2 + 1):
                line = [' ' for _ in xrange(0, r * 2 + 1)]
                view.append(line)
        ny = 0
        for y in xrange(y0 - r, y0 + r + 1):
            nx = 0
            if y0 - sight <= y <= y0 + sight:
                for x in xrange(x0 - r, x0 + r + 1):
                    if (x0 - sight <= x <= x0 + sight):
                        if pointer and (p, q, x, y) == pointer:
                            view[ny][nx] = '+'
                        else:
                            obj = l.get_objects((p, q, x, y))[-1]
                            view[ny][nx] = obj.get_char()
                            if not obj.is_default_color():
                                colors[(nx, ny)] = obj.get_color()
                    nx += 1
            ny += 1
        for y, line in enumerate(view):
            view[y] = ''.join(line)
        return view, colors
