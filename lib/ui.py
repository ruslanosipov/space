MSG_COLORS = {
    0: (100, 255, 100),
    1: (100, 100, 100),
    2: (200, 200, 200)}


class UI(object):
    global MSG_COLORS

    def compose(self, view, colors, chat_log, prompt, evt_mode, status_bar):
        if evt_mode == 'pilot':
            default_colors = self.ext_colors
        else:
            default_colors = self.int_colors
        surface = []
        for y, line in enumerate(view):
            new_line = []
            for x, char in enumerate(line):
                if (x, y) in colors.keys():
                    color = colors[(x, y)]
                else:
                    color = default_colors[char]
                if len(new_line) and new_line[-1][1] == color:
                    new_line[-1][0] += char
                else:
                    new_line.append([char, color])
            new_line.append(['|', (0, 255, 255)])
            if len(chat_log) >= y + 1:
                msg, msg_type = chat_log[y]
                new_line.append([msg, MSG_COLORS[msg_type]])
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

    def set_default_colors(self, int_colors, ext_colors):
        self.int_colors = int_colors
        self.ext_colors = ext_colors
