#!/usr/bin/env python

import unittest
import doctest


modules = [
    'lib.player.player',
    'lib.utl.bresenham',
    'lib.chat']

suite = unittest.TestSuite()
for module in modules:
    suite.addTest(doctest.DocTestSuite(module))
unittest.TextTestRunner(verbosity=2).run(suite)
