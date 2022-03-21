import os


def get_project_root():
    return os.path.dirname(os.path.dirname(__file__))


def get_trade_risk(entry_price, stop_level):
    return entry_price - stop_level


def get_position_sizing(portfolio_risk, entry_price, stop_level):
    return portfolio_risk / get_trade_risk(entry_price, stop_level)
