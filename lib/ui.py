class UI:
    def __init__(self):
        pass

    def compose(self, view, chat_log):
        surface = []
        for i, line in enumerate(view):
            line += '|'
            if len(chat_log) >= i + 1:
                line += chat_log[i]
            surface.append(line)
        return surface
