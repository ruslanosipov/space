from lib.obj.item import Item


class Gun(Item):

    def __init__(self):
        """
        >>> Gun()
        <class 'Gun'>
        """
        super(Gun, self).__init__('}', 'gun')