#!/usr/bin/env python

import unittest


testsuite = unittest.TestLoader().discover('tests/', pattern='*.py')
unittest.TextTestRunner(verbosity=1).run(testsuite)
