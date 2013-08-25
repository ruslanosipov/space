from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.protocols.amp import AMP
from twisted.internet.task import LoopingCall
from copy import deepcopy

import commands


class Requests:

    def __init__(self):
        self.clients = {}

    def add_request(self, client, request):
        if client not in self.clients:
            self.clients[client] = []
        self.clients[client].append(request)

    def get_requests(self):
        requests = deepcopy(self.clients)
        for client in self.clients.keys():
            self.clients[client] = []
        return requests


class CommandProtocol(AMP):

    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.uid = str(id(self))
        self.factory.clients[self.uid] = self

    #--------------------------------------------------------------------------
    # responders

    def queue_int(self, action, arg):
        self.factory.requests.add_request(self.uid, (action, arg))
        return {}
    commands.QueueInt.responder(queue_int)

    def queue_str(self, action, arg):
        self.factory.requests.add_request(self.uid, (action, arg))
        return {}
    commands.QueueStr.responder(queue_str)

    def queue_tuple_of_int(self, action, arg1, arg2):
        self.factory.requests.add_request(self.uid, (action, (arg1, arg2)))
        return {}
    commands.QueueTupleOfInt.responder(queue_tuple_of_int)

    def queue_tuple_of_str(self, action, arg1, arg2):
        self.factory.requests.add_request(self.uid, (action, (arg1, arg2)))
        return {}
    commands.QueueTupleOfStr.responder(queue_tuple_of_str)

    def query_equipment(self):
        print "TODO: get equipment here"
        equipment = {
            'head': '', 'torso': 'power armor', 'hands': 'laser gun'}
        return equipment
    commands.QueryEquipment.responder(query_equipment)

    #--------------------------------------------------------------------------
    # commands

    def add_chat_messages(self, messages):
        for i, m in enumerate(messages):
            messages[i] = {'message': m[0], 'type': m[1]}
        return self.callRemote(commands.AddChatMessages, messages=messages)

    def set_bottom_status_bar(self, text):
        return self.callRemote(commands.SetBottomStatusBar, text=text)

    def set_look_pointer(self, (x, y)):
        return self.callRemote(commands.SetLookPointer, x=x, y=y)

    def set_pilot(self, is_pilot):
        return self.callRemote(commands.SetPilot, is_pilot=is_pilot)

    def set_target(self, (x, y)):
        return self.callRemote(commands.SetTarget, x=x, y=y)

    def set_top_status_bar(self, text):
        return self.callRemote(commands.SetTopStatusBar, text=text)

    def set_view(self, view, colors):
        view = '\n'.join(view)
        c_colors = []
        for k, v in colors.items():
            c_colors.append(
                {'x': k[0], 'y': k[1], 'r': v[0], 'g': v[1], 'b': v[2]})
        return self.callRemote(commands.SetView, view=view, colors=c_colors)

    def unset_look_pointer(self):
        return self.callRemote(commands.UnsetLookPointer)

    def unset_target(self):
        return self.callRemote(commands.UnsetTarget)


class CommandFactory(Factory):

    protocol = CommandProtocol

    def __init__(self, requests):
        self.clients = {}
        self.requests = requests

    def buildProtocol(self, addr):
        return CommandProtocol(self)

    def callCommand(self, uid, command, *args, **kwargs):
        command = getattr(self.clients[uid], command)
        command(*args, **kwargs)


def main(loop, port, timeout):
    requests = Requests()
    loop.set_requests(requests)
    factory = CommandFactory(requests)
    loop.set_command_factory(factory)
    reactor.listenTCP(port, factory)
    lc = LoopingCall(loop.main)
    lc.start(timeout, now=False)
    reactor.run()
