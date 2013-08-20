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
        [['.'], ['.', '_'], ['#']],
        [['.'], ['.'], ['#']],
        [['.'], ['.', 'c'], ['#']]]
    obj_definitions = {
        '.': 'Floor',
        '#': 'Wall',
        '_': 'TeleportPlatform',
        'c': 'Console'}

    exterior = Level5D()
    galactica = exterior.add_spaceship(
        coords=(0, 0, 0, 0),
        name='Galactica')
    galactica.load_interior(level_definition, obj_definitions)
    galactica.get_interior().add_player((0, 0), Player('Mike'))
    enterprise = exterior.add_spaceship(
        coords=(0, 0, 1, 0),
        name='Enterprise')
    enterprise.load_interior(level_definition, obj_definitions)
    enterprise.get_interior().add_player((0, 0), Player('Josh'))

    return exterior


def spaceship():
    """
    >>> spaceship()
    <class 'Spaceship'> Galactica
    """
    galactica = Level5D().add_spaceship((0, 0, 0, 0), 'Galactica')
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
    galactica = Level5D().add_spaceship((0, 0, 0, 0), 'Galactica')
    level_definition = [
        [['.'], ['.', '+']],
        [['.'], ['.']]]
    obj_definitions = {
        '.': 'Floor',
        '+': 'Door'}
    galactica.load_interior(level_definition, obj_definitions)
    galactica.get_interior().add_player((0, 0), Player('Mike'))
    galactica.get_interior().add_player((1, 1), Player('Josh'))
    return galactica
