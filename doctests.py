#!/usr/bin/env python

import unittest
import doctest
import os
import sys


files = []
root_dirs = ['lib/']

for root_dir in root_dirs:
    for root, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename == '__init__.py' or filename[-3:] != '.py':
                continue
            f = os.path.join(root, filename)
            f = f.replace('/', '.')
            f = f[:-3]
            files.append(f)
files.append('tests.mocks')

suite = unittest.TestSuite()
for module in files:
    try:
        suite.addTest(doctest.DocTestSuite(module))
    except ValueError:
        pass
result = unittest.TextTestRunner(verbosity=1).run(suite)
if not result.wasSuccessful():
    sys.exit(1)
