"""AMP commands to communicate between client and server."""

from twisted.protocols import amp

#------------------------------------------------------------------------------
# Server commands.


class QueryEquipment(amp.Command):
    response = [(
        'equipment',
         amp.AmpList([('slot', amp.Unicode()), ('item', amp.Unicode())]))]


class QueryInventory(amp.Command):
    response = [(
        'inventory',
        amp.AmpList([('item', amp.Unicode()), ('qty', amp.Integer())]))]


class QueueStr(amp.Command):
    arguments = [('action', amp.Unicode()), ('arg', amp.Unicode())]


class QueueInt(amp.Command):
    arguments = [('action', amp.Unicode()), ('arg', amp.Integer())]


class QueueTupleOfStr(amp.Command):
    arguments = [
        ('action', amp.Unicode()),
        ('arg1', amp.Unicode()), ('arg2', amp.Unicode())]


class QueueTupleOfInt(amp.Command):
    arguments = [
        ('action', amp.Unicode()),
        ('arg1', amp.Integer()), ('arg2', amp.Integer())]

#------------------------------------------------------------------------------
# Client commands.


class AddChatMessages(amp.Command):
    arguments = [(
        'messages',
        amp.AmpList([('message', amp.Unicode()), ('type', amp.Integer())]))]


class SetBottomStatusBar(amp.Command):
    arguments = [('text', amp.Unicode())]


class SetEquipment(amp.Command):
    arguments = [(
        'equipment',
        amp.AmpList([('slot', amp.Unicode()), ('item', amp.Unicode())]))]


class SetInventory(amp.Command):
    arguments = [
        ('inventory',
            amp.AmpList([('item', amp.Unicode()), ('qty', amp.Integer())]))]


class SetLookPointer(amp.Command):
    arguments = [('x', amp.Integer()), ('y', amp.Integer())]


class SetPilot(amp.Command):
    arguments = [('is_pilot', amp.Boolean())]


class SetTarget(amp.Command):
    arguments = [('x', amp.Integer()), ('y', amp.Integer())]


class SetTopStatusBar(amp.Command):
    arguments = [('text', amp.Unicode())]


class SetView(amp.Command):
    arguments = [
        ('view', amp.Unicode()),
        ('colors', amp.AmpList(
            [('x', amp.Integer()),
             ('y', amp.Integer()),
             ('r', amp.Integer()),
             ('g', amp.Integer()),
             ('b', amp.Integer())]))]


class UnsetLookPointer(amp.Command):
    pass


class UnsetTarget(amp.Command):
    pass
