import ast

from lib.obj.player import Player
from lib.obj.player import IncorrectSlotName, ItemCanNotBeEquippedInSlot
from lib.obj.corpse import Corpse
from lib.interior.view import InteriorView

#------------------------------------------------------------------------------
# server game start setup


def load_extras(raw_extras):
    extras = {}
    for extra in raw_extras.split('\n'):
        if not len(extra):
            continue
        char, name, coords = extra.split('|')
        coords = ast.literal_eval('[%s]' % coords)
        for coord in coords:
            extras[coord] = (char, name)
    return extras


def load_interior_level(tiles_map, items_map):
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
    status = "Nothing to activate here..."
    for obj in objects[::-1]:
        try:
            try:
                obj.set_player(player)
            except AttributeError:
                pass
            status = obj.activate()
            break
        except AttributeError:
            pass
    return status


def add_player(name, spaceship, coords=None):
    """
    >>> from tests import mocks
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
    >>> from tests import mocks
    >>> from lib.obj.lasergun import LaserGun
    >>> spaceship = mocks.spaceship()
    >>> player = add_player('Mike', spaceship, (0, 0))
    >>> drop_item(player, 'helmet')
    'You do not have such an item.'
    >>> player.inventory_add(LaserGun())
    >>> drop_item(player, 'laser gun')
    'You drop a laser gun.'
    >>> player.get_inventory()
    {}
    >>> player.get_interior().get_objects((0, 0))[-2]
    <class 'LaserGun'>
    """
    item = player.inventory_remove_by_name(item_name)
    if item:
        player.get_interior().add_object(player.get_coords(), item, 1)
        return "You drop a %s." % item_name
    else:
        return "You do not have such an item."


def equipment(player):
    """
    >>> from lib.obj.player import Player
    >>> from lib.obj.powerarmor import PowerArmor
    >>> player = Player('Mike')
    >>> player.inventory_add(PowerArmor())
    >>> equipment(player)
    'You do not have anything equipped at the moment.'
    >>> _ = equip_item(player, 'power armor', 'torso')
    >>> equipment(player)
    'Equipment: power armor (torso).'
    """
    equipment = player.get_equipment()
    contents = []
    for k, v in equipment.items():
        if v is not None:
            contents.append("%s (%s)" % (v.get_name(), k))
    if not len(contents):
        return "You do not have anything equipped at the moment."
    return "Equipment: %s." % ', '.join(contents)


def equip_item(player, item_name, slot='hands'):
    """
    >>> from lib.obj.player import Player
    >>> from lib.obj.lasergun import LaserGun
    >>> from lib.obj.powerarmor import PowerArmor
    >>> player = Player('Mike')
    >>> player.inventory_add(LaserGun())
    >>> player.inventory_add(PowerArmor())
    >>> equip_item(player, 'helmet', 'head')
    'Can not equip a helmet, item not in inventory.'
    >>> equip_item(player, 'laser gun', 'toe')
    'Incorrect equipment slot name.'
    >>> equip_item(player, 'laser gun')
    'You equip a laser gun.'
    >>> equip_item(player, 'power armor', 'torso')
    'You equip a power armor.'
    >>> player.get_inventory()
    {}
    """
    item = player.inventory_remove_by_name(item_name)
    if item:
        try:
            player.equip(item, slot)
        except IncorrectSlotName:
            player.inventory_add(item)
            return "Incorrect equipment slot name."
        except ItemCanNotBeEquippedInSlot:
            player.inventory_add(item)
            return "Item can not be equipped in selected slot."
        msg = "You equip a %s." % item_name
    else:
        msg = "Can not equip a %s, item not in inventory." % item_name
    return msg


