MSG_COLORS = {
    0: (100, 255, 100),
    1: (100, 100, 100),
    2: (200, 200, 200),
    3: (200, 0, 0)}
UI_COLOR = (100, 100, 100)


class UI(object):
    global MSG_COLORS
    global UI_COLOR

    def compose(self, view, colors, chat_log, prompt, evt_mode, evt_mode_desc,
                bottom_status_bar, top_status_bar, target, look_pointer):
        if evt_mode == 'pilot':
            default_colors = self.ext_colors
        else:
            default_colors = self.int_colors
        surface = []
        surface.append([[top_status_bar, UI_COLOR]])
        for y, line in enumerate(view):
            new_line = []
            for x, char in enumerate(line):
                if (x, y) in colors.keys():
                    color = colors[(x, y)]
                else:
                    color = default_colors[char]
                if (x, y) == target:
                    char = 'x'
                    color = default_colors[char]
                elif (x, y) == look_pointer:
                    char = 'l'
                    color = default_colors[char]
                if len(new_line) and new_line[-1][1] == color:
                    new_line[-1][0] += char
                else:
                    new_line.append([char, color])
            if len(chat_log) >= y + 1:
                msg, msg_type = chat_log[y]
                new_line.append([' ' + msg, MSG_COLORS[msg_type]])
            if y == len(view) - 1:
                new_line.append([' > ' + prompt, UI_COLOR])
            surface.append(new_line)
        if not len(evt_mode_desc):
            evt_mode_desc = ' ' * 24
        else:
            evt_mode_desc += (24 - len(evt_mode_desc)) * ' '
        evt_mode_desc += bottom_status_bar
        surface.append([[evt_mode_desc, UI_COLOR]])
        return surface

    def set_default_colors(self, int_colors, ext_colors):
        self.int_colors = int_colors
        self.ext_colors = ext_colors
