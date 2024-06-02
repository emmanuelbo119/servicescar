import unittest

class TestClass(unittest.TestCase):

    def absoluteVal(self, x):
        if x < 0:
            return -x
        else:
            return x

    def test_negative_number(self):
        self.assertEqual(self.absoluteVal(-42), 42)

    def test_positive_number(self):
        self.assertEqual(self.absoluteVal(42), 42)

    def test_zero(self):
        self.assertEqual(self.absoluteVal(0), 0)

    def test_small_negative_number(self):
        self.assertEqual(self.absoluteVal(-1), 1)

    def test_small_positive_number(self):
        self.assertEqual(self.absoluteVal(1), 1)

if __name__ == '__main__':
    unittest.main()