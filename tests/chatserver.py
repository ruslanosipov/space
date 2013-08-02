import unittest


from lib.chatserver import ChatServer

class TestChatServer(unittest.TestCase):

    def setUp(self):
        self.chatserver = ChatServer()
        self.recipient = 'Mike'
        self.not_recipient = 'Josh'

    def test_recipient_receives_related_message(self):
        self.chatserver.add_single(self.recipient, "You see a wolf.", 1)
        self.assertEqual(self.chatserver.get_recent_for_recipient(
                         self.recipient), [("You see a wolf.", 1)],
                         "recipient should receive related message")

    def test_recipient_does_not_receive_unrelated_message(self):
        self.chatserver.add_single(self.recipient, "You see a wolf.", 1)
        self.chatserver.add_single(self.not_recipient, "You see a boar.", 1)
        self.assertEqual(self.chatserver.get_recent_for_recipient(
                         self.recipient), [("You see a wolf.", 1)],
                         "recipient should not see unrelated message")

    def test_recipient_does_not_receive_same_message_twice(self):
        self.chatserver.add_single(self.recipient, "You see a wolf.", 1)
        self.chatserver.get_recent_for_recipient(self.recipient)
        self.assertEqual(self.chatserver.get_recent_for_recipient(
                         self.recipient), [],
                         "recipient should not receive same message twice")

    def test_recipient_receives_public_messages(self):
        self.chatserver.add_single(self.recipient, "You see a wolf.", 1)
        self.chatserver.add_single('public', "Someone cries.", 2)
        self.assertEqual(self.chatserver.get_recent_for_recipient(
                         self.recipient), [("You see a wolf.", 1),
                         ("Someone cries.", 2)],
                         "recipient should receive public message")

    def test_chat_log_is_shorter_than_limit(self):
        limit = 1000
        for _ in xrange(0, 1024):
            self.chatserver.add_single('public', "Someone laughs.", 2)
        self.assertLessEqual(len(self.chatserver.get_recent_for_recipient(
                         self.recipient)), limit,
                         "number of chat log entries should not exceed limit")
