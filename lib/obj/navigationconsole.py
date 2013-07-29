from lib.obj.stationary import Stationary


class NavigationConsole(Stationary):

    def __init__(self):
        """
        >>> NavigationConsole()
        <class 'NavigationConsole'>
        """
        super(NavigationConsole, self).__init__(
            'n',
            'navigation console',
            True)
        self.player = None
        self.set_color((0, 0, 204))

    def activate(self):
        """
        >>> from lib.obj.player import Player
        >>> console = NavigationConsole()
        >>> console.set_player(Player('Mike'))
        >>> console.activate()
        'You are piloting the spaceship now...'
        """
        self.player.set_pilot()
        self.set_player()
        msg = "You are piloting the spaceship now..."
        return msg

    #--------------------------------------------------------------------------
    # accessors

    def set_player(self, player=None):
        self.player = player
