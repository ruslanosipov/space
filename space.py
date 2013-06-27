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
action = None  # interaction with the world

while True:
    client.send({'action': action})
    action = None
    view_field, chat_msgs = client.receive()
    view_field = packet.decode(view_field)
    chat_msgs = packet.decode(chat_msgs)
    chat.add(chat_msgs)

    events = event.get(evt_mode)
    evt_mode, evt, evt_arg = events if events else (evt_mode, None, None)
    if evt == 'quit':
        print 'Quiting...'
        break
    if evt == 'move':
        action = (evt, evt_arg)

    surface = ui.compose(view_field, chat_msgs)
    display.draw(surface)
    display.update()
