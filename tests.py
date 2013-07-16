#!/usr/bin/env python

import unittest
import doctest


modules = [
    'lib.player.player',
    'lib.utl.bresenham',
    'lib.ship.spaceship',
    'lib.chat',
    'lib.ship.projectile']

suite = unittest.TestSuite()
for module in modules:
    suite.addTest(doctest.DocTestSuite(module))
unittest.TextTestRunner(verbosity=1).run(suite)
