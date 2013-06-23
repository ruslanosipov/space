from lib.utl import packet


class View:
    def __init__(self, level):
        self.set_level(level)

    def generate(self, (x, y), radius, eyesight):
        level = self.level.get_level()
        view_field = []
        for y_ in xrange(y - radius, y + radius + 1):
            if y - eyesight <= y_ <= y + eyesight and len(level) >= y_ + 1:
                view_field.append('')
                for x_ in xrange(x - radius, x + radius + 1):
                    if x - eyesight <= x_ <= x + eyesight \
                            and len(level[y_]) >= x_ + 1:
                        view_field[-1] += level[y_][x_][-1]
                    else:
                        view_field[-1] += ' '
            else:
                line = [' ' for i in xrange(y - radius, y + radius + 1)]
                view_field.append(''.join(line))
        return packet.encode(view_field)

    def set_level(self, level):
        self.level = level
