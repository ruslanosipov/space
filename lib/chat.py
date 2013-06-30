class Chat:

    def __init__(self):
        self.log = []

    def get_log(self, size=24):
        """
        Returns list of latest chat messages

        size -- int, number of last entries
        """
        if not self.log:
            self.log = ['Welcome to Space, the game in space!']
        return self.log[len(self.log) - size:]

    def add_single(self, msg, name=False):
        """
        msg -- str
        name -- str
        """
        if len(self.log) > 1000:
            self.log = self.log[len(self.log) - 100:]
        if name:
            msg = "%s: %s" % (name, msg)
        self.log.append(msg)
