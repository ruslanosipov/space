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
        >>> from lib.interior.level3d import Level3D
        >>> from lib.exterior.level5d import Level5D
        >>> from lib.obj.spaceship import Spaceship
        >>> from lib.obj.player import Player
        >>> ext_level = Level5D()
        >>> spaceship = ext_level.add_spaceship('Enterprise', (0, 0, 0, 0))
        >>> mothership = ext_level.add_spaceship('Exterminator', (0, 0, 1, 1))
        >>> spaceship.set_interior(Level3D([[['.']]], {'.': 'Floor'}))
        >>> mothership.set_interior(Level3D([[['.']]], {'.': 'Floor'}))
        >>> spaceship.get_interior().set_spaceship(spaceship)
        >>> mothership.get_interior().set_spaceship(mothership)
        >>> player = Player('Mike')
        >>> spaceship.add_player(player, (0, 0))
        >>> teleport = TeleportPlatform()
        >>> teleport.set_level(spaceship.get_interior())
        >>> teleport.set_player(player)
        >>> teleport.activate()
        'Teleport platform makes a weird noise...'
        """
        spaceships = self.get_level().get_spaceship().get_adjacent_spaceships()
        if spaceships:
            self.get_level().get_spaceship().teleport_player_out(
                self.player,
                spaceships[0])
            msg = "Teleport platform makes a weird noise..."
        else:
            msg = "No spaceships in teleport radius are detected..."
        self.set_player()
        return msg

    def set_player(self, player=None):
        self.player = player
