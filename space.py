#!/usr/bin/env python

from ConfigParser import ConfigParser

from lib.chatclient import ChatClient
from lib.display import Display
from lib.ui import UI
from lib import event
from lib import client


class GameClient(object):

    def __init__(self, config):
        name = config.get('player', 'name')
        spaceship = config.get('player', 'spaceship')

        self.chat = ChatClient()
        self.display = Display()
        self.ui = UI()
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

        self.evt_mode, self.evt_mode_desc = 'normal', ''
        self.action = ('connect', (name, spaceship))
        self.arg_type = 'tuple_of_str'
        self.require_arg = False
        self.queued_evt = False
        self.prompt = ''
        ver = 'v0.3.0-alpha'
        self.top_status_bar = ' ' * (80 - len(ver)) + ver
        self.bottom_status_bar = ''
        self.view_field, self.colors = False, {}
        self.command = None
        self.look_pointer, self.target = None, None
        self.fps = 50
        self.blinker = 0

    def main(self):
        if self.action and not self.require_arg:
            command = getattr(self.command, 'queue_' + self.arg_type)
            command(self.action[0], self.action[1])
            self.action, self.arg_type = False, False
        if not self.view_field:
            return
        events = event.get(self.evt_mode)
        if events:
            self.evt_mode, evt, evt_arg, self.arg_type = events
        else:
            evt, evt_arg = None, None
        if self.evt_mode == 'normal' and len(self.evt_mode_desc):
            self.evt_mode_desc = ''
        if evt == 'quit':
            self.command.stop()
        elif evt == 'arg' and self.require_arg:
            self.action = (self.action, evt_arg) if evt_arg else 0
            self.evt_mode_desc = ''
            self.require_arg = False
        elif evt == 'activate':
            self.action = evt
            self.evt_mode_desc = 'Activate.. (direction)'
            self.require_arg = True
        elif evt == 'look':
            self.evt_mode_desc = 'Look... (direction)'
            self.action = (evt, evt_arg)
        elif evt == 'look_done':
            self.evt_mode_desc = ''
            self.action = (evt, evt_arg)
        elif evt == 'insert':
            self.prompt += evt_arg
        elif evt == 'backspace' and self.prompt:
            self.prompt = self.prompt[: - evt_arg]
        elif evt == 'return' and self.prompt:
            self.action = (self.queued_evt, self.prompt)
            self.queued_evt = False
            self.prompt, self.evt_mode, self.evt_mode_desc = '', 'normal', ''
        elif evt in ['say', 'equip', 'drop', 'unequip']:
            if evt == 'say':
                self.evt_mode_desc = 'Say...'
            elif evt == 'equip':
                self.evt_mode_desc = 'Equip... (item, slot)'
            elif evt == 'drop':
                self.evt_mode_desc = 'Drop... (item name)'
            elif evt == 'unequip':
                self.evt_mode_desc = 'Unequip... (slot)'
            self.queued_evt = evt
        elif (evt, evt_arg) != (None, None):
            self.action = (evt, evt_arg)

        self.blinker = self.blinker + 1 if self.blinker < self.fps else 0
        surface = self.ui.compose(
            self.view_field, self.colors,
            self.chat.get_log(), self.prompt,
            self.evt_mode, self.evt_mode_desc,
            self.bottom_status_bar, self.top_status_bar,
            self.target if self.blinker < self.fps / 2 else None,
            self.look_pointer if self.blinker < self.fps / 2 else None)
        self.display.draw(surface)
        self.display.update()

    #--------------------------------------------------------------------------
    # state accessors

    def add_chat_messages(self, messages):
        self.chat.add_multiple(messages)

    def set_bottom_status_bar(self, text):
        self.bottom_status_bar = text

    def set_command(self, command):
        self.command = command

    def set_look_pointer(self, (x, y)):
        self.look_pointer = (x, y)
        self.blinker = 0

    def set_pilot(self, is_pilot):
        if is_pilot:
            self.evt_mode = 'pilot'
        elif not is_pilot and self.evt_mode == 'pilot':
            self.evt_mode = 'normal'

    def set_target(self, (x, y)):
        self.target = (x, y)
        self.blinker = 0

    def set_top_status_bar(self, text):
        ver = 'v0.3.0-alpha'
        text += ' ' * (80 - len(text) - len(ver)) + ver
        self.top_status_bar = text

    def set_view(self, view, colors):
        self.view_field = view
        self.colors = colors

    def unset_look_pointer(self):
        self.look_pointer = False

    def unset_target(self):
        self.target = False

config = ConfigParser()
config.read('config.ini')
host = config.get('server', 'host')
port = config.getint('server', 'port')
client.main(GameClient(config), host, port, timeout=0.02)
