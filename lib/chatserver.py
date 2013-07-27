class ChatServer(object):
    """
    Manages and sends out chat messages for players.
    """

    def __init__(self):
        """
        >>> ChatServer()
        <class 'ChatServer'>
        """
        self.log = []
        self.recipients = {}

    def __repr__(self):
        return "<class '%s'>" % self.__class__.__name__

    def get_recent(self, recipient):
        """
        Returns list of latest chat messages

        >>> from lib.obj.player import Player
        >>> chat = ChatServer()
        >>> player = Player('Mike')
        >>> chat.add_single(player, 'bar')
        >>> chat.add_single('all', 'foo')
        >>> chat.get_recent(player)
        ['bar', 'foo']

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

        >>> from lib.obj.player import Player
        >>> chat = ChatServer()
        >>> player = Player('Mike')
        >>> chat.add_single(player, 'bar')
        >>> chat.get_recent(player)
        ['bar']
        """
        if len(self.log) > 1000:
            # TODO: save in a text file
            self.log = self.log[len(self.log) - 100:]
        if name:
            msg = "%s: %s" % (name, msg)
        id = self.log[-1][0] + 1 if len(self.log) else 0
        self.log.append((id, recipient, msg))
