"""Allows players to take control of the spaceship."""

from lib.obj.stationary import Stationary


class NavigationConsole(Stationary):
    """Allows players to take control of the spaceship."""

    def __init__(self):
        super(NavigationConsole, self).__init__(
            char='n',
            name='navigation console',
            is_path_blocker=True)
        self.player = None

    def activate(self):
        if self.player.interior.spaceship.pilot:
            msg = "Someone else is operating the console..."
        elif self.player.interior.spaceship.is_alive:
            self.player.toggle_pilot()
            msg = "You are piloting the spaceship now..."
        else:
            msg = "The console is inoperable."
        self.player = None
        return msg
