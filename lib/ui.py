class UI:

    def __init__(self):
        pass

    def compose(self, view, chat_log):
        """
        view -- list of strings
        chat_log -- list of strings

        Returns list of strings, the "text wall" ready to be rendered
        """
        surface = []
        for i, line in enumerate(view):
            line += '|'
            if len(chat_log) >= i + 1:
                line += chat_log[i]
            surface.append(line)
        return surface
