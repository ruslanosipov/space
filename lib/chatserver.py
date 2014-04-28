"""Manages and distributes chat messages for players."""

MSG_TYPES = [
    0,  # Conversation.
    1,  # Player action.
    2,  # Event in surroundings not caused by player.
    3,  # Hostile action.
]


class ChatServer(object):
    """Manages and distributes chat messages for players."""

    def __init__(self):
        self.log = []
        self.recipients = {}

    def get_recent_for_recipient(self, recipient):
        """Get a list of messages recipient haven't received yet."""
        log = []
        if recipient not in self.recipients:
            self.recipients[recipient] = -1
        for item in self.log:
            msg_id, receiver, msg, msg_type = item
            if msg_id > self.recipients[recipient] and \
                    receiver in ['public', recipient]:
                log.append((msg, msg_type))
                self.recipients[recipient] = msg_id
        return log

    def add_single(self, recipient, msg, msg_type=0):
        """Add single message to message pool."""
        if len(self.log) > 1000:
            self.log = self.log[len(self.log) - 100:]
        msg_id = self.log[-1][0] + 1 if len(self.log) else 0
        self.log.append((msg_id, recipient, msg, msg_type))
