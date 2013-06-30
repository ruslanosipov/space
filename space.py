#!/usr/bin/env python

from lib.chat import Chat
from lib.client import Client
from lib.display import Display
from lib.ui import UI
from lib.utl import packet
from lib import event

chat = Chat()
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

    events = event.get(evt_mode)
    evt_mode, evt, evt_arg = events if events else (evt_mode, None, None)
    if evt == 'quit':
        print 'Quiting...'
        break
    if evt == 'arg' and waiting_for_action_arg:
        action = (action, evt_arg) if evt_arg else 0
        waiting_for_action_arg = 0
    if evt == 'activate':
        action = evt
        waiting_for_action_arg = 1
    if evt == 'move':
        action = (evt, evt_arg)
    if evt == 'insert':
        prompt += evt_arg
    if evt == 'backspace' and prompt:
        prompt = prompt[: - evt_arg]
    if evt == 'return' and prompt:
        action = ('say', prompt)
        prompt, evt_mode = '', 'normal'

    surface = ui.compose(view_field, chat_msgs, prompt)
    display.draw(surface)
    display.update()
