#!/usr/bin/env python

import time
import sys

from lib.server import Server
from lib.level import Level
from lib.view import View
from lib.chat import ChatServer
from lib.player import Player
from lib.utl import packet

server = Server(12345)
level = Level('spaceship')
view = View(level)
chat = ChatServer()
server.listen()
players = {}

try:
    while True:
        clock = time.clock()
        server.receive()
        data = server.get_data()
        new_data = {}
        # Process data received from players
        for s in data.keys():
            if data[s]:
                for package in data[s]:
                    if package[0] == 'connect' and s not in players:
                        player_name = package[1]
                        players[s] = Player((25, 10), player_name, symbol='@')
                        level.add_object(players[s].get_symbol(), (25, 10))
                    elif package[0] == 'activate':
                        x, y = package[1]
                        x, y = int(x), int(y)
                        x_, y_ = players[s].get_coordinates()
                        x_, y_ = x_ + x, y_ + y
                        item = level.get_top_item((x_, y_))
                        if item:
                            name = level.get_item_name(item)
                            exec("from lib.obj.%s import Item" % name)
                            i = Item(item)
                            msg = i.activate()
                            i.get_symbol()
                            level.remove_object(item, (x_, y_))
                            level.add_object(i.get_symbol(), (x_, y_))
                            del i
                        else:
                            msg = "Nothing to activate"
                        chat.add_single(players[s].get_name(), msg)
                    elif package[0] == 'move':
                        # TODO: deal with data type loss on Server() level
                        x, y = package[1]
                        x, y = int(x), int(y)
                        if players[s].validate_movement((x, y)):
                            x_, y_ = players[s].get_coordinates()
                            x_, y_ = x_ + x, y_ + y
                            mob = level.get_mob((x_, y_))
                            if not level.is_blocker((x_, y_)):
                                level.remove_object(
                                    players[s].get_symbol(),
                                    players[s].get_coordinates())
                                players[s].move((x, y))
                                level.add_object(
                                    players[s].get_symbol(),
                                    players[s].get_coordinates())
                            elif mob:
                                for player in players.values():
                                    if player.get_coordinates() == (x_, y_):
                                        if players[s].get_mode() == 'attack':
                                            player.take_damage(25)
                                            msg = 'You attack player'
                                            if not player.is_alive():
                                                level.remove_object('@',
                                                                    (x_, y_))
                                                level.add_object('%', (x_, y_))
                                                msg += '. Player is dead'
                                            chat.add_single(
                                                    players[s].get_name(),
                                                    msg)
                            else:
                                # TODO: object-specific message
                                msg = "Something is obstructing your path"
                                chat.add_single(players[s].get_name(), msg)
                    elif package[0] == 'target':
                        targets = view.get_visible_players(
                                players[s].get_coordinates(),
                                players[s].get_eyesight())
                        if len(targets):
                            players[s].set_target(targets[0])
                        else:
                            msg = 'Nothing to target'
                            chat.add_single(players[s].get_name(), msg)
                    elif package[0] == 'say':
                        chat.add_single(
                            'all',
                            package[1],
                            name=players[s].get_name())
                    elif package[0] == 'look':
                        x, y = package[1]
                        x, y = int(x), int(y)
                        x_, y_ = players[s].get_coordinates()
                        x, y = x + x_, y + y_
                        items = ', '.join(level.get_object_ids((x, y)))
                        msg = 'You see: %s' % items
                        chat.add_single(players[s].get_name(), msg)
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
