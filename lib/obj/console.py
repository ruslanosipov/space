"""Console (terminal)."""

from lib.obj.stationary import Stationary


class Console(Stationary):
    """Console (terminal)."""

    def __init__(self):
        super(Console, self).__init__(
                char='c',
                name='console',
                is_path_blocker=True)

    def activate(self):
        msg = "Console beeps..."
        return msg
