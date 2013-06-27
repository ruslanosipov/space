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

while True:
    client.send({})
    view_field, chat_msgs = client.receive()
    view_field = packet.decode(view_field)
    chat_msgs = packet.decode(chat_msgs)

    chat.add(chat_msgs)

    surface = ui.compose(view_field, chat_msgs)
    evt = event.get()
    if evt == 'quit':
        print 'Quiting...'
        break

    display.draw(surface)
    display.update()
