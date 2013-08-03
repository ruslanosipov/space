#!/usr/bin/env python

import time
import sys
from ConfigParser import ConfigParser

from lib.server import Server
from lib.chatserver import ChatServer
from lib import misc

from lib.exterior.level5d import Level5D
from lib.exterior.view import ExteriorView

config = ConfigParser()
config.read('config.ini')
port = config.getint('server', 'port')

ext_level = Level5D()
ext_view = ExteriorView(ext_level)
chat = ChatServer()

server = Server(port)
server.listen()

players = {}
spaceships = {}

spaceship = misc.add_spaceship(
    'Enterprise', (0, 0, 10, 10),
    (24, 2), ext_level)
spaceships['Enterprise'] = spaceship
spaceship = misc.add_spaceship(
    'Galactica', (0, 0, 16, 16),
    (7, 2), ext_level)
spaceships['Galactica'] = spaceship

try:
    while True:
        clock = time.clock()
        server.receive()
        data = server.get_data()
        new_data = {}
        # Process data received from players
        for s in data.keys():
            if not data[s]:
                continue
            for evt, arg in data[s]:
                msg = None
                if s in players:
                    player = players[s]
                if evt == 'connect' and s not in players:
                    name, spaceship = arg
                    spaceship = spaceships[spaceship]
                    player = misc.add_player(name, spaceship)
                    players[s] = player
                spaceship = player.get_interior().get_spaceship()
                if not player.is_alive():
                    continue
                int_level = player.get_interior()
                if player.is_pilot() and not spaceship.is_alive():
                    continue
                if evt == 'activate':
                    dx, dy = map(int, arg)
                    x, y = player.get_coords()
                    msg = misc.activate_obj(
                        (x + dx, y + dy),
                        int_level,
                        player)
                elif evt == 'pickup':
                    dx, dy = map(int, arg)
                    x, y = player.get_coords()
                    msg = misc.pick_up_obj(player, (x + dx, y + dy), int_level)
                elif evt == 'inventory':
                    msg = misc.inventory(player)
                elif evt == 'move':
                    dx, dy = map(int, arg)
                    x, y = player.get_coords()
                    msg = misc.move(player, (x + dx, y + dy), int_level, chat)
                elif evt == 'rotate':
                    spaceship.rotate_pointer(int(arg))
                elif evt == 'accelerate':
                    spaceship.accelerate(arg)
                elif evt == 'ext_fire':
                    misc.exterior_fire(
                        spaceship.get_coords(),
                        spaceship.get_pointer(),
                        ext_level)
                elif evt == 'target':
                    msg = misc.set_target(player, int_level)
                elif evt == 'int_fire':
                    msg = misc.interior_fire(player, int_level, chat)
                elif evt == 'say':
                    chat.add_single('public', "%s: %s" % (name, arg), 0)
                elif evt == 'look':
                    dx, dy = map(int, arg)
                    x, y = player.get_coords()
                    msg = misc.look((x + dx, y + dy), int_level)
                elif evt == 'unpilot':
                    msg = "You are done piloting the spaceship..."
                    player.set_pilot()
                elif evt == 'equip':
                    msg = misc.equip_item(player, arg)
                elif evt == 'drop':
                    msg = misc.drop_item(player, arg)
                if msg is not None:
                    chat.add_single(player, msg, 1)
        # Let the world process one step
        ext_level.update()
        # Generate views for players
        for s in data.keys():
            player = players[s]
            spaceship = player.get_interior().get_spaceship()
            int_radius = 11
            ext_radius = 11
            if not player.is_pilot():
                view = player.get_interior().get_spaceship().get_view()
                view, colors = view.generate(
                    player.get_coords(),
                    int_radius,
                    player.get_sight(),
                    player.get_target())
                status_bar = ""
            else:
                view, colors = ext_view.generate(
                    spaceship.get_coords(),
                    ext_radius,
                    ext_radius,
                    spaceship.get_abs_pointer())
                status_bar = "SPD: %s" % spaceship.get_speed()
            chat_log = chat.get_recent_for_recipient(player)
            new_data[s] = (
                '\n'.join(view),
                colors,
                chat_log,
                player.is_pilot(),
                status_bar)
        server.set_data(new_data)
        time.sleep(time.clock() - clock + 0.02)
        server.send()
except KeyboardInterrupt:
    print "Keyboard interrupt detected, exiting..."
    server.close()
    sys.exit(0)
