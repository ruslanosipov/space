from lib.obj.armor import Armor


class TestArmor(Armor):

    def __init__(self):
        super(TestArmor, self).__init__(']', 'test armor', 10, 'A')
