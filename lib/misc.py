from tests import mocks

from lib.obj.player import Player
from lib.obj.corpse import Corpse
from lib.obj.spaceship import Spaceship
from lib.interior.level3d import Level3D
from lib.interior.view import InteriorView

#------------------------------------------------------------------------------
# server game start setup


def load_interior_level(tiles_map, items_map):
    r"""
    >>> tiles_map, items_map = '###\n...', '#+#\n...'
    >>> load_interior_level(tiles_map, items_map)
    [[['#'], ['#', '+'], ['#']], [['.'], ['.'], ['.']]]
    """
    level = []
    tiles_map, items_map = tiles_map.split('\n'), items_map.split('\n')
    for y, line in enumerate(tiles_map):
        level.append([])
        for x, tile in enumerate(line):
            level[y].append([tile])
            if items_map[y][x] != tile:
                level[y][x].append(items_map[y][x])
    return level


def load_obj_definitions(txt, separator='|'):
    r"""
    >>> txt = '.|Floor\n#|Wall'
    >>> d = load_obj_definitions(txt)
    >>> d['.']
    'Floor'
    >>> d['#']
    'Wall'
    """
    obj_defs = {}
    for line in txt.split('\n'):
        if line:
            char, name = line.split(separator)
            obj_defs[char] = name
    return obj_defs

#------------------------------------------------------------------------------
# player (interior)


def activate_obj((x, y), level, player=None):
    """
    >>> from lib.interior.level3d import Level3D
    >>> level = Level3D()
    >>> level.load_converted_char_map([[['.', '+'], ['.']]],
    ...                               {'.': 'Floor', '+': 'Door'})
    >>> activate_obj((0, 0), level)
    'You open the door...'
    >>> activate_obj((1, 0), level)
    'Nothing to activate here...'
    """
    objects = level.get_objects((x, y))
    msg = "Nothing to activate here..."
    for obj in objects[::-1]:
        try:
            try:
                obj.set_player(player)
            except AttributeError:
                pass
            msg = obj.activate()
            break
        except AttributeError:
            pass
    return msg


def add_player(name, spaceship, coords=None):
    """
    >>> spaceship = mocks.spaceship()
    >>> player = add_player('Mike', spaceship, (0, 0))
    >>> player
    <class 'Player'> Mike
    >>> player.get_interior().get_spaceship()
    <class 'Spaceship'> Galactica
    """
    player = Player(name)
    if coords is None:
        coords = spaceship.get_spawn_point()
    spaceship.get_interior().add_player(coords, player)
    return player


def drop_item(player, item_name):
    """
    >>> from lib.obj.gun import Gun
    >>> spaceship = mocks.spaceship()
    >>> player = add_player('Mike', spaceship, (0, 0))
    >>> drop_item(player, 'helmet')
    'You do not have such an item.'
    >>> player.inventory_add(Gun())
    >>> drop_item(player, 'gun')
    'You drop a gun.'
    >>> player.get_inventory()
    {}
    >>> player.get_interior().get_objects((0, 0))[-2]
    <class 'Gun'>
    """
    item = player.inventory_remove_by_name(item_name)
    if item:
        player.get_interior().add_object(player.get_coords(), item, 1)
        return "You drop a %s." % item_name
    else:
        return "You do not have such an item."


def equip_item(player, item_name):
    """
    >>> from lib.obj.player import Player
    >>> from lib.obj.gun import Gun
    >>> player = Player('Mike')
    >>> player.inventory_add(Gun())
    >>> equip_item(player, 'helmet')
    'Can not equip a helmet, item not in inventory.'
    >>> equip_item(player, 'gun')
    'You equip a gun.'
    >>> player.get_inventory()
    {}
    """
    item = player.inventory_remove_by_name(item_name)
    if item:
        player.equip(item)
        msg = "You equip a %s." % item_name
    else:
        msg = "Can not equip a %s, item not in inventory." % item_name
    return msg


def interior_fire(player, level, chat):
    """
    >>> from lib.interior.level3d import Level3D
    >>> from lib.obj.player import Player
    >>> from lib.chatserver import ChatServer
    >>> from lib.obj.gun import Gun
    >>> chat = ChatServer()
    >>> player = Player('Mike')
    >>> hostile = Player('Josh')
    >>> level = Level3D()
    >>> level.load_converted_char_map([[['.'], ['.']]], {'.': 'Floor'})
    >>> level.add_object((0, 0), player)
    >>> level.add_object((1, 0), hostile)
    >>> interior_fire(player, level, chat)
    'You have no weapon to fire from...'
    >>> player.equip(Gun())
    >>> interior_fire(player, level, chat)
    'Target is not set...'
    >>> set_target(player, level)
    >>> interior_fire(player, level, chat)
    'You shoot at Josh.'
    """
    target = player.get_target()
    if not player.is_gunman():
        return "You have no weapon to fire from..."
    if target:
        hostile = level.get_player(target)
        hostile.receive_damage(player.get_ranged_damage())
        msg = 'You shoot at %s.' % hostile.get_name()
        hostile_msg = '%s shoots at you.' % player.get_name()
        if not hostile.is_alive():
            level.remove_object(target, hostile)
            level.add_object(target, Corpse(hostile.get_name()))
            player.set_target()
            msg += ' %s is dead.' % hostile.get_name()
            hostile_msg += ' You are dead!'
        chat.add_single(hostile, hostile_msg, 2)
    else:
        msg = 'Target is not set...'
    return msg


