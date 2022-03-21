import unittest

from util.misc import get_trade_risk, get_position_sizing


class MyTestCase(unittest.TestCase):
    def test_trade_risk(self):
        # Test inputs:
        entry_price = 52.65
        stop_level = 48.41

        result = get_trade_risk(entry_price, stop_level)

        self.assertAlmostEqual(result, 4.24)

    def test_position_sizing(self):
        # Test inputs:
        portfolio_risk = 2000
        entry_price = 30
        stop_level = 26.81 * 0.97

        result = get_position_sizing(portfolio_risk, entry_price, stop_level)

        self.assertTrue(abs(result - 500.0) < 1.0)


if __name__ == '__main__':
    unittest.main()
