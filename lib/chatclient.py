"""Receives, cuts and displays chat log."""

class ChatClient(object):
    """Receives, cuts and displays chat log."""

    def __init__(self):
        self.log = []
        self.width = 56

    def get_log(self, size=22):
        if len(self.log) <= size:
            log = self.log
        else:
            log = self.log[len(self.log) - size:]
        formatted_log = []
        for msg, msg_type in log:
            if len(msg) <= self.width:
                formatted_log.append((msg, msg_type))
            else:
                chunk, w = len(msg), self.width
                formatted_log += \
                    [(msg[i:i + w], msg_type) for i in xrange(0, chunk, w)]
        if len(formatted_log) <= size:
            return formatted_log
        return formatted_log[len(formatted_log) - size:]

    def add_multiple(self, msgs):
        if len(self.log) > 1000:
            # TODO: save in a text file
            self.log = self.log[len(self.log) - 100:]
        self.log += msgs
