import unittest

from intrinsic_value import get_exit_multiple


class MyTestCase(unittest.TestCase):
    def test_get_exit_multiple(self):
        result = get_exit_multiple('AAPL')

        self.assertAlmostEqual(result, 36.0)


if __name__ == '__main__':
    unittest.main()
