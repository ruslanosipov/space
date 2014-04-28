import unittest

from lib.exterior.level5d import Level5D as ExteriorLevel
from lib.obj.player import Player


class TestTeleportPlatformActivate(unittest.TestCase):

    def setUp(self):
        self.level = ExteriorLevel()
        char_map, obj_defs = [[['_']]], {'_': 'TeleportPlatform'}
        self.galactica = self.level.add_spaceship(
            (0, 0, 0, 0), 'Battlestar Galactica')
        self.galactica.load_interior(char_map, obj_defs)
        self.galactica.interior.add_player((0, 0), Player('Mike'))
        self.teleport, self.player = \
            self.galactica.interior.get_objects((0, 0))

    def test_no_spaceships_in_teleport_radius(self):
        self.teleport.player = self.player
        self.assertEqual(self.teleport.activate(),
                         "No spaceships in teleport radius are detected...")

    def test_teleport_player_to_adjacent_spaceship(self):
        enterprise = self.level.add_spaceship(
            (0, 0, 1, 1), 'USS Enterprise')
        char_map, obj_defs = [[['_']]], {'_': 'TeleportPlatform'}
        enterprise.load_interior(char_map, obj_defs)
        self.teleport.player = self.player
        self.assertEqual(self.teleport.activate(), ("Teleport platform makes "
                         "a weird noise, Mike disappears..."))
        self.assertIn(self.player, enterprise.interior.get_objects((0, 0)))
