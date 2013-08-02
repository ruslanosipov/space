import unittest

from lib.chatclient import ChatClient


class TestChatClient(unittest.TestCase):

    def setUp(self):
        self.chatclient = ChatClient()

    def test_get_log_returns_correct_size(self):
        self.chatclient.add_multiple([("foo", 1) for x in xrange(0, 8)])
        self.assertEqual(len(self.chatclient.get_log(22)), 8,
                         "log should return all available records")
        self.chatclient.add_multiple([("foo", 1) for x in range(0, 20)])
        self.assertEqual(len(self.chatclient.get_log(22)), 22,
                         "log should not return more items then size")
        self.chatclient.add_multiple([("foo" * 20, 1) for x in xrange(0, 8)])
        width_limit = 56
        for line in self.chatclient.get_log(22):
            self.assertLessEqual(len(line[0]), width_limit,
                                 "chat log should respect width limit")
