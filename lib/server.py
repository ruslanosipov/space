"""Server - serves game information to a set of clients."""

import copy
import logging

from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.protocols.amp import AMP
from twisted.internet.task import LoopingCall

from lib import commands

logging = logging.getLogger(__name__)


class Requests(object):

    def __init__(self):
        self.clients = {}

    def add_request(self, client, request):
        if client not in self.clients:
            self.clients[client] = []
        self.clients[client].append(request)

    def get_requests(self):
        requests = copy.deepcopy(self.clients)
        for client in self.clients.keys():
            self.clients[client] = []
        return requests


class CommandProtocol(AMP):

    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.uid = str(id(self))
        self.factory.clients[self.uid] = self
        logging.info("%s:Connected.", self.uid)

    #--------------------------------------------------------------------------
    # responders

    def queue_int(self, action, arg):
        self.factory.requests.add_request(self.uid, (action, arg))
        logging.debug(
                "%s:Queued int '%s' with value %d.", self.uid, action, arg)
        return {}
    commands.QueueInt.responder(queue_int)

    def queue_str(self, action, arg):
        self.factory.requests.add_request(self.uid, (action, arg))
        logging.debug(
                "%s:Queued str '%s' with value '%s'.", self.uid, action, arg)
        return {}
    commands.QueueStr.responder(queue_str)

    def queue_tuple_of_int(self, action, arg1, arg2):
        self.factory.requests.add_request(self.uid, (action, (arg1, arg2)))
        logging.debug(
                "%s:Queued tuple of int '%s' with values (%d, %d).",
                self.uid, action, arg1, arg2)
        return {}
    commands.QueueTupleOfInt.responder(queue_tuple_of_int)

    def queue_tuple_of_str(self, action, arg1, arg2):
        self.factory.requests.add_request(self.uid, (action, (arg1, arg2)))
        logging.debug(
                "%s:Queued tuple of str '%s' with values ('%s', '%s').",
                self.uid, action, arg1, arg2)
        return {}
    commands.QueueTupleOfStr.responder(queue_tuple_of_str)

    def query_equipment(self):
        equipment = self.factory.game.get_equipment(self.uid)
        amp_equipment = []
        for k, v in equipment.items():
            v = 'None' if v is None else v.get_name()
            amp_equipment.append({'slot': k, 'item': v})
        logging.debug(
                "%s:Request equipment, response: %s.", self.uid, amp_equipment)
        return {'equipment': amp_equipment}
    commands.QueryEquipment.responder(query_equipment)

    def query_inventory(self):
        inventory = self.factory.game.get_inventory(self.uid)
        amp_inventory = []
        for item, qty in inventory.items():
            amp_inventory.append({'item': item.get_name(), 'qty': qty})
        logging.debug(
                "%s:Request inventory, response: %s.", self.uid, amp_inventory)
        return {'inventory': amp_inventory}
    commands.QueryInventory.responder(query_inventory)

    #--------------------------------------------------------------------------
    # commands

    def add_chat_messages(self, messages):
        for i, m in enumerate(messages):
            messages[i] = {'message': m[0], 'type': m[1]}
        logging.debug("%s:Sent messages: %s.", self.uid, messages)
        return self.callRemote(commands.AddChatMessages, messages=messages)

    def set_bottom_status_bar(self, text):
        logging.debug("%s:Set bottom status bar to '%s'.", self.uid, text)
        return self.callRemote(commands.SetBottomStatusBar, text=text)

    def set_equipment(self, equipment):
        amp_equipment = []
        for k, v in equipment.items():
            v = 'None' if v is None else v.get_name()
            amp_equipment.append({'slot': k, 'item': v})
        logging.debug("%s:Set equipment to %s.", self.uid, amp_equipment)
        return self.callRemote(commands.SetEquipment, equipment=amp_equipment)

    def set_inventory(self, inventory):
        amp_inventory = []
        for item, qty in inventory.items():
            amp_inventory.append({'item': item.get_name(), 'qty': qty})
        logging.debug("%s:Set inventory to %s.", self.uid, amp_inventory)
        return self.callRemote(commands.SetInventory, inventory=amp_inventory)

    def set_look_pointer(self, (x, y)):
        logging.debug(
                "%s:Set look pointer at (%d, %d).",
                self.uid, x, y)
        return self.callRemote(commands.SetLookPointer, x=x, y=y)

    def set_pilot(self, is_pilot):
        logging.debug(
                "%s:Set pilot mode to %r.",
                self.uid, is_pilot)
        return self.callRemote(commands.SetPilot, is_pilot=is_pilot)

    def set_target(self, (x, y)):
        logging.debug(
                "%s:Set target pointer at (%d, %d).",
                self.uid, x, y)
        return self.callRemote(commands.SetTarget, x=x, y=y)

    def set_top_status_bar(self, text):
        logging.debug("%s:Set top status bar to '%s'.", self.uid, text)
        return self.callRemote(commands.SetTopStatusBar, text=text)

    def set_view(self, view, colors):
        view = '\n'.join(view)
        c_colors = []
        for k, v in colors.items():
            c_colors.append(
                {'x': k[0], 'y': k[1], 'r': v[0], 'g': v[1], 'b': v[2]})
        logging.debug("%s:Set view.", self.uid)
        return self.callRemote(commands.SetView, view=view, colors=c_colors)

    def unset_look_pointer(self):
        logging.debug("%s:Unset look pointer.", self.uid)
        return self.callRemote(commands.UnsetLookPointer)

    def unset_target(self):
        logging.debug("%s:Unset target pointer.", self.uid)
        return self.callRemote(commands.UnsetTarget)


class CommandFactory(Factory):

    protocol = CommandProtocol

    def __init__(self, requests, game):
        self.clients = {}
        self.game = game
        self.requests = requests

    def buildProtocol(self, addr):
        return CommandProtocol(self)

    def callCommand(self, uid, command, *args, **kwargs):
        command = getattr(self.clients[uid], command)
        command(*args, **kwargs)


def main(loop, port, timeout):
    requests = Requests()
    loop.set_requests(requests)
    factory = CommandFactory(requests, loop)
    loop.set_command_factory(factory)
    reactor.listenTCP(port, factory)
    logging.info("Started server on port %d.", port)
    lc = LoopingCall(loop.main)
    lc.start(timeout, now=False)
    reactor.run()
