MSG_TYPES = [
    0,  # converstaion
    1,  # player action
    2]  # event in surroundings not caused by player


class ChatServer(object):
    """
    Manages and distributes chat messages for players.
    """
    global MSG_TYPES

    def __init__(self):
        self.log = []
        self.recipients = {}

    def __repr__(self):
        return "<class '%s'>" % self.__class__.__name__

    def get_recent_for_recipient(self, recipient):
        log = []
        if recipient not in self.recipients:
            self.recipients[recipient] = -1
        for item in self.log:
            id, receiver, msg, msg_type = item
            if id > self.recipients[recipient] and \
                    receiver in ['public', recipient]:
                log.append((msg, msg_type))
                self.recipients[recipient] = id
        return log

    def add_single(self, recipient, msg, msg_type=0):
        if len(self.log) > 1000:
            self.log = self.log[len(self.log) - 100:]
        id = self.log[-1][0] + 1 if len(self.log) else 0
        self.log.append((id, recipient, msg, msg_type))
