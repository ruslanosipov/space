from twisted.protocols.amp import Command, Unicode, Integer, AmpList, Boolean

#------------------------------------------------------------------------------
# server commands


class QueueStr(Command):

    arguments = [('action', Unicode()), ('arg', Unicode())]
    response = []


class QueueInt(Command):

    arguments = [('action', Unicode()), ('arg', Integer())]
    response = []


class QueueTupleOfStr(Command):
    arguments = [
        ('action', Unicode()), ('arg1', Unicode()), ('arg2', Unicode())]
    response = []


class QueueTupleOfInt(Command):
    arguments = [
        ('action', Unicode()), ('arg1', Integer()), ('arg2', Integer())]
    response = []

#------------------------------------------------------------------------------
# client commands


class AddChatMessages(Command):

    arguments = [
        ('messages', AmpList([('message', Unicode()), ('type', Integer())]))]
    response = []


class SetBottomStatusBar(Command):

    arguments = [('text', Unicode())]
    response = []


class SetPilot(Command):

    arguments = [('is_pilot', Boolean())]
    response = []


class SetTopStatusBar(Command):

    arguments = [('text', Unicode())]
    response = []


class SetView(Command):

    arguments = [
        ('view', Unicode()),
        ('colors', AmpList(
            [('x', Integer()),
            ('y', Integer()),
            ('r', Integer()),
            ('g', Integer()),
            ('b', Integer())]))]
    response = []
