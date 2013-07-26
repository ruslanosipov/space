from lib.exterior.level5d import Level5D
from lib.interior.level3d import Level3D
from lib.obj.spaceship import Spaceship
from lib.obj.player import Player


def exterior_with_adjacent_spaceships():
    """
    Creates 2 identical spaceships adjacent to each other with
    interiors, players and some tiles/items to play around with.

    .T#
    ..#
    .c#

    >>> exterior = exterior_with_adjacent_spaceships()
    >>> exterior
    <class 'Level5D'>
    >>> spaceships = exterior.get_spaceships()
    >>> spaceships
    [<class 'Spaceship'> Galactica, <class 'Spaceship'> Enterprise]
    >>> [spaceship.get_interior() for spaceship in spaceships]
    [<class 'Level3D'>, <class 'Level3D'>]
    >>> [s.get_interior().get_players() for s in spaceships]
    [[<class 'Player'> Mike], [<class 'Player'> Josh]]
    """
    level_definition = [
        [['.'], ['.', 'T'], ['#']],
        [['.'], ['.'], ['#']],
        [['.'], ['.', 'c'], ['#']]]
    obj_definitions = {
        '.': 'Floor',
        '#': 'Wall',
        'T': 'TeleportPlatform',
        'c': 'Console'}

    exterior = Level5D()
    galactica = exterior.add_spaceship(
        name='Galactica',
        coords=(0, 0, 0, 0))
    galactica.load_interior(level_definition, obj_definitions)
    galactica.get_interior().add_player(Player('Mike'), (0, 0))
    enterprise = exterior.add_spaceship(
        name='Enterprise',
        coords=(0, 0, 1, 0))
    enterprise.load_interior(level_definition, obj_definitions)
    enterprise.get_interior().add_player(Player('Josh'), (0, 0))

    return exterior


def spaceship():
    """
    >>> spaceship()
    <class 'Spaceship'> Galactica
    """
    galactica = Level5D().add_spaceship('Galactica', (0, 0, 0, 0))
    galactica.load_interior([[['.']]], {'.': 'Floor'})
    return galactica


def spaceship_with_two_players():
    """
    >>> spaceship = spaceship_with_two_players()
    >>> spaceship
    <class 'Spaceship'> Galactica
    >>> spaceship.get_interior().get_players()
    [<class 'Player'> Mike, <class 'Player'> Josh]
    """
    galactica = Level5D().add_spaceship('Galactica', (0, 0, 0, 0))
    level_definition = [
        [['.'], ['.', '+']],
        [['.'], ['.']]]
    obj_definitions = {
        '.': 'Floor',
        '+': 'Door'}
    galactica.load_interior(level_definition, obj_definitions)
    galactica.get_interior().add_player(Player('Mike'), (0, 0))
    galactica.get_interior().add_player(Player('Josh'), (1, 1))
    return galactica
