# test.py
# author: Sébastien Combéfis
# version: February 1, 2016

import unittest
from lib import test_mathutil

suite = unittest.TestLoader().loadTestsFromTestCase(test_mathutil.TestMathUtil)
runner = unittest.TextTestRunner()
print(runner.run(suite))