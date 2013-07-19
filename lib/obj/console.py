from lib.obj.stationary import Stationary


class Console(Stationary):

    def __init__(self):
        """
        >>> Console()
        <class 'Console'>
        """
        super(Console, self).__init__('c', 'console')

    def activate(self):
        """
        >>> console = Console()
        >>> console.activate()
        'Console beeps...'
        """
        msg = "Console beeps..."
        return msg
