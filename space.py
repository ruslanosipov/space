#!/usr/bin/env python

from ConfigParser import ConfigParser

from lib.chatclient import ChatClient
from lib.client import Client
from lib.display import Display
from lib.interior.ui import UI
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

evt_mode = 'normal'
action = ('connect', (name, spaceship))
require_arg = False
prompt = ''

while True:
    if action and not require_arg:
        client.send(action)
        action = False
    view_field, chat_msgs = client.receive()[-1]
    view_field = view_field.split('\n')
    chat_msgs = chat_msgs.split('\n')
    if len(chat_msgs[0]):
        chat.add_multiple(chat_msgs)

    events = event.get(evt_mode)
    evt_mode, evt, evt_arg = events if events else (evt_mode, None, None)
    if evt == 'quit':
        print 'Quiting...'
        break
    elif evt == 'arg' and require_arg:
        action = (action, evt_arg) if evt_arg else 0
        require_arg = False
    elif evt == 'activate':
        action = evt
        require_arg = True
    elif evt == 'look':
        action = evt
        require_arg = True
    elif evt == 'fly':
        action = (evt, evt_arg)
        evt_mode = 'ship' if evt_mode == 'normal' else 'normal'
    elif evt == 'insert':
        prompt += evt_arg
    elif evt == 'backspace' and prompt:
        prompt = prompt[: - evt_arg]
    elif evt == 'return' and prompt:
        action = ('say', prompt)
        prompt, evt_mode = '', 'normal'
    elif evt == 'say':
        continue
    elif (evt, evt_arg) != (None, None):
        action = (evt, evt_arg)

    surface = ui.compose(view_field, chat.get_log(), prompt, evt_mode)
    display.draw(surface)
    display.update()
