import json
import requests
from bs4 import BeautifulSoup

from util.Data import get_fundamentals


def get_growth_rate(symbol):
    # https://www.yahoofinanceapi.com/
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',  # Do Not Track Request Header
        'Connection': 'close'
    }

    response = requests.get(f"https://finance.yahoo.com/quote/{symbol}/analysis?p={symbol}", headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    for tr in soup.find_all("tr", class_="BdT Bdc($seperatorColor)"):
        if tr.contents[0].contents[0].text == "Next 5 Years (per annum)":
            eps_forward_5yrs = tr.contents[1].contents[0].text
        if tr.contents[0].contents[0].text == "Past 5 Years (per annum)":
            eps_trailing_5yrs = tr.contents[1].contents[0].text

    # TODO: exception handling
    growth_rate = float(eps_forward_5yrs[:-1])
    print(f"retrieved growth_rate: {growth_rate}")
    if growth_rate > 5.99:
        growth_rate = growth_rate * 0.95
    elif growth_rate > 11.99:
        growth_rate = growth_rate * 0.90
    elif growth_rate > 19.99:
        growth_rate = growth_rate * 0.85
    elif growth_rate > 29.99:
        growth_rate = growth_rate * 0.80
    elif growth_rate > 40.0:
        growth_rate = 40.0

    return growth_rate


def get_exit_multiple(symbol: str):
    # http://people.stern.nyu.edu/adamodar/podcasts/valUGspr17/session21.pdf
    # TODO: implement
    return 36.0


def calc_capm(access_token, stock_fundamentals: dict):
    """
    Calculates Capital Asset Pricing Model
    :param access_token:
    :param stock_fundamentals: dict of stock's fundamentals
    :return: expected annualized rate of return
    """

    """ replace hunk """
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    query = {
        'symbol': '$VIX.X,$TYX.X',
    }
    quote = requests.get(f"https://api.tdameritrade.com/v1/marketdata/quotes",
                         headers=headers, params=query).json()
    """ replace hunk """

    valVIX = quote['$VIX.X']['lastPrice']
    valTYX = quote['$TYX.X']['lastPrice']
    beta = stock_fundamentals['beta']

    if valVIX < 13:
        market_risk_premium = 5
    elif valVIX < 18:
        market_risk_premium = 6
    elif valVIX < 30:
        market_risk_premium = 7
    elif valVIX < 45:
        market_risk_premium = 8
    else:
        market_risk_premium = 9

    risk_free_rate = valTYX / 10.0

    return (beta * market_risk_premium) + risk_free_rate


def IVquoteRequest(access_token, symbol: str):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    return requests.get(f"https://api.tdameritrade.com/v1/marketdata/{symbol}/quotes", headers=headers).json()[symbol]


def calc_intrinsic_value(access_token, symbol: str):
    fundamentals = get_fundamentals(access_token, symbol)
    eps_growth_rate = get_growth_rate(symbol)  # TODO: apply reduction
    exit_multiple = get_exit_multiple(symbol)
    expected_annual_ror = calc_capm(access_token, fundamentals)
    years_of_growth = 2  # TODO: change

    eps_ttm = fundamentals['epsTTM']
    intrinsic_value = (
            (eps_ttm * pow(1 + (eps_growth_rate / 100), years_of_growth)) * exit_multiple /
            pow((1 + (expected_annual_ror / 100)), years_of_growth))

    current_price = IVquoteRequest(access_token, symbol)['lastPrice']

    return {
        'intrinsic_value': intrinsic_value,
        'last_price': current_price,
        'margin_of_safety': (intrinsic_value - current_price) / intrinsic_value,
    }
