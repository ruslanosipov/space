from lib.obj.stationary import Stationary


class Console(Stationary):

    def __init__(self):
        super(Console, self).__init__('c', 'console', True)

    def activate(self):
        msg = "Console beeps..."
        return msg
