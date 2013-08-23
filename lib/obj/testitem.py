from lib.obj.item import Item


class TestItem(Item):

    def __init__(self):
        super(TestItem, self).__init__('?', 'test item')
