from lib.obj.stationary import Stationary


class Door(Stationary):

    def __init__(self, is_open=False):
        """
        >>> Door()
        <class 'Door'>
        """
        if is_open:
            super(Door, self).__init__('/', 'door')
        else:
            super(Door, self).__init__('+', 'door', True, True)

    def activate(self):
        """
        >>> door = Door(True)
        >>> door.activate()
        'You close the door...'
        >>> door.is_path_blocker()
        True
        >>> door.is_view_blocker()
        True
        >>> door.get_char()
        '+'
        """
        if self.block_path:
            self.char = '/'
            self.block_path, self.block_view = False, False
            msg = "You open the door..."
        else:
            self.char = '+'
            self.block_path, self.block_view = True, True
            msg = "You close the door..."
        return msg
