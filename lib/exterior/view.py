from lib.view import View


class ExteriorView(View):

    #--------------------------------------------------------------------------
    # generate

    def generate(self, (p, q, x0, y0), r, eyesight, pointer=None):
        """
        Generate exterior view.
        """
        l = self.level
        view = []
        for y in xrange(y0 - r, y0 + r + 1):
            if y0 - eyesight <= y <= y0 + eyesight:
                view.append([])
                for x in xrange(x0 - r, x0 + r + 1):
                    if x0 - eyesight <= x <= x0 + eyesight:
                        if pointer and (p, q, x, y) == pointer:
                            char, color = '+', (255, 255, 255)
                        else:
                            obj = l.get_objects((p, q, x, y))[-1]
                            char = obj.get_char()
                            color = obj.get_color()
                        if len(view[-1]) and view[-1][-1][1] == color:
                            view[-1][-1][0] += char
                        else:
                            view[-1].append([char, color])
        return view
