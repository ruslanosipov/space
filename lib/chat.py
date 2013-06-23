from lib.utl import packet


class Chat:
    def __init__(self):
        self.log = []

    def get_log(self, size):
        """
        Returns list of latest chat messages

        size -- int, number of last entries
        """
        # TODO: use actual values
        chat_log = [
            'Dwarf said foo',
            'Human slapped dwarf',
            'Dwarf finished his beer',
        ]
        return packet.encode(chat_log)

    def add(self, msgs):
        """
        msgs -- list
        """
        self.log += msgs
