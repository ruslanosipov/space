from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from twisted.protocols.amp import AMP
from twisted.internet.task import LoopingCall

import commands


class CommandProtocol(AMP):

    def __init__(self, main):
        self.main = main

    def connectionLost(self, reason):
        print "Server connection lost, shutting down..."
        reactor.stop()

    #--------------------------------------------------------------------------
    # responders

    def add_chat_messages(self, messages):
        for i, m in enumerate(messages):
            messages[i] = (m['message'], m['type'])
            self.main.add_chat_messages(messages)
        return {}
    commands.AddChatMessages.responder(add_chat_messages)

    def set_bottom_status_bar(self, text):
        self.main.set_bottom_status_bar(text)
        return {}
    commands.SetBottomStatusBar.responder(set_bottom_status_bar)

    def set_pilot(self, is_pilot):
        self.main.set_pilot(is_pilot)
        return {}
    commands.SetPilot.responder(set_pilot)

    def set_top_status_bar(self, text):
        self.main.set_top_status_bar(text)
        return {}
    commands.SetTopStatusBar.responder(set_top_status_bar)

    def set_view(self, view, colors):
        view = view.split('\n')
        c_colors = {}
        for c in colors:
            c_colors[(c['x'], c['y'])] = (c['r'], c['g'], c['b'])
        self.main.set_view(view, c_colors)
        return {}
    commands.SetView.responder(set_view)


class Client:

    def __init__(self, host, port, main):
        destination = TCP4ClientEndpoint(reactor, host, port)
        self.protocol = CommandProtocol(main)
        self.d = connectProtocol(destination, self.protocol)

    def stop(self):
        self.protocol.transport.loseConnection()

    #--------------------------------------------------------------------------
    # commands

    def queue_int(self, action, arg):
        return self.protocol.callRemote(
            commands.QueueInt, action=action, arg=arg)

    def queue_str(self, action, arg):
        return self.protocol.callRemote(
            commands.QueueStr, action=action, arg=arg)

    def queue_tuple_of_int(self, action, arg):
        return self.protocol.callRemote(
            commands.QueueTupleOfInt, action=action, arg1=arg[0], arg2=arg[1])

    def queue_tuple_of_str(self, action, arg):
        return self.protocol.callRemote(
            commands.QueueTupleOfStr, action=action, arg1=arg[0], arg2=arg[1])


def main(loop, host, port, timeout):
    command = Client(host, port, loop)
    loop.set_command(command)
    lc = LoopingCall(loop.main)
    lc.start(timeout, now=False)
    reactor.run()
