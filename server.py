#!/usr/bin/env python

import time

from lib.server import Server
from lib.display import Display
from lib.level import Level
from lib.view import View
from lib.ui import UI
from lib.chat import Chat

server = Server(12345)
level = Level('dat/spaceship.map')
view = View(level)
chat = Chat()

server.listen()

while True:
    clock = time.clock()
    server.receive()
    data = server.get_data()
    new_data = {}
    # TODO: process data received from clients
    for s in data.keys():
        x, y = 25, 10
        radius = 12
        eyesight = 11
        player_view = view.generate((x, y), radius, eyesight)
        chat_log = chat.get_log(10)
        new_data[s] = (player_view, chat_log)
    server.set_data(new_data)
    time.sleep(time.clock() - clock + 0.5)
    server.send()
