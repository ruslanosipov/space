from lib.obj.stationary import Stationary


class TeleportPlatform(Stationary):
    """
    Teleport platform bound to a spaceship. Can transport players
    between adjacent spaceships.
    """

    def __init__(self):
        super(TeleportPlatform, self).__init__('_', 'teleport platform')
        self.player = None

    def activate(self):
        """
        Teleport a player to the adjacent spaceship if one is around.
        """
        spaceship = self.get_interior().get_spaceship()
        spaceships = spaceship.get_exterior().get_adjacent_spaceships(
            spaceship.get_coords())
        if spaceships:
            spaceship.get_exterior().teleport_player(
                self.player,
                spaceships[0],
                spaceship)
            msg = "Teleport platform makes a weird noise, %s disappears..." % \
                self.player.get_name()
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
