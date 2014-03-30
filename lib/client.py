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

    def set_equipment(self, equipment):
        amp_equipment, equipment = equipment, {}
        for item in amp_equipment:
            equipment[item['slot']] = item['item']
        self.main.set_equipment(equipment)
        return {}
    commands.SetEquipment.responder(set_equipment)

    def set_inventory(self, inventory):
        amp_inventory, inventory = inventory, {}
        for item in amp_inventory:
            inventory[item['item']] = item['qty']
        self.main.set_inventory(inventory)
        return {}
    commands.SetInventory.responder(set_inventory)

    def set_look_pointer(self, x, y):
        self.main.set_look_pointer((x, y))
        return {}
    commands.SetLookPointer.responder(set_look_pointer)

    def set_pilot(self, is_pilot):
        self.main.set_pilot(is_pilot)
        return {}
    commands.SetPilot.responder(set_pilot)

    def set_target(self, x, y):
        self.main.set_target((x, y))
        return {}
    commands.SetTarget.responder(set_target)

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

    def unset_look_pointer(self):
        self.main.unset_look_pointer()
        return {}
    commands.UnsetLookPointer.responder(unset_look_pointer)

    def unset_target(self):
        self.main.unset_target()
        return {}
    commands.UnsetTarget.responder(unset_target)

    #--------------------------------------------------------------------------
    # commands

    def read_equipment(self, amp_equipment):
        equipment = {}
        for item in amp_equipment['equipment']:
            equipment[item['slot']] = item['item']
        return equipment

    def query_equipment(self):
        amp_equipment = self.callRemote(commands.QueryEquipment)
        amp_equipment.addCallback(self.read_equipment)
        return amp_equipment

    def read_inventory(self, amp_inventory):
        inventory = {}
        for item in amp_inventory['inventory']:
            inventory[item['item']] = item['qty']
        return inventory

    def query_inventory(self):
        amp_inventory = self.callRemote(commands.QueryInventory)
        amp_inventory.addCallback(self.read_inventory)
        return amp_inventory

    def queue_action(self, action, arg):
        if isinstance(arg, tuple):
            if isinstance(arg[0], int):
                return self._queue_tuple_of_int(action, arg)
            return self._queue_tuple_of_str(action, arg)
        if isinstance(arg, int):
            return self._queue_int(action, arg)
        return self._queue_str(action, arg)

    def _queue_int(self, action, arg):
        return self.callRemote(
            commands.QueueInt, action=action, arg=arg)

    def _queue_str(self, action, arg):
        return self.callRemote(
            commands.QueueStr, action=action, arg=arg)

    def _queue_tuple_of_int(self, action, arg):
        return self.callRemote(
            commands.QueueTupleOfInt, action=action, arg1=arg[0], arg2=arg[1])

    def _queue_tuple_of_str(self, action, arg):
        return self.callRemote(
            commands.QueueTupleOfStr, action=action, arg1=arg[0], arg2=arg[1])


class Client:

    def __init__(self, host, port, main):
        destination = TCP4ClientEndpoint(reactor, host, port)
        self.protocol = CommandProtocol(main)
        self.d = connectProtocol(destination, self.protocol)

    def callCommand(self, command, *args, **kwargs):
        command = getattr(self.protocol, command)
        return command(*args, **kwargs)

    def stop(self):
        self.protocol.transport.loseConnection()

    #--------------------------------------------------------------------------
    # commands

    def queue_action(self, action, arg):
        return self.protocol.queue_action(action, arg)


def main(loop, host, port, timeout):
    command = Client(host, port, loop)
    loop.set_command(command)
    lc = LoopingCall(loop.main)
    lc.start(timeout, now=False)
    reactor.run()
