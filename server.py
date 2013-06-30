#!/usr/bin/env python

import time

from lib.server import Server
from lib.level import Level
from lib.view import View
from lib.chat import Chat
from lib.player import Player
from lib.utl import packet

server = Server(12345)
level = Level('spaceship')
view = View(level)
chat = Chat()
server.listen()
players = {}

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
                        i.activate()
                        i.get_symbol()
                        level.remove_object(item, (x_, y_))
                        level.add_object(i.get_symbol(), (x_, y_))
                        del i
                elif package[0] == 'move':
                    # TODO: deal with data type loss on Server() level
                    x, y = package[1]
                    x, y = int(x), int(y)
                    if players[s].validate_movement((x, y)):
                        x_, y_ = players[s].get_coordinates()
                        x_, y_ = x_ + x, y_ + y
                        if not level.is_blocker((x_, y_)):
                            level.remove_object(
                                players[s].get_symbol(),
                                players[s].get_coordinates())
                            players[s].move((x, y))
                            level.add_object(
                                players[s].get_symbol(),
                                players[s].get_coordinates())
                elif package[0] == 'say':
                    chat.add_single(package[1], name=players[s].get_name())
    # Generate views for players
    for s in data.keys():
        player = players[s]
        radius = 12
        player_view = view.generate(
            player.get_coordinates(),
            radius,
            player.get_eyesight())
        chat_log = packet.encode(chat.get_log(24))
        new_data[s] = (player_view, chat_log)
    server.set_data(new_data)
    time.sleep(time.clock() - clock + 0.02)
    server.send()
