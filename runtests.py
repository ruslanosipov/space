#!/usr/bin/env python

import unittest
import sys


testsuite = unittest.TestLoader().discover('tests/', pattern='*.py')
result = unittest.TextTestRunner(verbosity=1).run(testsuite)
if not result.wasSuccessful():
    sys.exit(1)
