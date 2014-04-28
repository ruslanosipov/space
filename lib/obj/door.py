"""Regular door."""

from lib.obj.stationary import Stationary


class Door(Stationary):
    """Regular door.

    Can be opened and closed by calling activate() method.
    """

    def __init__(self, is_open=False):
        if is_open:
            super(Door, self).__init__(char='/', name='door')
        else:
            super(Door, self).__init__(
                    char='+',
                    name='door',
                    is_path_blocker=True,
                    is_view_blocker=True)

    def activate(self):
        if self.is_path_blocker:
            self.char = '/'
            self.is_path_blocker, self.is_view_blocker = False, False
            msg = "You open the door..."
        else:
            self.char = '+'
            self.is_path_blocker, self.is_view_blocker = True, True
            msg = "You close the door..."
        return msg
