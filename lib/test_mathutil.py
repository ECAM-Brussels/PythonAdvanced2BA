import unittest
from lib import mathutil

class TestMathUtil(unittest.TestCase):
    def test_fact(self):
        with self.assertRaises(ValueError):
            mathutil.fact(-1)
        self.assertEqual(mathutil.fact(0), 1)
        self.assertEqual(mathutil.fact(1), 1)
        self.assertEqual(mathutil.fact(6), 720)