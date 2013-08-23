import unittest

from lib.utl.bresenham import get_line


class TestGetLine(unittest.TestCase):

    def test_one_segment_line_can_be_drawn(self):
        self.assertEqual(get_line((0, 0), (0, 0)), [(0, 0)],
                         "one segment line should be drawn correctly")

    def test_long_line_can_be_drawn(self):
        self.assertEqual(
            get_line((0, 0), (3, 3)), [(0, 0), (1, 1), (2, 2), (3, 3)],
            "n-segment line should be drawn correctly")

    def test_line_respects_length_parameter(self):
        self.assertEqual(len(get_line((0, 0), (1, 1), 5)), 5,
                         "get_line should respect length parameter")
        self.assertEqual(len(get_line((0, 0), (10, 10), 5)), 5,
                         "get_line should respect length parameter")
