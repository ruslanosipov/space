"""Test stationary object instance."""

from lib.obj.stationary import Stationary


class TestStationary(Stationary):
    """Test stationary object instance."""

    def __init__(self):
        super(TestStationary, self).__init__('/', 'test stationary')

    def activate(self):
        return "You activate the %s..." % self.name
