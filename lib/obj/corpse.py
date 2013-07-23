from lib.obj.stationary import Stationary


class Corpse(Stationary):

        def __init__(self, name):
            """
            >>> corpse = Corpse('Mike')
            >>> corpse
            <class 'Corpse'>
            >>> corpse.get_name()
            'corpse of Mike'
            """
            super(Corpse, self).__init__('%', "corpse of %s" % name)
