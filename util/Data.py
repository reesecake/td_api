import json
import os
from datetime import datetime
from time import sleep

import requests
import pandas as pd

from util.IndexInfo import get_spy
from util.misc import get_project_root


def get_fundamentals_raw(access_token, symbol) -> requests.Response:
    """
    Get fundamentals data for a stock
    :param access_token:
    :param symbol: str - $ticker
    :return: Response - GET response of fundamentals
    """
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    query = {
        'symbol': f'{symbol}',
        'projection': 'fundamental',
    }

    try:
        response = requests.get(f"https://api.tdameritrade.com/v1/instruments",
                                params=query, headers=headers)
        response.raise_for_status()
    except requests.HTTPError as e:
        if e.response.status_code == 429:
            print(e.response.json())
            sleep(61)
            response = get_fundamentals_raw(access_token, symbol)
        else:
            raise

    # print(response.status_code)
    # print(json.dumps(response.json(), indent=4))
    return response


def get_fundamentals(access_token, symbol):
    fun_resp = get_fundamentals_raw(access_token, symbol)

    fun_dict = {}
    if fun_resp.status_code == 200:
        fun_dict = fun_resp.json()
        print(fun_dict[symbol]['fundamental']['symbol'])
    else:
        print(fun_resp.json())

    return fun_dict[symbol]['fundamental']


def build_fundamentals_df(access_token):
    f = open("time.json", "r")
    f_contents = json.load(f)
    f.close()
    if f_contents['fundamentals']['last_built'] == datetime.today().date():
        print("fundamentals have already been built today")
        return

    rows = []
    for ticker in get_spy()['Symbol'].tolist():
        rows.append(get_fundamentals(access_token, ticker))

    df = pd.DataFrame(rows)
    print(df)
    df.to_excel(os.path.join(get_project_root(), "output/fundamentals", f"{datetime.today().date()}_fundamentals.xlsx"))
    f = open("time.json", "r")
    f_contents = json.load(f)
    f.close()
    f_contents['fundamentals'] = {"last_built": f"{datetime.today().date()}"}
    f = open("time.json", "w")
    f.write(json.dumps(f_contents, indent=4))
    f.close()
