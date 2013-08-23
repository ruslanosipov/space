from lib.obj.stationary import Stationary


class TestStationaryBlocking(Stationary):

    def __init__(self):
        super(TestStationaryBlocking, self).__init__(
            '/', 'test blocking stationary', True, True)

    def activate(self):
        msg = "You activate the %s..." % self.get_name()
        return msg
