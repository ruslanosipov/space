import unittest

from lib.obj.spaceship import Spaceship
from lib.obj.navigationconsole import NavigationConsole
from lib.obj.player import Player


class TestNavigationConsole(unittest.TestCase):

    def setUp(self):
        self.spaceship = Spaceship('@', 'Galactica', (0, 0, 0, 0))
        self.spaceship.load_interior([[['.'], ['.']]], {'.': 'Floor'})
        self.player = Player('Mike')
        self.spaceship.get_interior().add_player((0, 0), self.player)
        self.console = NavigationConsole()

    def test_console_makes_player_pilot_spaceship(self):
        self.console.set_player(self.player)
        self.assertEqual(self.console.activate(),
                         "You are piloting the spaceship now...",
                         "corresponding message should be returned")
        self.assertTrue(self.player.is_pilot(), "player should become a pilot")

    def test_console_can_not_be_used_if_spaceship_is_broken(self):
        self.spaceship.receive_damage(1000)
        self.console.set_player(self.player)
        self.assertEqual(self.console.activate(), "The console is inoperable.",
                         "console can not be activated if spaceship is broken")
        self.assertFalse(self.player.is_pilot(),
                         "player should not become a pilot")

    def test_spaceship_can_be_piloted_only_by_one_player(self):
        player = Player('Josh')
        self.spaceship.get_interior().add_player((1, 0), player)
        self.console.set_player(self.player)
        self.console.activate()
        self.console.set_player(player)
        self.assertEqual(self.console.activate(),
                         "Someone else is operating the console...",
                         "corresponding message should be returned")
        self.assertFalse(player.is_pilot(), "player should not become a pilot")

