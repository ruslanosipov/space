#!/usr/bin/env python

import time
import sys
from ConfigParser import ConfigParser

from lib.server import Server
from lib.chatserver import ChatServer
from lib import misc

from lib.interior.level3d import Level3D
from lib.interior.view import InteriorView
from lib.exterior.view import ExteriorView
from lib.exterior.level5d import Level5D

config = ConfigParser()
config.read('config.ini')
port = config.getint('server', 'port')

tiles_map = open('dat/maps/spaceship_tiles.txt', 'rb').read()
items_map = open('dat/maps/spaceship_items.txt', 'rb').read()
level_definition = misc.load_interior_level(tiles_map, items_map)
txt = open('dat/obj_definitions.txt', 'rb').read()
obj_definitions = misc.load_obj_definitions(txt)
int_level = Level3D(level_definition, obj_definitions)
ext_level = Level5D()
int_view = InteriorView(int_level)
ext_view = ExteriorView(ext_level)
chat = ChatServer()

server = Server(port)
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
            if not data[s]:
                continue
            for evt, arg in data[s]:
                msg = None
                if s in players:
                    player = players[s]
                if evt == 'connect' and s not in players:
                    player = misc.add_player(arg, (25, 10), int_level)
                    players[s] = player
                    spaceship = ext_level.add_spaceship(
                        'USS Enterprise',
                        (0, 0, 13, 13))
                spaceship = player.get_spaceship()
                if player.get_spaceship() is not None:
                    spaceship = player.get_spaceship()
                if not player.is_alive():
                    continue
                if player.get_spaceship() and not spaceship.is_alive():
                    continue
                if evt == 'activate':
                    dx, dy = map(int, arg)
                    x, y = player.get_coords()
                    msg = misc.activate_obj((x + dx, y + dy), int_level)
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
                    spaceship.accelerate(float(arg))
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
                    chat.add_single('all', arg, name=player.get_name())
                elif evt == 'look':
                    dx, dy = map(int, arg)
                    x, y = player.get_coords()
                    msg = misc.look((x + dx, y + dy), int_level)
                elif evt == 'fly':
                    if player.get_spaceship() is None:
                        msg = "You are piloting the spaceship now..."
                        for spaceship in ext_level.get_spaceships():
                            player.set_spaceship(spaceship)
                            break
                    else:
                        msg = "You are done piloting the spaceship..."
                        player.set_spaceship()
                if msg is not None:
                    chat.add_single(player.get_name(), msg)
        # Let the world process one step
        ext_level.update()
        # Generate views for players
        for s in data.keys():
            player = players[s]
            spaceship = player.get_spaceship()
            int_radius = 11
            ext_radius = 12
            if spaceship is None:
                view = int_view.generate(
                    player.get_coords(),
                    int_radius,
                    player.get_sight(),
                    player.get_target())
            else:
                view = ext_view.generate(
                    spaceship.get_coords(),
                    ext_radius,
                    ext_radius,
                    spaceship.get_abs_pointer())
            chat_log = chat.get_recent(player.get_name())
            new_data[s] = ('\n'.join(view), '\n'.join(chat_log))
        server.set_data(new_data)
        time.sleep(time.clock() - clock + 0.02)
        server.send()
except KeyboardInterrupt:
    print "Keyboard interrupt detected, exiting..."
    server.close()
    sys.exit(0)