def interior_fire(player, level, chat):
    """
    >>> from lib.interior.level3d import Level3D
    >>> from lib.obj.player import Player
    >>> from lib.chatserver import ChatServer
    >>> from lib.obj.lasergun import LaserGun
    >>> chat = ChatServer()
    >>> player = Player('Mike')
    >>> hostile = Player('Josh')
    >>> level = Level3D()
    >>> level.load_converted_char_map([[['.'], ['.']]], {'.': 'Floor'})
    >>> level.add_object((0, 0), player)
    >>> level.add_object((1, 0), hostile)
    >>> interior_fire(player, level, chat)
    'You have no weapon to fire from...'
    >>> _ = player.equip(LaserGun())
    >>> interior_fire(player, level, chat)
    'Target is not set...'
    >>> _ = set_target(player, level)
    >>> interior_fire(player, level, chat)
    ''
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
        chat.add_single(player, msg, 3)
        chat.add_single(hostile, hostile_msg, 3)
        return ''
    return 'Target is not set...'


def inventory(player):
    """
    >>> from lib.obj.player import Player
    >>> from lib.obj.lasergun import LaserGun
    >>> player = Player('Mike')
    >>> inventory(player)
    'You do not own anything at the moment...'
    >>> player.inventory_add(LaserGun())
    >>> inventory(player)
    'Inventory contents: laser gun.'
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
    >>> from tests import mocks
    >>> from lib.chatserver import ChatServer
    >>> chat = ChatServer()
    >>> spaceship = mocks.spaceship_with_two_players()
    >>> player = spaceship.get_interior().get_objects((0, 0))[-1]
    >>> move(player, (1, 0), spaceship.get_interior(), chat)
    'Your path is obstructed by the door...'
    >>> move(player, (0, 1), spaceship.get_interior(), chat)
    ''
    >>> move(player, (1, 1), spaceship.get_interior(), chat)
    ''
    """
    status = ''
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
        chat.add_single(player, msg, 3)
        chat.add_single(hostile, hostile_msg, 3)
    else:
        objects = level.get_objects((x, y))
        for obj in objects[::-1]:
            if obj.is_path_blocker():
                status = "Your path is obstructed by the %s..." % \
                    obj.get_name()
                break
    return status


def look(player, (dx, dy), level, visible_tiles):
    """
    >>> from lib.interior.level3d import Level3D
    >>> from lib.obj.player import Player
    >>> level = Level3D()
    >>> level.load_converted_char_map([[['.', 'c']]],
    ...                               {'.': 'Floor', 'c': 'Console'})
    >>> player = Player('Mike')
    >>> look(player, (0, 0), level, [(0, 0)])
    'You see: console, floor.'
    >>> look(player, (0, 1), level, [(0, 0)])
    "You can't see anything there."
    """
    if not player.is_looking():
        player.set_looking()
        player.set_look_coords(player.get_coords())
    x, y = player.get_look_coords()
    x, y = x + dx, y + dy
    px, py = player.get_coords()
    if abs(px - x) >= 12 or abs(py - y) >= 12:
        return None
    player.set_look_coords((x, y))
    if (x, y) not in visible_tiles:
        return "You can't see anything there."
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
    ...                               {'.': 'Floor', '}': 'LaserGun'})
    >>> pick_up_obj(player, (0, 0), level)
    'You pick up a laser gun...'
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


def set_target(player, level, visible_tiles):
    """
    >>> from lib.interior.level3d import Level3D
    >>> from lib.obj.player import Player
    >>> player = Player('Mike')
    >>> l = [[['.'], ['.']], [['.'], ['.']]]
    >>> level = Level3D()
    >>> level.load_converted_char_map(l, {'.': 'Floor'})
    >>> level.add_object((0, 0), player)
    >>> set_target(player, level, [])
    'No suitable target found...'
    >>> hostile = Player('Josh')
    >>> level.add_object((1, 1), hostile)
    >>> set_target(player, level, [(1, 1)])
    ''
    """
    status = ''
    targets = level.get_nearest_players_coords(
        player.get_coords(),
        player.get_sight(),
        visible_tiles)
    if len(targets):
        # TODO: implement switching between targets
        x, y = targets[0]
        player.set_target((x, y))
    else:
        status = 'No suitable target found...'
    return status


def unequip_item(player, slot):
    """
    >>> from lib.obj.player import Player
    >>> from lib.obj.lasergun import LaserGun
    >>> player = Player('Mike')
    >>> player.inventory_add(LaserGun())
    >>> equip_item(player, 'laser gun')
    'You equip a laser gun.'
    >>> player.get_inventory()
    {}
    >>> unequip_item(player, 'toe')
    'You do not have item in this slot.'
    >>> unequip_item(player, 'hands')
    'You unequip a laser gun.'
    >>> player.get_inventory()
    {<class 'LaserGun'>: 1}
    """
    item = player.unequip(slot)
    if item:
        player.inventory_add(item)
        msg = "You unequip a %s." % item.get_name()
    else:
        msg = "You do not have item in this slot."
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
    extras = open('dat/maps/%s_extras.txt' % name.lower(), 'rb').read()
    extras = load_extras(extras)
    spaceship = exterior.add_spaceship(coords, name)
    spaceship.load_interior(level_definition, obj_definitions, extras)
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
