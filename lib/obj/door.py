from lib.obj.itemtemplate import ItemTemplate


class Item(ItemTemplate):

    def activate(self):
        if self.symbol == '+':
            self.symbol = '/'
            msg = "You open the door"
        else:
            self.symbol = '+'
            msg = "You close the door"
        return msg
