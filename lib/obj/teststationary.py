from lib.obj.stationary import Stationary


class TestStationary(Stationary):

    def __init__(self):
        super(TestStationary, self).__init__('/', 'test stationary')

    def activate(self):
        msg = "You activate the %s..." % self.get_name()
        return msg
