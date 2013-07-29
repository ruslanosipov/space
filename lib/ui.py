class UI(object):

    def compose(self, view, chat_log, prompt, evt_mode, status_bar):
        """
        view -- list of strings
        chat_log -- list of strings
        prompt -- str
        evt_mode -- str
        status_bar -- str

        Returns list of strings, the "text wall" ready to be rendered
        """
        surface = []
        for i, line in enumerate(view):
            line.append(['|', (255, 255, 255)])
            if len(chat_log) >= i + 1:
                line.append([chat_log[i], (255, 255, 255)])
            if i == len(view) - 1:
                line.append(['> ' + prompt, (255, 255, 255)])
            surface.append(line)
        surface.append([['-' * 23 + '+' + '-' * 56, (255, 255, 255)]])
        if evt_mode == 'normal':
            evt_mode = ' ' * 12
        else:
            evt_mode = '-- %s --' % evt_mode[:6].upper()
        evt_mode += ' %s' % status_bar
        surface.append([[evt_mode, (255, 255, 255)]])
        return surface
