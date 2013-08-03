from lib.obj.item import Item


class Knife(Item):

    def __init__(self):
        """
        >>> Knife()
        <class 'Knife'>
        """
        super(Knife, self).__init__(')', 'knife')
        self.melee_damage = (20, 30)