def inventory(player):
    """
    >>> from lib.obj.player import Player
    >>> from lib.obj.gun import Gun
    >>> player = Player('Mike')
    >>> inventory(player)
    'You do not own anything at the moment...'
    >>> player.inventory_add(Gun())
    >>> inventory(player)
    'Inventory contents: gun.'
    """
    inv = player.get_inventory()
    if not len(inv):
        return "You do not own anything at the moment..."
    contents = []
    for item, qty in inv.items():
        item = item.get_name()
        if qty > 1:
            item += " (%d)" % qty
        contents.append(item)
    msg = 'Inventory contents: %s.' % ', '.join(contents)
    return msg


def move(player, (x, y), level, chat):
    """
    >>> from lib.chatserver import ChatServer
    >>> chat = ChatServer()
    >>> spaceship = mocks.spaceship_with_two_players()
    >>> player = spaceship.get_interior().get_objects((0, 0))[-1]
    >>> move(player, (1, 0), spaceship.get_interior(), chat)
    'Your path is obstructed by the door...'
    >>> move(player, (0, 1), spaceship.get_interior(), chat)
    >>> move(player, (1, 1), spaceship.get_interior(), chat)
    'You punch Josh.'
    """
    msg = None
    hostile = level.get_player((x, y))
    if not level.is_path_blocker((x, y)):
        level.move_object(player.get_coords(), (x, y), player)
        player.set_coords((x, y))
    elif hostile:
        hostile.receive_damage(player.get_melee_damage())
        msg, hostile_msg = player.get_melee_attack_messages(hostile.get_name())
        if not hostile.is_alive():
            level.remove_object((x, y), hostile)
            level.add_object((x, y), Corpse(hostile.get_name()))
            player.set_target()
            msg += ' %s is dead.' % hostile.get_name()
            hostile_msg += ' You are dead!'
        chat.add_single(hostile, hostile_msg, 2)
    else:
        objects = level.get_objects((x, y))
        for obj in objects[::-1]:
            if obj.is_path_blocker():
                msg = "Your path is obstructed by the %s..." % obj.get_name()
                break
    return msg


def look((x, y), level):
    """
    >>> from lib.interior.level3d import Level3D
    >>> level = Level3D()
    >>> level.load_converted_char_map([[['.', 'c']]],
    ...                               {'.': 'Floor', 'c': 'Console'})
    >>> look((0, 0), level)
    'You see: console, floor.'
    """
    objects = level.get_objects((x, y))
    names = []
    for obj in objects[::-1]:
        names.append(obj.get_name())
    msg = 'You see: %s.' % ', '.join(names)
    return msg


def pick_up_obj(player, (x, y), level):
    """
    >>> from lib.interior.level3d import Level3D
    >>> from lib.obj.player import Player
    >>> player = Player('Mike')
    >>> level = Level3D()
    >>> level.load_converted_char_map([[['.', '}'], ['.']]],
    ...                               {'.': 'Floor', '}': 'Gun'})
    >>> pick_up_obj(player, (0, 0), level)
    'You pick up a gun...'
    >>> pick_up_obj(player, (1, 0), level)
    'Nothing to pick up here...'
    """
    objects = level.get_objects((x, y))
    msg = "Nothing to pick up here..."
    for obj in objects[::-1]:
        try:
            if obj.is_pickupable():
                obj.set_coords(None)
                player.inventory_add(obj)
                level.remove_object((x, y), obj)
                msg = "You pick up a %s..." % obj.get_name()
                break
        except AttributeError:
            pass
    return msg


def set_target(player, level):
    """
    >>> from lib.interior.level3d import Level3D
    >>> from lib.obj.player import Player
    >>> player = Player('Mike')
    >>> l = [[['.'], ['.']], [['.'], ['.']]]
    >>> level = Level3D()
    >>> level.load_converted_char_map(l, {'.': 'Floor'})
    >>> level.add_object((0, 0), player)
    >>> set_target(player, level)
    'No suitable target found...'
    >>> hostile = Player('Josh')
    >>> level.add_object((1, 1), hostile)
    >>> set_target(player, level)
    """
    msg = None
    targets = level.get_nearest_mobs_coords(
        player.get_coords(),
        player.get_sight())
    if len(targets):
        # TODO: implement switching between targets
        x, y = targets[0]
        player.set_target((x, y))
    else:
        msg = 'No suitable target found...'
    return msg

#------------------------------------------------------------------------------
# spaceship (exterior)


def add_spaceship(name, coords, spawn, exterior):
    """
    >>> from lib.exterior.level5d import Level5D
    >>> add_spaceship('Galactica', (0, 0, 0, 0), (8, 3), Level5D())
    <class 'Spaceship'> Galactica
    """
    tiles_map = open('dat/maps/%s_tiles.txt' % name.lower(), 'rb').read()
    items_map = open('dat/maps/%s_items.txt' % name.lower(), 'rb').read()
    level_definition = load_interior_level(tiles_map, items_map)
    txt = open('dat/obj_defs.txt', 'rb').read()
    obj_definitions = load_obj_definitions(txt)
    spaceship = exterior.add_spaceship(coords, name)
    spaceship.load_interior(level_definition, obj_definitions)
    spaceship.set_view(InteriorView(spaceship.get_interior()))
    spaceship.set_spawn_point(spawn)
    return spaceship


def exterior_fire(coords, pointer, level):
    """
    >>> from lib.exterior.level5d import Level5D
    >>> from lib.obj.spaceship import Spaceship
    >>> s = Spaceship('@', 'USS Enterprise', (0, 0, 0, 0))
    >>> exterior_fire(s.get_coords(), s.get_pointer(), Level5D())
    """
    level.add_projectile(coords, pointer, 50, 1000, 10)
