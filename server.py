#!/usr/bin/env python

import time
import sys
from ConfigParser import ConfigParser

from lib.server import Server
from lib.level import Level
from lib.view import View
from lib.chat import ChatServer
from lib.player import Player
from lib.utl import packet

config = ConfigParser()
config.read('config.ini')
port = config.getint('server', 'port')

server = Server(port)
level = Level('spaceship')
view = View(level)
chat = ChatServer()
server.listen()
players = {}


def connect(player_name):
    global level

    player = Player((25, 10), player_name, symbol='@')
    level.add_object(player.get_symbol(), (25, 10))
    return player


def activate(player, (dx, dy)):
    global level

    x, y = player.get_coordinates()
    x, y = dx + x, dy + y
    item_symbol = level.get_top_item((x, y))
    if item_symbol:
        name = level.get_item_name(item_symbol)
        try:
            exec("from lib.obj.%s import Item" % name)
            item = Item(item_symbol)
            msg = item.activate()
            new_symbol = item.get_symbol()
            if new_symbol != item_symbol:
                level.remove_object(item_symbol, (x, y))
                level.add_object(new_symbol, (x, y))
            del item
        except ImportError:
            msg = "This object can not be activated"
    else:
        msg = "Nothing to activate"
    return msg


def pickup(player, (dx, dy)):
    global level

    x, y = player.get_coordinates()
    x, y = dx + x, dy + y
    item_symbol = level.get_top_item((x, y))
    if item_symbol:
        if level.can_be_picked_up(item_symbol):
            name = level.get_item_name(item_symbol)
            player.add_to_inventory((name, 1))
            msg = 'You pick up %s' % name
            level.remove_object(item_symbol, (x, y))
        else:
            msg = "This object can not be picked up"
    else:
        msg = "Nothing to pick up"
    return msg


def inventory(player):
    inv = player.get_inventory()
    if not len(inv):
        return "You do not own anything at the moment"
    msg = 'You have: '
    items = []
    for item, qty in inv.items():
        if qty > 1:
            items.append("%s (%d)" % (item, qty))
        else:
            items.append(item)
    msg += ', '.join(items)
    return msg


def move(player, (dx, dy)):
    global level
    global players

    msg = None
    if player.validate_movement((dx, dy)):
        x, y = player.get_coordinates()
        x, y = dx + x, dy + y
        mob = level.get_mob((x, y))
        if not level.is_blocker((x, y)):
            level.remove_object(
                player.get_symbol(),
                player.get_coordinates())
            player.move((dx, dy))
            level.add_object(
                player.get_symbol(),
                player.get_coordinates())
        elif mob:
            for mob in players.values():
                if mob.get_coordinates() == (x, y):
                    if player.get_mode() == 'attack':
                        mob.take_damage(25)
                        msg = 'You attack someone'
                        mob_msg = 'You are being attacked'
                        if not mob.is_alive():
                            level.remove_object('@', (x, y))
                            level.add_object('%', (x, y))
                            player.set_target(None)
                            msg += '. Enemy is dead'
                            mob_msg += '. You are dead'
                break
            chat.add_single(mob.get_name(), mob_msg)
        else:
            # TODO: object-specific message
            msg = "Something is obstructing your path"
        return msg


def target(player):
    global view
    global players

    msg = None
    targets = view.get_visible_players(
            player.get_coordinates(),
            player.get_eyesight())
    if len(targets):
        x, y = targets[0]
        player.set_target((x, y))
        for mob in players.values():
            if mob.get_coordinates() == (x, y):
                mob.become_target(player)
                break
    else:
        msg = 'Nothing to target'
    return msg


def fire(player):
    global level
    global players
    global chat

    target = player.get_target()
    if target:
        for mob in players.values():
            x, y = mob.get_coordinates()
            if (x, y) == target:
                mob.take_damage(50)
                msg = 'You shoot at someone'
                mob_msg = 'Someone shoots at you'
                if not mob.is_alive():
                    level.remove_object('@', (x, y))
                    level.add_object('%', (x, y))
                    msg += '. Target is dead'
                    mob_msg += '. You are dead'
                    player.set_target(None)
                break
    else:
        msg = 'No target found'
    chat.add_single(mob.get_name(), mob_msg)
    return msg


def look(player, (dx, dy)):
    global level

    x, y = player.get_coordinates()
    x, y = dx + x, dy + y
    items = ', '.join(level.get_object_ids((x, y)))
    msg = 'You see: %s' % items
    return msg

try:
    while True:
        clock = time.clock()
        server.receive()
        data = server.get_data()
        new_data = {}
        # Process data received from players
        for s in data.keys():
            if data[s]:
                for evt, arg in data[s]:
                    if s in players:
                        player = players[s]
                    if evt == 'connect' and s not in players:
                        player = connect(arg)
                        players[s] = player
                    if not player.is_alive():
                        continue
                    if evt == 'activate':
                        dx, dy = arg
                        dx, dy = int(dx), int(dy)
                        msg = activate(player, (dx, dy))
                        chat.add_single(player.get_name(), msg)
                    elif evt == 'pickup':
                        dx, dy = arg
                        dx, dy = int(dx), int(dy)
                        msg = pickup(player, (dx, dy))
                        chat.add_single(player.get_name(), msg)
                    elif evt == 'inventory':
                        msg = inventory(player)
                        chat.add_single(player.get_name(), msg)
                    elif evt == 'move':
                        # TODO: deal with data type loss on Server() level
                        dx, dy = arg
                        dx, dy = int(dx), int(dy)
                        msg = move(player, (dx, dy))
                        if msg:
                            chat.add_single(player.get_name(), msg)
                    elif evt == 'target':
                        msg = target(player)
                        if msg:
                            chat.add_single(player.get_name(), msg)
                    elif evt == 'fire':
                        msg = fire(player)
                        chat.add_single(player.get_name(), msg)
                    elif evt == 'say':
                        chat.add_single('all', arg, name=player.get_name())
                    elif evt == 'look':
                        dx, dy = arg
                        dx, dy = int(dx), int(dy)
                        msg = look(player, (dx, dy))
                        chat.add_single(player.get_name(), msg)
        # Generate views for players
        for s in data.keys():
            player = players[s]
            radius = 11
            player_view = view.generate(
                player.get_coordinates(),
                radius,
                player.get_eyesight(),
                player.get_target())
            chat_log = packet.encode(chat.get_recent(player.get_name()))
            new_data[s] = (player_view, chat_log)
        server.set_data(new_data)
        time.sleep(time.clock() - clock + 0.02)
        server.send()
except KeyboardInterrupt:
    print "Keyboard interrupt detected, exiting..."
    server.close()
    sys.exit(0)
