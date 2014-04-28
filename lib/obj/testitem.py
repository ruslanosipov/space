"""Test item instance."""

from lib.obj.item import Item


class TestItem(Item):
    """Test item instance."""

    def __init__(self):
        super(TestItem, self).__init__('?', 'test item')
