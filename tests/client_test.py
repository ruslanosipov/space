from twisted.internet import defer
from twisted.trial import unittest

from lib import client
from lib import commands


class MainMock(object):
    bottom_status_bar = ''
    chat_messages = []
    colors = {}
    equipment = {}
    inventory = {}
    is_pilot = False
    look_pointer = None
    target = None
    top_status_bar = ''
    view = ''

    def add_chat_messages(self, messages):
        self.chat_messages += messages

    def set_bottom_status_bar(self, text):
        self.bottom_status_bar = text

    def set_equipment(self, equipment):
        self.equipment = equipment

    def set_inventory(self, inventory):
        self.inventory = inventory

    def set_look_pointer(self, (x, y)):
        self.look_pointer = (x, y)

    def set_pilot(self, is_pilot):
        self.is_pilot = is_pilot

    def set_target(self, (x, y)):
        self.target = (x, y)

    def set_top_status_bar(self, text):
        self.top_status_bar = text

    def set_view(self, view, colors):
        self.view = view
        self.colors = colors

    def unset_look_pointer(self):
        self.look_pointer = None

    def unset_target(self):
        self.target = None


class ProtocolTestMixin(object):

    def setUp(self):
        self.main = MainMock()
        self.protocol = client.CommandProtocol(self.main)

    def assert_callback(self, unused):
        raise NotImplementedError("Has to be implemented!")

    def test_responder(self):
        responder = self.protocol.lookupFunction(
            self.command.commandName)
        d = responder(self.command.makeArguments(self.data, self.protocol))
        d.addCallback(self.assert_callback)
        return d


class AddChatMessagesTest(ProtocolTestMixin, unittest.TestCase):
    command = commands.AddChatMessages
    data = {'messages': [{'message': 'Hello world!', 'type': 0}]}

    def assert_callback(self, unused):
        self.assertEqual(self.main.chat_messages, [('Hello world!', 0)])


class SetBottomStatusBarTest(ProtocolTestMixin, unittest.TestCase):
    command = commands.SetBottomStatusBar
    data = {'text': 'new bottom status bar'}

    def assert_callback(self, unused):
        self.assertEquals(self.main.bottom_status_bar, self.data['text'])


class SetEquipmentTest(ProtocolTestMixin, unittest.TestCase):
    command = commands.SetEquipment
    data = {'equipment': [{'slot': 'torso', 'item': 'armor'}]}

    def assert_callback(self, unused):
        self.assertEquals(self.main.equipment, {'torso': 'armor'})


class SetInventoryTest(ProtocolTestMixin, unittest.TestCase):
    command = commands.SetInventory
    data = {'inventory': [{'item': 'knife', 'qty': 2}]}

    def assert_callback(self, unused):
        self.assertEquals(self.main.inventory, {'knife': 2})


class SetLookPointerTest(ProtocolTestMixin, unittest.TestCase):
    command = commands.SetLookPointer
    data = {'x': 2, 'y': 7}

    def assert_callback(self, unused):
        self.assertEqual(self.main.look_pointer, (2, 7))


class SetPilotTest(ProtocolTestMixin, unittest.TestCase):
    command = commands.SetPilot
    data = {'is_pilot': True}

    def assert_callback(self, unused):
        self.assertTrue(self.main.is_pilot)


class SetTargetTest(ProtocolTestMixin, unittest.TestCase):
    command = commands.SetTarget
    data = {'x': 2, 'y': 7}

    def assert_callback(self, unused):
        self.assertEqual(self.main.target, (2, 7))


class SetTopStatusBarTest(ProtocolTestMixin, unittest.TestCase):
    command = commands.SetTopStatusBar
    data = {'text': 'new top status bar'}

    def assert_callback(self, unused):
        self.assertEqual(self.main.top_status_bar, self.data['text'])


class SetViewTest(ProtocolTestMixin, unittest.TestCase):
    command = commands.SetView
    data = {
        'view': 'the view string',
        'colors': [{'x': 9, 'y': 6, 'r': 255, 'g': 0, 'b': 255}]}

    def assert_callback(self, unused):
        self.assertEqual(self.main.view, [self.data['view']])
        self.assertEqual(self.main.colors, {(9, 6): (255, 0, 255)})


class UnsetLookPointerTest(ProtocolTestMixin, unittest.TestCase):
    command = commands.UnsetLookPointer
    data = {}

    def assert_callback(self, unused):
        self.assertIsNone(self.main.look_pointer)


class UnsetTargetTest(ProtocolTestMixin, unittest.TestCase):
    command = commands.UnsetTarget
    data = {}

    def assert_callback(self, unused):
        self.assertIsNone(self.main.target)


class ControllerCommandsTest(unittest.TestCase):

    def setUp(self):
        self.calls = []
        self.main = MainMock()
        self.protocol = client.CommandProtocol(self.main)
        self.protocol.callRemote = self.call_remote

    def call_remote(self, command_type, **kwargs):
        result = defer.Deferred()
        self.calls.append((result, command_type, kwargs))
        return result

    def test_query_equipment(self):
        self.protocol.query_equipment()
        self.assertEquals(len(self.calls), 1)
        result, command, kwargs = self.calls.pop()
        self.assertIdentical(command, commands.QueryEquipment)
        self.assertEqual(kwargs, {})
        result.callback({'equipment': [{'slot': 'torso', 'item': 'armor'}]})
        self.assertEqual(result.result, {'torso': 'armor'})

    def test_query_inventory(self):
        self.protocol.query_inventory()
        self.assertEquals(len(self.calls), 1)
        result, command, kwargs = self.calls.pop()
        self.assertIdentical(command, commands.QueryInventory)
        self.assertEqual(kwargs, {})
        result.callback({'inventory': [{'item': 'knife', 'qty': 2}]})
        self.assertEqual(result.result, {'knife': 2})

    def test_queue_int_action(self):
        self.protocol.queue_action('sample_action', 42)
        self.assertEquals(len(self.calls), 1)
        _, command, kwargs = self.calls.pop()
        self.assertIdentical(command, commands.QueueInt)
        self.assertEqual(kwargs, {'action': 'sample_action', 'arg': 42})

    def test_queue_str_action(self):
        self.protocol.queue_action('sample_action', 'string')
        self.assertEquals(len(self.calls), 1)
        _, command, kwargs = self.calls.pop()
        self.assertIdentical(command, commands.QueueStr)
        self.assertEqual(kwargs, {'action': 'sample_action', 'arg': 'string'})

    def test_queue_tuple_of_int_action(self):
        self.protocol.queue_action('sample_action', (42, 98))
        self.assertEquals(len(self.calls), 1)
        _, command, kwargs = self.calls.pop()
        self.assertIdentical(command, commands.QueueTupleOfInt)
        self.assertEqual(kwargs, {
            'action': 'sample_action',
            'arg1': 42,
            'arg2': 98})

    def test_queue_tuple_of_str_action(self):
        self.protocol.queue_action('sample_action', ('string1', 'string2'))
        self.assertEquals(len(self.calls), 1)
        _, command, kwargs = self.calls.pop()
        self.assertIdentical(command, commands.QueueTupleOfStr)
        self.assertEqual(kwargs, {
            'action': 'sample_action',
            'arg1': 'string1',
            'arg2': 'string2'})
