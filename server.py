#!/usr/bin/env python

"""Space server.

Usage:
    server.py [--port=<port>] [--debug]
    server.py --help | -h

Options:
    --port <port>   Open at port [default: 12345].
    --debug         Extend log level.
    --help -h       Show this screen.
"""

import logging

import docopt

from lib import misc
from lib import server
from lib.chatserver import ChatServer
from lib.exterior.level5d import Level5D
from lib.exterior import view as exterior_view
from lib.interior import view as interior_view


class GameServer(object):

    def __init__(self):
        self.ext_level = Level5D()
        self.chat = ChatServer()

        self.clients = {}
        self.players = {}
        self.spaceships = {}

        spaceship = misc.add_spaceship(
            'Enterprise', (0, 0, 10, 10),
            (14, 4), self.ext_level)
        self.spaceships['Enterprise'] = spaceship
        spaceship = misc.add_spaceship(
            'Galactica', (0, 0, 16, 16),
            (5, 2), self.ext_level)
        self.spaceships['Galactica'] = spaceship
        self.requests = False
        self.command_factory = False

    def main(self):
        if not self.requests:
            return
        requests = self.requests.get_requests()

        # first: process players' actions which affect the world
        for uid, data in requests.items():
            if not data:
                continue
            for evt, arg in data:
                logging.debug(
                    "Received event '{}' with args '{}' from client {}.".format(
                        evt, arg, uid))

                if uid in self.players:
                    player, client = self.players[uid], self.clients[uid]
                if evt == 'connect' and uid not in self.players:
                    name, spaceship = arg
                    spaceship = self.spaceships[spaceship]
                    player = misc.add_player(name, spaceship)
                    self.players[uid] = player
                    # I keep track of previous and current status bars,
                    # view a list as a mutable tuple (old, new)
                    self.clients[uid] = {
                        'view': '',
                        'colors': {},
                        'top_status_bar': ['', ''],
                        'bottom_status_bar': ['', ''],
                        'is_pilot': False,
                        'target': [None, None],
                        'look_coords': [None, None]}
                    client = self.clients[uid]

                spaceship = player.interior.spaceship
                if not player.is_alive:
                    continue
                int_level = player.interior
                if player.is_pilot and not spaceship.is_alive:
                    continue
                if evt == 'activate':
                    dx, dy = arg
                    x, y = player.coords
                    client['top_status_bar'][-1] = misc.activate_obj(
                        (x + dx, y + dy),
                        int_level, player)
                elif evt == 'pickup':
                    dx, dy = arg
                    x, y = player.coords
                    client['top_status_bar'][-1] = misc.pick_up_obj(
                        player, (x + dx, y + dy),
                        int_level)
                elif evt == 'move':
                    dx, dy = arg
                    x, y = player.coords
                    client['top_status_bar'][-1] = misc.move(
                        player, (x + dx, y + dy),
                        int_level, self.chat)
                elif evt == 'rotate':
                    spaceship.rotate_pointer(arg)
                elif evt == 'accelerate':
                    spaceship.accelerate(arg)
                elif evt == 'ext_fire':
                    misc.exterior_fire(
                        spaceship.coords,
                        spaceship.get_pointer(),
                        self.ext_level)
                elif evt == 'int_fire':
                    client['top_status_bar'][-1] = misc.interior_fire(
                        player, int_level, self.chat)
                elif evt == 'say':
                    self.chat.add_single(
                        'public', "%s: %s" % (player.name, arg), 0)
                elif evt == 'unpilot':
                    client['top_status_bar'][-1] = \
                        "You are done piloting the spaceship..."
                    player.toggle_pilot()
                elif evt == 'equip':
                    client['top_status_bar'][-1] = misc.equip_item(
                        player, arg)
                    self.command_factory.callCommand(
                        uid, 'set_equipment', player.equipment)
                elif evt == 'unequip':
                    client['top_status_bar'][-1] = misc.unequip_item(
                        player, arg)
                    self.command_factory.callCommand(
                        uid, 'set_equipment', player.equipment)
                elif evt == 'drop':
                    client['top_status_bar'][-1] = misc.drop_item(player, arg)
                    self.command_factory.callCommand(
                        uid, 'set_inventory', player.inventory)


        # second: let the world process one tick
        self.ext_level.update()

        # third: process insignificant actions and generate views
        for uid, data in requests.items():
            if uid not in self.players.keys():
                continue
            player, client = self.players[uid], self.clients[uid]
            int_radius = 11
            ext_radius = 11
            spaceship = player.interior.spaceship
            int_level = player.interior
            if not player.is_pilot:
                visible_tiles = interior_view.find_visible_tiles(
                    player.interior,
                    player.coords,
                    int_radius,
                    player.sight)
            for evt, arg in data:
                msg = None
                if evt == 'target':
                    client['top_status_bar'][-1] = misc.set_target(
                        player, int_level, visible_tiles)
                elif evt == 'look':
                    client['top_status_bar'][-1] = misc.look(
                        player, (0, 0),
                        int_level, visible_tiles)
                elif evt == 'look_dir':
                    dx, dy = arg
                    _tmp = misc.look(
                        player, (dx, dy),
                        int_level, visible_tiles)
                    if _tmp:
                        client['top_status_bar'][-1] = _tmp
                elif evt == 'look_done':
                    player.toggle_looking()
                if msg is not None:
                    self.chat.add_single(player, msg, 1)
            # generate a view for player or spaceship
            if not player.is_pilot:
                view, colors, target, look_coords = \
                        interior_view.generate_interior_view(
                                player.interior,
                                player.coords,
                                int_radius,
                                player.sight,
                                visible_tiles,
                                player.target,
                                player.look_coords)
                client['target'][-1] = target
                client['look_coords'][-1] = look_coords
                # create bottom status bar
                hp = str(player.health)
                client['bottom_status_bar'][-1] = \
                    "HP %s%s " % (' ' * (3 - len(hp)), hp)
                if player.get_equipment_slot('hands') is not None:
                    weapon = player.get_equipment_slot('hands').name
                    client['bottom_status_bar'][-1] += "(%s) " % weapon
            else:
                view, colors = exterior_view.generate_exterior_view(
                        self.ext_level,
                        spaceship.coords,
                        ext_radius,
                        ext_radius,
                        spaceship.get_abs_pointer())
                # create bottom status bar
                spd = str(spaceship.speed)
                client['bottom_status_bar'][-1] = \
                    "SPD %s%s " % (' ' * (3 - len(spd)), spd)
                hp = str(spaceship.health)
                client['bottom_status_bar'][-1] += \
                    "HP %s%s " % (' ' * (3 - len(hp)), hp)
                client['bottom_status_bar'][-1] += \
                    "POS%s " % ''.join((
                        ' ' * (3 - len(str(coord))) + str(coord)
                        for coord in spaceship.coords))
            recent_chat_msgs = self.chat.get_recent_for_recipient(player)
            if len(recent_chat_msgs):
                self.command_factory.callCommand(
                    uid, 'add_chat_messages', recent_chat_msgs)
            if view != client['view'] or \
                    colors != client['colors']:
                client['view'] = view
                client['colors'] = colors
                self.command_factory.callCommand(uid, 'set_view', view, colors)
            if player.is_pilot != client['is_pilot']:
                client['is_pilot'] = player.is_pilot
                self.command_factory.callCommand(
                    uid, 'set_pilot',
                    player.is_pilot)
            bar = client['bottom_status_bar']
            if bar[-1] != bar[0]:
                bar[0] = bar[1]
                self.command_factory.callCommand(
                    uid, 'set_bottom_status_bar',
                    bar[0])
                client['bottom_status_bar'] = bar
            bar = client['top_status_bar']
            if bar[-1] != bar[0]:
                bar[0] = bar[-1]
                self.command_factory.callCommand(
                    uid, 'set_top_status_bar',
                    bar[0])
                client['top_status_bar'] = bar
            if client['target'][-1] != client['target'][0]:
                client['target'][0] = client['target'][-1]
                if client['target'][0]:
                    self.command_factory.callCommand(
                        uid, 'set_target', client['target'][0])
                else:
                    self.command_factory.callCommand(uid, 'unset_target')
            if client['look_coords'][-1] != client['look_coords'][0]:
                client['look_coords'][0] = client['look_coords'][-1]
                if client['look_coords'][0]:
                    self.command_factory.callCommand(
                        uid, 'set_look_pointer', client['look_coords'][0])
                else:
                    self.command_factory.callCommand(uid, 'unset_look_pointer')

    #--------------------------------------------------------------------------
    # client accessors

    def get_equipment(self, player_uid):
        return self.players[player_uid].equipment

    def get_inventory(self, player_uid):
        return self.players[player_uid].inventory

    #--------------------------------------------------------------------------
    # accessors

    def set_command_factory(self, command_factory):
        self.command_factory = command_factory

    def set_requests(self, requests):
        self.requests = requests


def main(arguments):
    level = logging.DEBUG if arguments['--debug'] else logging.INFO
    logging.basicConfig(level=level)
    port = int(arguments['--port'])
    server.main(GameServer(), port, 0.02)

if __name__ == '__main__':
    main(docopt.docopt(__doc__))
