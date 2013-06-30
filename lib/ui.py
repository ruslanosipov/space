class UI:

    def __init__(self):
        pass

    def compose(self, view, chat_log, prompt):
        """
        view -- list of strings
        chat_log -- list of strings
        prompt -- str

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
        return surface
