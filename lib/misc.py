import ast
import random

from lib.obj.corpse import Corpse
from lib.obj.player import ItemCanNotBeEquipped
from lib.obj.player import Player
from lib.utl import ignored

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
    Activate object topmost available object at (x, y). Some objects
    need to know who the player is while activating.
    """
    objects = level.get_objects((x, y))
    status = "Nothing to activate here..."
    for obj in objects[::-1]:
        with ignored.ignored(AttributeError):
            _ = obj.player
            obj.player = player
        with ignored.ignored(AttributeError):
            status = obj.activate()
            break
    return status


def add_player(name, spaceship, coords=None):
    """
    Places player inside a spaceship, by default coords take
    spaceship's spawn_point attribute.
    """
    player = Player(name)
    if coords is None:
        coords = spaceship.spawn_point
    spaceship.interior.add_player(coords, player)
    return player


def drop_item(player, item_name):
    """
    Drops the item under the player's feet.
    """
    item = player.inventory_remove_by_name(item_name)
    if item:
        player.interior.add_object(player.coords, item, 1)
        return "You drop a %s." % item_name
    else:
        return "You do not have such an item."


def equip_item(player, item_name):
    """
    Equips item in corresponding slot from the inventory. Returns string.
    """
    item = player.inventory_remove_by_name(item_name)
    if item:
        try:
            player.equip(item)
        except ItemCanNotBeEquipped:
            player.inventory_add(item)
            return "Item can not be equipped."
        msg = "You equip a %s." % item_name
    else:
        msg = "Can not equip a %s, item not in inventory." % item_name
    return msg


def interior_fire(player, level, chat):
    """
    Fire at other player. Target must be set up, weapon must be
    equipped. Returns string.
    """
    target = player.target
    if not player.is_gunman():
        return "You have no weapon to fire from..."
    if target:
        hostile = level.get_player(target)
        msg = 'You shoot at %s.' % hostile.name
        hostile_msg = '%s shoots at you.' % player.name
        if random.randint(0, 99) < player.get_ranged_accuracy():
            hostile.receive_damage(player.get_ranged_damage())
        else:
            msg += ' You miss.'
            hostile_msg += ' %s misses.' % player.name
        if not hostile.is_alive:
            level.remove_object(target, hostile)
            level.add_object(target, Corpse(hostile.name))
            player.target = None
            msg += ' %s is dead.' % hostile.name
            hostile_msg += ' You are dead!'
        chat.add_single(player, msg, 3)
        chat.add_single(hostile, hostile_msg, 3)
        return ''
    return 'Target is not set...'


def move(player, (x, y), level, chat):
    """
    Move or attack a hostile standing in your way.
    """
    status = ''
    hostile = level.get_player((x, y))
    if not level.is_path_blocker((x, y)):
        level.move_object(player.coords, (x, y), player)
        player.coords = (x, y)
    elif hostile:
        hostile.receive_damage(player.get_melee_damage())
        msg, hostile_msg = player.get_melee_attack_messages(hostile.name)
        if not hostile.is_alive:
            level.remove_object((x, y), hostile)
            level.add_object((x, y), Corpse(hostile.name))
            player.target = None
            msg += ' %s is dead.' % hostile.name
            hostile_msg += ' You are dead!'
        chat.add_single(player, msg, 3)
        chat.add_single(hostile, hostile_msg, 3)
    else:
        objects = level.get_objects((x, y))
        for obj in objects[::-1]:
            if obj.is_path_blocker:
                status = "Your path is obstructed by the %s..." % \
                    obj.name
                break
    return status


def look(player, (dx, dy), level, visible_tiles):
    """
    Look around the player, show description of visible objects from
    top to bottom. Returns string.
    """
    if not player.is_looking:
        player.toggle_looking()
        player.look_coords = player.coords
    x, y = player.look_coords
    x, y = x + dx, y + dy
    px, py = player.coords
    if abs(px - x) >= 12 or abs(py - y) >= 12:
        return None
    player.look_coords = (x, y)
    if (x, y) not in visible_tiles:
        return "You can't see anything there."
    objects = level.get_objects((x, y))
    names = []
    for obj in objects[::-1]:
        names.append(obj.name)
    msg = 'You see: %s.' % ', '.join(names)
    return msg


def pick_up_obj(player, (x, y), level):
    """
    Pick up top object from (x, y) and put it in the inventory. Returns
    string.
    """
    objects = level.get_objects((x, y))
    msg = "Nothing to pick up here..."
    for obj in objects[::-1]:
        with ignored.ignored(AttributeError):
            if obj.is_pickupable:
                obj.coords = None
                player.inventory_add(obj)
                level.remove_object((x, y), obj)
                msg = "You pick up a %s..." % obj.name
                break
    return msg


def set_target(player, level, visible_tiles):
    """
    Sets a target for a player if one is within visible_tiles. Returns
    string.
    """
    status = ''
    targets = level.get_nearest_players_coords(
        player.coords,
        player.sight,
        visible_tiles)
    if len(targets):
        # TODO: implement switching between targets
        player.target = targets[0]
    else:
        status = 'No suitable target found...'
    return status


def unequip_item(player, slot):
    """
    Unequip item from selected slot. Returns string.
    """
    item = player.unequip(slot)
    if item:
        player.inventory_add(item)
        msg = "You unequip a %s." % item.name
    else:
        msg = "You do not have an item in this slot."
    return msg

#------------------------------------------------------------------------------
# spaceship (exterior)


def add_spaceship(name, coords, spawn, exterior):
    tiles_map = open('dat/maps/%s_tiles.txt' % name.lower(), 'rb').read()
    items_map = open('dat/maps/%s_items.txt' % name.lower(), 'rb').read()
    level_definition = load_interior_level(tiles_map, items_map)
    txt = open('dat/obj_defs.txt', 'rb').read()
    obj_definitions = load_obj_definitions(txt)
    extras = open('dat/maps/%s_extras.txt' % name.lower(), 'rb').read()
    extras = load_extras(extras)
    spaceship = exterior.add_spaceship(coords, name)
    spaceship.load_interior(level_definition, obj_definitions, extras)
    spaceship.spawn_point = spawn
    return spaceship


def exterior_fire(coords, pointer, level):
    level.add_projectile(coords, pointer, 50, 1000, 10)
