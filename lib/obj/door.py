from lib.obj.stationary import Stationary


class Door(Stationary):
    """
    Regular door. Can be opened and closed by calling activate()
    method.
    """

    def __init__(self, is_open=False):
        if is_open:
            super(Door, self).__init__('/', 'door')
        else:
            super(Door, self).__init__('+', 'door', True, True)

    def activate(self):
        if self.block_path:
            self.char = '/'
            self.block_path, self.block_view = False, False
            msg = "You open the door..."
        else:
            self.char = '+'
            self.block_path, self.block_view = True, True
            msg = "You close the door..."
        return msg
