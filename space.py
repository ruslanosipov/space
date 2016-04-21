#!/usr/bin/env python

"""Space client.

Usage:
    space.py --host=<host> [--port=<port>] [--debug]
    space.py --help | -h

Options:
    --host <host>   Host to connect to.
    --port <port>   Port to connect to [default: 12345].
    --debug         Expand logging level.
    --help -h       Show this screen.
"""

from ConfigParser import ConfigParser
import logging

import docopt

from lib import client
from lib.chatclient import ChatClient
from lib.display import Display
from lib.event import Event
from lib.ui import UI


class GameClient(object):

    def __init__(self, config):
        name = config.get('player', 'name')
        spaceship = config.get('player', 'spaceship')

        self.chat = ChatClient()
        self.display = Display()
        self.ui = UI()
        self.event = Event()
        int_colors, ext_colors = {}, {}
        obj_defs = open('dat/int_obj_colors.txt', 'rb').read().split('\n')
        for line in obj_defs:
            if len(line):
                char, color = line.split('|')
                int_colors[char] = eval(color)
        obj_defs = open('dat/ext_obj_colors.txt', 'rb').read().split('\n')
        for line in obj_defs:
            if len(line):
                char, color = line.split('|')
                ext_colors[char] = eval(color)
        self.ui.set_default_colors(int_colors, ext_colors)

        self.evt_mode = 'normal'
        self.evt, self.evt_arg = 'connect', (name, spaceship)
        self.tmp_arg = None
        self.require_arg, self.queued_evt = False, False
        self.command = None

    def main(self):
        events = self.event.get()
        if events:
            evt, evt_arg = events
            self.evt_mode = self.event.get_mode()
            logging.debug("Received event. Mode: {}, event: {}, args: {}.".format(
                self.evt_mode, evt, evt_arg))

            if evt == 'quit':
                self.command.stop()

            if self.evt_mode == 'insert':
                self._process_insert(evt, evt_arg)
            else:
                self._process_event(evt, evt_arg)

        if self.evt is not None and not self.require_arg:
            command = getattr(self.command, 'queue_action')
            command(self.evt, self.evt_arg)
            self.evt, self.evt_arg = None, None

        self._draw_screen()

    def _process_event(self, evt, evt_arg):
        if evt == 'arg' and self.require_arg:
            if evt_arg:
                self.evt, self.evt_arg = (self.evt, evt_arg)
            else:
                if self.evt in ['equip', 'drop']:
                    d = self.command.callCommand('query_inventory')
                    d.addCallback(getattr(self, 'set_inventory'))
                elif self.evt in ['unequip']:
                    d = self.command.callCommand('query_equipment')
                    d.addCallback(getattr(self, 'set_equipment'))
                self.evt, self.evt_arg = None, None
            self.ui.set_evt_mode_desc('')
            self.require_arg = False
            if self.evt in ['say']:
                self.ui.set_prompt('')
            self.event.collapse_current_layout()
        elif evt_arg is None:
            self.evt = evt
            self.require_arg = True
            self.ui.set_evt_mode_desc(evt.capitalize() + '...')
        elif evt in ['inventory', 'equipment']:
            d = self.command.callCommand('query_%s' % evt)
            d.addCallback(getattr(self, 'set_%s' % evt))
        elif evt == 'reset_right_pane':
            self.event.collapse_current_layout()
            self.ui.set_mode()
        else:
            self.evt, self.evt_arg = evt, evt_arg

        if evt in ['equip', 'drop', 'unequip'] and evt_arg is None:
            getattr(self, 'setup_%s' % evt)()

    def _process_insert(self, evt, evt_arg):
        if evt == 'insert_type':
            self.ui.set_prompt(evt_arg)
        else:
            self.evt = evt
            self.ui.set_evt_mode_desc(evt.capitalize() + '...')
            self.require_arg = True

    def _draw_screen(self):
        top_bar, left_pane, right_pane, bottom_bar = self.ui.compose()
        self.display.draw(top_bar, left_pane, right_pane, bottom_bar)
        self.display.update()

    #--------------------------------------------------------------------------
    # state accessors

    def add_chat_messages(self, messages):
        self.chat.add_multiple(messages)
        self.ui.set_chat_log(self.chat.get_log())

    def set_bottom_status_bar(self, text):
        self.ui.set_bottom_status_bar(text)

    def set_command(self, command):
        self.command = command

    def set_equipment(self, equipment):
        self.ui.set_equipment(equipment)
        self.evt_mode = 'equipment'
        self.event.set_mode('eqp')
        self.ui.set_mode('equipment')

    def set_inventory(self, inventory):
        self.ui.set_inventory(inventory)
        self.evt_mode = 'inventory'
        self.event.set_mode('inv')
        self.ui.set_mode('inventory')

    def set_look_pointer(self, (x, y)):
        self.ui.set_look_pointer((x, y))

    def set_pilot(self, is_pilot):
        if is_pilot:
            self.event.set_mode('pilot')
        elif not is_pilot and self.evt_mode == 'pilot':
            self.event.set_mode('normal')
        self.ui.set_pilot_mode()

    def set_target(self, (x, y)):
        self.ui.set_target((x, y))

    def set_top_status_bar(self, text):
        ver = 'v0.3.1-alpha'
        text += ' ' * (80 - len(text) - len(ver)) + ver
        self.ui.set_top_status_bar(text)

    def set_view(self, view, colors):
        self.ui.set_view_field(view)
        self.ui.set_colors(colors)

    def setup_drop(self):
        inventory = self.ui.get_inventory()
        inventory_keys = inventory.keys()
        keys = self.event.extend_current_layout('arg', inventory_keys)
        inventory_keys = [
            '%s %s' % (k, i) for k, i in zip(keys, inventory_keys)]
        self.ui.set_inventory(dict(zip(inventory_keys, inventory.values())))

    def setup_equip(self):
        inventory = self.ui.get_inventory()
        inventory_keys = inventory.keys()
        keys = self.event.extend_current_layout('arg', inventory_keys)
        inventory_keys = [
            '%s %s' % (k, i) for k, i in zip(keys, inventory_keys)]
        self.ui.set_inventory(dict(zip(inventory_keys, inventory.values())))

    def setup_unequip(self):
        equipment = self.ui.get_equipment()
        equipment_keys = equipment.keys()
        keys = self.event.extend_current_layout('arg', equipment_keys)
        equipment_keys = [
            '%s %s' % (k, e) for k, e in zip(keys, equipment_keys)]
        self.ui.set_equipment(dict(zip(equipment_keys, equipment.values())))

    def unset_look_pointer(self):
        self.ui.set_look_pointer(None)

    def unset_target(self):
        self.ui.set_target(None)

def main(arguments):
    level = logging.DEBUG if arguments['--debug'] else logging.INFO
    logging.basicConfig(level=level)

    conf = ConfigParser()
    conf.read('config.ini')
    host = arguments['--host']
    port = int(arguments['--port'])
    client.main(GameClient(conf), host, port, timeout=0.02)

if __name__ == '__main__':
    main(docopt.docopt(__doc__))
