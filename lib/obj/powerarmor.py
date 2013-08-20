from lib.obj.armor import Armor


class PowerArmor(Armor):

    def __init__(self):
        """
        >>> PowerArmor()
        <class 'PowerArmor'>
        """
        super(PowerArmor, self).__init__(']', 'power armor', 30, 'P')
