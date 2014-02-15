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
    Activate object topmost available object at (x, y). Some objects
    need to know who the player is while activating.
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
    Places player inside a spaceship, by default coords take
    spaceship's spawn_point attribute.
    """
    player = Player(name)
    if coords is None:
        coords = spaceship.get_spawn_point()
    spaceship.get_interior().add_player(coords, player)
    return player


def drop_item(player, item_name):
    """
    Drops the item under the player's feet.
    """
    item = player.inventory_remove_by_name(item_name)
    if item:
        player.get_interior().add_object(player.get_coords(), item, 1)
        return "You drop a %s." % item_name
    else:
        return "You do not have such an item."


def equipment(player):
    """
    Returnes string describing player's equipment.
    """
    equipment = []
    for k, v in player.get_equipment().items():
        v = 'None' if v is None else v.get_name()
        equipment.append({'slot': k, 'item': v})
    return {'equipment': equipment}


def equip_item(player, item_name, slot='hands'):
    """
    Equips item in desired slot from the inventory. Returns string.
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
    Fire at other player. Target must be set up, weapon must be
    equipped. Returns string.
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
    Return list of strings (items).
    """
    inv = player.get_inventory()
    contents = []
    for item, qty in inv.items():
        item = item.get_name()
        if qty > 1:
            item += " (%d)" % qty
        contents.append(item)
    return contents


def move(player, (x, y), level, chat):
    """
    Move or attack a hostile standing in your way.
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
    Look around the player, show description of visible objects from
    top to bottom. Returns string.
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
    Pick up top object from (x, y) and put it in the inventory. Returns
    string.
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
    Sets a target for a player if one is within visible_tiles. Returns
    string.
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
    Unequip item from selected slot. Returns string.
    """
    item = player.unequip(slot)
    if item:
        player.inventory_add(item)
        msg = "You unequip a %s." % item.get_name()
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
    spaceship.set_view(InteriorView(spaceship.get_interior()))
    spaceship.set_spawn_point(spawn)
    return spaceship


def exterior_fire(coords, pointer, level):
    level.add_projectile(coords, pointer, 50, 1000, 10)
