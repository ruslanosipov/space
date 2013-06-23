#!/usr/bin/env python

from lib.chat import Chat
from lib.client import Client
from lib.display import Display
from lib.event import Event
from lib.inputmgr import InputMgr
from lib.ui import UI
from lib.utl import packet

chat = Chat()
client = Client('www.example.com', 12345)
display = Display()
event = Event()
inputmgr = InputMgr()
ui = UI()

while True:
    client.send({})
    view_field, chat_msgs = client.receive()
    view_field = packet.decode(view_field)
    chat_msgs = packet.decode(chat_msgs)

    chat.add(chat_msgs)

    surface = ui.compose(view_field, chat_msgs)
    key = inputmgr.read()
    evt = event.receive(key)

    display.draw(surface)
