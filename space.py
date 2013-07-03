#!/usr/bin/env python

from lib.chat import ChatClient
from lib.client import Client
from lib.display import Display
from lib.ui import UI
from lib.utl import packet
from lib import event

chat = ChatClient()
client = Client('127.0.0.1', 12345)
display = Display()
ui = UI()

evt_mode = 'normal'
action = ('connect', 'player 1')
waiting_for_action_arg = 0
prompt = ''

while True:
    if action and not waiting_for_action_arg:
        client.send(action)
        action = 0
    view_field, chat_msgs = client.receive()[-1]
    view_field = packet.decode(view_field)
    chat_msgs = packet.decode(chat_msgs)
    if len(chat_msgs[0]):
        chat.add_multiple(chat_msgs)

    events = event.get(evt_mode)
    evt_mode, evt, evt_arg = events if events else (evt_mode, None, None)
    if evt == 'quit':
        print 'Quiting...'
        break
    elif evt == 'arg' and waiting_for_action_arg:
        action = (action, evt_arg) if evt_arg else 0
        waiting_for_action_arg = 0
    elif evt == 'activate':
        action = evt
        waiting_for_action_arg = 1
    elif evt == 'look':
        action = evt
        waiting_for_action_arg = 1
    elif evt == 'move':
        action = (evt, evt_arg)
    elif evt == 'target':
        action = (evt, evt_arg)
    elif evt == 'insert':
        prompt += evt_arg
    elif evt == 'backspace' and prompt:
        prompt = prompt[: - evt_arg]
    elif evt == 'return' and prompt:
        action = ('say', prompt)
        prompt, evt_mode = '', 'normal'

    surface = ui.compose(view_field, chat.get_log(), prompt, evt_mode)
    display.draw(surface)
    display.update()
