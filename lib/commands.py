from twisted.protocols.amp import Command, String, Integer, AmpList, Boolean

#------------------------------------------------------------------------------
# server commands


class QueueStr(Command):

    arguments = [('action', String()), ('arg', String())]
    response = []


class QueueInt(Command):

    arguments = [('action', String()), ('arg', Integer())]
    response = []


class QueueTupleOfStr(Command):
    arguments = [('action', String()),
                 ('arg1', String()),
                 ('arg2', String())]
    response = []


class QueueTupleOfInt(Command):
    arguments = [('action', String()),
                 ('arg1', Integer()),
                 ('arg2', Integer())]
    response = []

#------------------------------------------------------------------------------
# client commands


class AddChatMessages(Command):

    arguments = [('messages', AmpList([('message', String()),
                                       ('type', Integer())]))]
    response = []


class SetBottomStatusBar(Command):

    arguments = [('text', String())]
    response = []


class SetPilot(Command):

    arguments = [('is_pilot', Boolean())]
    response = []


class SetTopStatusBar(Command):

    arguments = [('text', String())]
    response = []


class SetView(Command):

    arguments = [('view', String()),
                 ('colors', AmpList([('x', Integer()),
                                     ('y', Integer()),
                                     ('r', Integer()),
                                     ('g', Integer()),
                                     ('b', Integer())]))]
    response = []
