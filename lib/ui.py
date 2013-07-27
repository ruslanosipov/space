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
            line += '|'
            if len(chat_log) >= i + 1:
                line += chat_log[i]
            if i == len(view) - 1:
                line += '> ' + prompt
            surface.append(line)
        surface.append('-' * 23 + '+' + '-' * 56)
        if evt_mode == 'normal':
            evt_mode = ' ' * 12
        else:
            evt_mode = '-- %s --' % evt_mode[:6].upper()
        evt_mode += ' %s' % status_bar
        surface.append(evt_mode)
        return surface
