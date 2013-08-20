from lib.obj.stationary import Stationary


class NavigationConsole(Stationary):

    def __init__(self):
        super(NavigationConsole, self).__init__(
            'n',
            'navigation console',
            True)
        self.player = None

    def activate(self):
        if self.player.get_interior().get_spaceship().get_pilot():
            msg = "Someone else is operating the console..."
        elif self.player.get_interior().get_spaceship().is_alive():
            self.player.set_pilot()
            msg = "You are piloting the spaceship now..."
        else:
            msg = "The console is inoperable."
        self.set_player()
        return msg

    #--------------------------------------------------------------------------
    # accessors

    def set_player(self, player=None):
        self.player = player
