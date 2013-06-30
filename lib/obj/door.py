from lib.obj.itemtemplate import ItemTemplate


class Item(ItemTemplate):

    def activate(self):
        self.symbol = '/' if self.symbol == '+' else '+'
