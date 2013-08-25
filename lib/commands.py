from twisted.protocols.amp import Command, Unicode, Integer, AmpList, Boolean

#------------------------------------------------------------------------------
# server commands


class QueueStr(Command):

    arguments = [('action', Unicode()), ('arg', Unicode())]


class QueueInt(Command):

    arguments = [('action', Unicode()), ('arg', Integer())]


class QueueTupleOfStr(Command):
    arguments = [
        ('action', Unicode()), ('arg1', Unicode()), ('arg2', Unicode())]


class QueueTupleOfInt(Command):
    arguments = [
        ('action', Unicode()), ('arg1', Integer()), ('arg2', Integer())]

#------------------------------------------------------------------------------
# client commands


class AddChatMessages(Command):

    arguments = [
        ('messages', AmpList([('message', Unicode()), ('type', Integer())]))]


class SetBottomStatusBar(Command):

    arguments = [('text', Unicode())]


class SetLookPointer(Command):

    arguments = [('x', Integer()), ('y', Integer())]


class SetPilot(Command):

    arguments = [('is_pilot', Boolean())]


class SetTarget(Command):

    arguments = [('x', Integer()), ('y', Integer())]


class SetTopStatusBar(Command):

    arguments = [('text', Unicode())]


class SetView(Command):

    arguments = [
        ('view', Unicode()),
        ('colors', AmpList(
            [('x', Integer()),
             ('y', Integer()),
             ('r', Integer()),
             ('g', Integer()),
             ('b', Integer())]))]


class QueryEquipment(Command):

    response = [
        ('head', Unicode()), ('torso', Unicode()), ('hands', Unicode())]


class UnsetLookPointer(Command):

    pass


class UnsetTarget(Command):

    pass
