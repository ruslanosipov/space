#!/usr/bin/env python

from ConfigParser import ConfigParser

from lib.chatclient import ChatClient
from lib.client import Client
from lib.display import Display
from lib.ui import UI
from lib import event

config = ConfigParser()
config.read('config.ini')
host = config.get('server', 'host')
port = config.getint('server', 'port')
name = config.get('player', 'name')
spaceship = config.get('player', 'spaceship')

chat = ChatClient()
client = Client(host, port)
display = Display()
ui = UI()

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
ui.set_default_colors(int_colors, ext_colors)

evt_mode, evt_mode_desc = 'normal', ''
action = ('connect', (name, spaceship))
require_arg = False
queued_evt = False
prompt = ''

while True:
    if action and not require_arg:
        client.send(action)
        action = False
    view_field, colors, chat_msgs, is_pilot, status_bar, top_status_bar \
        = client.receive()[-1]
    if is_pilot:
        evt_mode = 'pilot'
    elif not is_pilot and evt_mode == 'pilot':
        evt_mode = 'normal'
    view_field = view_field.split('\n')
    if len(chat_msgs):
        chat.add_multiple(chat_msgs)

    events = event.get(evt_mode)
    evt_mode, evt, evt_arg = events if events else (evt_mode, None, None)
    if evt_mode == 'normal' and len(evt_mode_desc):
        evt_mode_desc = ''
    if evt == 'quit':
        print 'Quiting...'
        break
    elif evt == 'arg' and require_arg:
        action = (action, evt_arg) if evt_arg else 0
        evt_mode_desc = ''
        require_arg = False
    elif evt == 'activate':
        action = evt
        evt_mode_desc = 'Activate.. (direction)'
        require_arg = True
    elif evt == 'look':
        evt_mode_desc = 'Look... (direction)'
        action = (evt, evt_arg)
    elif evt == 'look_done':
        evt_mode_desc = ''
        action = (evt, evt_arg)
    elif evt == 'insert':
        prompt += evt_arg
    elif evt == 'backspace' and prompt:
        prompt = prompt[: - evt_arg]
    elif evt == 'return' and prompt:
        action = (queued_evt, prompt)
        queued_evt = None
        prompt, evt_mode, evt_mode_desc = '', 'normal', ''
    elif evt in ['say', 'equip', 'drop', 'unequip']:
        if evt == 'say':
            evt_mode_desc = 'Say...'
        elif evt == 'equip':
            evt_mode_desc = 'Equip... (item, slot)'
        elif evt == 'drop':
            evt_mode_desc = 'Drop... (item name)'
        elif evt == 'unequip':
            evt_mode_desc = 'Unequip... (slot)'
        queued_evt = evt
    elif (evt, evt_arg) != (None, None):
        action = (evt, evt_arg)

    surface = ui.compose(
        view_field, colors, chat.get_log(), prompt,
        evt_mode, evt_mode_desc, status_bar, top_status_bar)
    display.draw(surface)
    display.update()
