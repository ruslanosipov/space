"""Teleport platform bound to a spaceship."""

from lib.obj.stationary import Stationary


class TeleportPlatform(Stationary):
    """Teleport platform bound to a spaceship.

    Can transport players between adjacent spaceships.
    """

    def __init__(self):
        super(TeleportPlatform, self).__init__(
                char='_',
                name='teleport platform')
        self.player = None

    def activate(self):
        """
        Teleport a player to the adjacent spaceship if one is around.
        """
        spaceship = self.interior.spaceship
        spaceships = spaceship.exterior.get_adjacent_spaceships(
            spaceship.coords)
        if spaceships:
            spaceship.exterior.teleport_player(
                self.player,
                spaceships[0],
                spaceship)
            msg = "Teleport platform makes a weird noise, %s disappears..." % \
                self.player.name
        else:
            msg = "No spaceships in teleport radius are detected..."
        self.player = None
        return msg

    #--------------------------------------------------------------------------
    # Accessors.

    @property
    def interior(self):
        return self._interior

    @interior.setter
    def interior(self, interior):
        self._interior = interior
        self.interior.spaceship.teleport_point = self.coords
