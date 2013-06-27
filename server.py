#!/usr/bin/env python

import time

from lib.server import Server
from lib.level import Level
from lib.view import View
from lib.chat import Chat
from lib.player import Player

server = Server(12345)
level = Level('dat/spaceship.map')
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
        if s not in players:
            players[s] = Player((25, 10))
        if data[s]['action'] and data[s]['action'][0] == 'move':
            # TODO: deal with data type loss on Server() level
            x, y = data[s]['action'][1]
            players[s].move((int(x), int(y)))
    # Generate views for players
    for s in data.keys():
        player = players[s]
        radius = 12
        player_view = view.generate(
            player.get_coordinates(),
            radius,
            player.get_eyesight()
        )
        chat_log = chat.get_log(10)
        new_data[s] = (player_view, chat_log)
    server.set_data(new_data)
    time.sleep(time.clock() - clock + 0.5)
    server.send()
