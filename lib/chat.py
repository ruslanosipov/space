class Chat:

    def __init__(self):
        self.log = []

    def get_log(self, size=24):
        """
        Returns list of latest chat messages

        size -- int, number of last entries
        """
        if not self.log:
            self.log = [
                'crewman: hi!',
                'space owl: hello!',
                'crewman: how can I help you?',
                'space owl: hello!',
                'crewman: hi?',
                'space owl: hello!',
                'crewman: em?',
                'space owl: hello!',
                'crewman: right, keep it up',
                'space owl: hello!',
                'crewman: em?',
                'space owl: hello!',
                'crewman: whatever',
                'space owl: I am a space owl',
                'crewman: huh?!',
                'space owl: hello!',
                'crewman: huh?!',
                'space owl: hello!',
                'space owl: hello!',
                'crewman: you repeated yourself',
                'space owl: I know',
                'space owl: fell asleep in hello pose',
                'crewman: how is that?',
                'space owl: look -',
                'space owl: hello!']
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
