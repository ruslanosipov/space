from tests.mocks import exterior_with_adjacent_spaceships
from tests.mocks import spaceship

from lib.obj.stationary import Stationary


class TeleportPlatform(Stationary):

    def __init__(self):
        """
        >>> TeleportPlatform()
        <class 'TeleportPlatform'>
        """
        super(TeleportPlatform, self).__init__('T', 'teleport platform')
        self.player = None

    def activate(self):
        """
        >>> from lib.obj.player import Player
        >>> spaceship = spaceship()
        >>> teleport = TeleportPlatform()
        >>> spaceship.get_interior().add_object((0, 0), teleport)
        >>> player = Player('Mike')
        >>> spaceship.get_interior().add_player(player, (0, 0))
        >>> teleport.set_player(player)
        >>> teleport.activate()
        'No spaceships in teleport radius are detected...'

        >>> exterior = exterior_with_adjacent_spaceships()
        >>> interior = exterior.get_spaceships()[0].get_interior()
        >>> teleport = interior.get_objects((1, 0))[-1]
        >>> player = interior.get_player((0, 0))
        >>> teleport.set_player(player)
        >>> teleport.activate()
        'Teleport platform makes a weird noise...'
        """
        spaceship = self.get_interior().get_spaceship()
        spaceships = spaceship.get_exterior().get_adjacent_spaceships(
            spaceship.get_coords())
        if spaceships:
            spaceship.get_exterior().teleport_player(
                self.player,
                spaceships[0],
                spaceship)
            msg = "Teleport platform makes a weird noise..."
        else:
            msg = "No spaceships in teleport radius are detected..."
        self.set_player()
        return msg

    #--------------------------------------------------------------------------
    # accessors

    def set_player(self, player=None):
        self.player = player

    def set_interior(self, interior):
        super(TeleportPlatform, self).set_interior(interior)
        self.interior.get_spaceship().set_teleport_point(self.get_coords())
