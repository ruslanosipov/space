"""Test stationary object blocking the path."""

from lib.obj.stationary import Stationary


class TestStationaryBlocking(Stationary):
    """Test stationary object blocking the path."""

    def __init__(self):
        super(TestStationaryBlocking, self).__init__(
            char='/',
            name='test blocking stationary',
            is_path_blocker=True,
            is_view_blocker=True)
