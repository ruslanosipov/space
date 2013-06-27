class Chat:
    def __init__(self):
        self.log = []

    def get_log(self, size=24):
        """
        Returns list of latest chat messages

        size -- int, number of last entries
        """
        return self.log[len(self.log) - size]

    def add(self, msgs):
        """
        msgs -- list
        """
        if len(self.log) > 1000:
            self.log = self.log[len(self.log) - 100:]
        self.log += msgs

    def get_sample_log(self, size=24):
        """
        Returns list of latest chat messages

        size -- int, number of last entries
        """
        # TODO: use actual values
        log = [
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
            'space owl: hello!'
        ]
        return log[len(log) - size:]
