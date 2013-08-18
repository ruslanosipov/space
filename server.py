#!/usr/bin/env python

from ConfigParser import ConfigParser

from lib.chatserver import ChatServer
from lib import server
from lib import misc

from lib.exterior.level5d import Level5D
from lib.exterior.view import ExteriorView


class GameServer(object):

    def __init__(self):
        self.ext_level = Level5D()
        self.ext_view = ExteriorView(self.ext_level)
        self.chat = ChatServer()

        self.clients = {}
        self.players = {}
        self.spaceships = {}

        spaceship = misc.add_spaceship(
            'Enterprise', (0, 0, 10, 10),
            (24, 2), self.ext_level)
        self.spaceships['Enterprise'] = spaceship
        spaceship = misc.add_spaceship(
            'Galactica', (0, 0, 16, 16),
            (7, 2), self.ext_level)
        self.spaceships['Galactica'] = spaceship
        self.requests = False
        self.command_factory = False

    def main(self):
        if not self.requests:
            return
        requests = self.requests.get_requests()
        for client, data in requests.items():
            if not data:
                status = self.clients[client]['top_status_bar']
                continue
            for evt, arg in data:
                if client in self.players:
                    player = self.players[client]
                if evt == 'connect' and client not in self.players:
                    name, spaceship = arg
                    spaceship = self.spaceships[spaceship]
                    player = misc.add_player(name, spaceship)
                    self.players[client] = player
                    self.clients[client] = {
                        'view': '',
                        'colors': {},
                        'top_status_bar': '',
                        'bottom_status_bar': '',
                        'is_pilot': False}
                    status = ''
                spaceship = player.get_interior().get_spaceship()
                if not player.is_alive():
                    continue
                int_level = player.get_interior()
                if player.is_pilot() and not spaceship.is_alive():
                    continue
                if evt == 'activate':
                    dx, dy = map(int, arg)
                    x, y = player.get_coords()
                    status = misc.activate_obj(
                        (x + dx, y + dy),
                        int_level,
                        player)
                elif evt == 'pickup':
                    dx, dy = map(int, arg)
                    x, y = player.get_coords()
                    status = misc.pick_up_obj(player, (x + dx, y + dy),
                                              int_level)
                elif evt == 'move':
                    dx, dy = map(int, arg)
                    x, y = player.get_coords()
                    status = misc.move(player, (x + dx, y + dy),
                                       int_level, self.chat)
                elif evt == 'rotate':
                    spaceship.rotate_pointer(int(arg))
                elif evt == 'accelerate':
                    spaceship.accelerate(arg)
                elif evt == 'ext_fire':
                    misc.exterior_fire(
                        spaceship.get_coords(),
                        spaceship.get_pointer(),
                        self.ext_level)
                elif evt == 'int_fire':
                    status = misc.interior_fire(player, int_level, self.chat)
                elif evt == 'say':
                    self.chat.add_single('public', "%s: %s" % (name, arg), 0)
                elif evt == 'unpilot':
                    status = "You are done piloting the spaceship..."
                    player.set_pilot()
                elif evt == 'equip':
                    if ', ' in arg:
                        item, slot = arg.split(', ')
                    else:
                        item, slot = arg, 'hands'
                    status = misc.equip_item(player, item, slot)
                elif evt == 'unequip':
                    status = misc.unequip_item(player, arg)
                elif evt == 'drop':
                    status = misc.drop_item(player, arg)
        # Let the world process one step
        self.ext_level.update()
        for uid, data in requests.items():
            if uid not in self.players.keys():
                continue
            player = self.players[uid]
            int_radius = 11
            ext_radius = 11
            spaceship = player.get_interior().get_spaceship()
            int_level = player.get_interior()
            if not player.is_pilot():
                view = player.get_interior().get_spaceship().get_view()
                visible_tiles = view.visible_tiles(
                    player.get_coords(),
                    int_radius,
                    player.get_sight())
            for evt, arg in data:
                msg = None
                if evt == 'inventory':
                    msg = misc.inventory(player)
                elif evt == 'equipment':
                    msg = misc.equipment(player)
                elif evt == 'target':
                    status = misc.set_target(player, int_level)
                elif evt == 'look':
                    status = misc.look(player, (0, 0),
                                       int_level, visible_tiles)
                elif evt == 'look_dir':
                    dx, dy = map(int, arg)
                    status = misc.look(player, (dx, dy),
                                       int_level, visible_tiles)
                elif evt == 'look_done':
                    player.set_looking()
                if msg is not None:
                    self.chat.add_single(player, msg, 1)
            # Generate views for players
            if not player.is_pilot():
                view = player.get_interior().get_spaceship().get_view()
                view, colors = view.generate(
                    player.get_coords(),
                    int_radius,
                    player.get_sight(),
                    visible_tiles,
                    player.get_target(),
                    player.get_look_coords())
                # create status bar
                health = str(player.get_health())
                status_bar = "HP %s%s " % (' ' * (3 - len(health)), health)
                if player.get_equipment('hands') is not None:
                    weapon = player.get_equipment('hands').get_name()
                    status_bar += "(%s) " % weapon
            else:
                view, colors = self.ext_view.generate(
                    spaceship.get_coords(),
                    ext_radius,
                    ext_radius,
                    spaceship.get_abs_pointer())
                # create status bar
                speed = str(spaceship.get_speed())
                status_bar = "SPD %s%s " % (' ' * (3 - len(speed)), speed)
                health = str(spaceship.get_health())
                status_bar += "HP %s%s " % (' ' * (3 - len(health)), health)
            ver = "v0.2.1-alpha"
            if status[- len(ver):] != ver:
                status += ' ' * (80 - len(status) - len(ver)) + ver
            chat_log = self.chat.get_recent_for_recipient(player)
            if len(chat_log):
                self.command_factory.callCommand(uid, 'add_chat_messages',
                                                 chat_log)
            if view != self.clients[uid]['view'] or \
                    colors != self.clients[uid]['colors']:
                self.clients[uid]['view'] = view
                self.clients[uid]['colors'] = colors
                self.command_factory.callCommand(uid, 'set_view', view, colors)
            if player.is_pilot() != self.clients[uid]['is_pilot']:
                self.clients[uid]['is_pilot'] = player.is_pilot()
                self.command_factory.callCommand(uid, 'set_pilot',
                                                 player.is_pilot())
            if status_bar != self.clients[uid]['bottom_status_bar']:
                self.clients[uid]['bottom_status_bar'] = status_bar
                self.command_factory.callCommand(uid, 'set_bottom_status_bar',
                                                 status_bar)
            if status != self.clients[uid]['top_status_bar']:
                self.clients[uid]['top_status_bar'] = status
                self.command_factory.callCommand(uid, 'set_top_status_bar',
                                                 status)

    def set_command_factory(self, command_factory):
        self.command_factory = command_factory

    def set_requests(self, requests):
        self.requests = requests


config = ConfigParser()
config.read('config.ini')
port = config.getint('server', 'port')
server.main(GameServer(), port, 0.02)
