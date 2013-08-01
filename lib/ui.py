class UI(object):

    def compose(self, view, colors, chat_log, prompt, evt_mode, status_bar):
        surface = []
        for y, line in enumerate(view):
            new_line = []
            for x, char in enumerate(line):
                if (x, y) in colors.keys():
                    color = colors[(x, y)]
                else:
                    color = self.default_colors[char]
                if len(new_line) and new_line[-1][1] == color:
                    new_line[-1][0] += char
                else:
                    new_line.append([char, color])
            new_line.append(['|', (0, 255, 255)])
            if len(chat_log) >= y + 1:
                new_line.append([chat_log[y], (255, 255, 255)])
            if y == len(view) - 1:
                new_line.append(['> ' + prompt, (255, 255, 255)])
            surface.append(new_line)
        surface.append([['-' * 23 + '+' + '-' * 56, (0, 255, 255)]])
        if evt_mode == 'normal':
            evt_mode = ' ' * 12
        else:
            evt_mode = '-- %s --' % evt_mode[:6].upper()
        evt_mode += ' %s' % status_bar
        surface.append([[evt_mode, (0, 255, 255)]])
        return surface

    def set_default_colors(self, colors):
        self.default_colors = colors
