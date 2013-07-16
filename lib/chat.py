class ChatServer(object):
    """
    Manages and sends out chat messages for players.
    """

    def __init__(self):
        self.log = [(0, 'all', 'Welcome to Space, the game in space!')]
        self.recipients = {}

    def get_recent(self, recipient):
        """
        Returns list of latest chat messages

        >>> chat = ChatServer()
        >>> chat.add_single('foo', 'bar')
        >>> chat.get_recent('foo')[-1]
        'bar'

        recipient -- str, who reads the log
        """
        log = []
        if recipient not in self.recipients:
            self.recipients[recipient] = -1
        for item in self.log:
            if item[0] > self.recipients[recipient] and \
                    item[1] in ['all', recipient]:
                log.append(item[2])
                self.recipients[recipient] = item[0]
        return log

    def add_single(self, recipient, msg, name=False):
        """
        Add single message to chat log meant for recepient. 

        recipient -- str
        msg -- str
        name -- str
        """
        if len(self.log) > 1000:
            # TODO: save in a text file
            self.log = self.log[len(self.log) - 100:]
        if name:
            msg = "%s: %s" % (name, msg)
        id = self.log[-1][0] + 1
        self.log.append((id, recipient, msg))


class ChatClient(object):
    """
    Receives, cuts and displays chat log
    """

    def __init__(self):
        self.log = []
        self.width = 56

    def get_log(self, size=22):
        """
        Cut chat log to screen width.

        >>> chat = ChatClient()
        >>> chat.add_multiple(['foo', 'bar'])
        >>> chat.get_log()
        ['foo', 'bar']

        size -- int
        """
        if len(self.log) <= size:
            log = self.log
        else:
            log = self.log[len(self.log) - size:]
        formatted_log = []
        for entry in log:
            if len(entry) <= self.width:
                formatted_log.append(entry)
            else:
                chunk, w = len(entry), self.width
                formatted_log += [entry[i:i + w] for i in xrange(0, chunk, w)]
        if len(formatted_log) <= size:
            return formatted_log
        return formatted_log[len(formatted_log) - size:]

    def add_multiple(self, msgs):
        """
        Add messages to a chat log.

        msgs -- list of str
        """
        if len(self.log) > 1000:
            # TODO: save in a text file
            self.log = self.log[len(self.log) - 100:]
        self.log += msgs
