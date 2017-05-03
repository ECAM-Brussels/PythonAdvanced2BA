# test.py
# author: Sébastien Combéfis
# version: May 3, 2017

import importlib
import sys
import unittest

sys.path.append('CodeExamples')
import lib
from lib.test_mathutil import TestMathUtil

suite = unittest.TestLoader().loadTestsFromTestCase(TestMathUtil)
runner = unittest.TextTestRunner()
mathutil_test = not runner.run(suite).wasSuccessful()

sys.path.remove('CodeExamples')
sys.path.append('AIproject')
importlib.reload(lib)
from test_pylos import TestPylosState

suite = unittest.TestLoader().loadTestsFromTestCase(TestPylosState)
runner = unittest.TextTestRunner()
pylos_test = not runner.run(suite).wasSuccessful()

exit(mathutil_test and pylos_test)
