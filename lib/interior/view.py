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
        [[['...', (120, 120, 120)]], [['...', (120, 120, 120)]], \
[['...', (120, 120, 120)]]]
        """
        l = self.level
        view = []
        for y in xrange(y0 - r, y0 + r + 1):
            view.append([])
            if y0 - eyesight <= y <= y0 + eyesight:
                for x in xrange(x0 - r, x0 + r + 1):
                    if (x0 - eyesight <= x <= x0 + eyesight):
                        if pointer and (x, y) == pointer:
                            char, color = 'x', (255, 255, 255)
                        else:
                            obj = l.get_objects((x, y))[-1]
                            char = obj.get_char()
                            color = obj.get_color()
                        if len(view[-1]) and view[-1][-1][1] == color:
                            view[-1][-1][0] += char
                        else:
                            view[-1].append([char, color])
        return view
