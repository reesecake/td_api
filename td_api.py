import json
import requests
from datetime import datetime

from intrinsic_value import calc_intrinsic_value
from util.Data import get_fundamentals, build_fundamentals_df
from util.IndexInfo import get_spy

'''https://developer.tdameritrade.com/content/getting-started'''
'''https://developer.tdameritrade.com/user/me/apps'''
'''https://developer.tdameritrade.com/content/simple-auth-local-apps'''

# my investment account
account_id = 275487917
# use authorization_code to get new refresh_token
code = '4wJ5mHMnkAesGtaianUSXOtSeVly1Au1M+B7UJyW2HTk6QGs9zXCpR3jmwJLi8HHgoh+Q8rGlMAn2Vo/Y/REWzOC3b0hrPNDjgBtzYkVafQyIiVh7t9IKq0bCgbsSET1slSrBMKBKqhJr9Lt3rgE3R8NTXROp9sf+KbqpPcQqypTBxfqmujGZr/KcGmgLGx3NyWwQBFmWVl5+uuyhJttZb1fqZz027DjGfpfZbhS2zp2anD2syGkDjlk2SOvCxXgwjv2NygK8fUgRnm74X0GCIIApfkjh0D/OP+x434b2ZJSMebtmfsT2lUytUEtrymMzYGmxi33rAqW+1P0ykbRiYCqp9IprsKH0DZKfrkNQBI/uRzKOXgHUclc26GufP8hJ3Wci0SPs5i/H2MBrfQSuc+5I9E7Rpyyj62MXLoOYI4m7fBT6xvZJeQN9Xcx30o+kHshK100MQuG4LYrgoVi/JHHvlAwUSz52DecgwqrVotNys1bWpQhXK/wYg6NtDXt+Yy/LvegGeBLWHz5z/mWLPBjzX9pfLWZP3gdNhA8+DPkUKxjUTEQaWENcGuHrkkZb405tXgQ9fwrjzL4SDuhwsGfCnyXYDfFIQmVf/9iiRp8LLcAYWtr5N+Qdro8VJrTUtuhZnteq1PEr1tjw6ivFZvcCBxJ17jbRkAP9k9dU32bMgkxCsIGm2QnQkjPT/KniOMzeny3BMv6egcZAdSTLcvw5h7YYeEGdjou0YCGRtCMxxJzjQLSP0MP3UEjvmDfkqDTFDcQEjGRQls8P/xFyUij2a5HRrTjPE0KddvZQrWouaHkC5Gb5TJ60LhehYWX8QFYkDIJmCtmFAefmEU2YTE3aYZ4UBsf1vsmSGVo5kELiZ33t0dnVRzi1o8I1KO7di2PWvzUx4GSqyMgmxDuTBFnyKZAPCIp212FD3x19z9sWBHDJACbC00B75E'
# refresh_token lasts 90 days
refresh_token = 'cgCtBVFen+qAu5xv/FvEldZaKNbqE0/cPd8gS9yQDFdehLASLUrdBYSc1QJGc6rK9XuiKd12UTIWekpezu2dpovm7xEnTPbIGwYf+pyRRA8kT9qekyYCNRXnbCeOvXdLKNfPhKiYzr9zWRhv7fJph21phDurGsZBlR9rvm34F53jWiTB5yCqbLtXIC4r8FM12PdH8lpsnvMTAiy+1D6oBagedZxy9JUXPGTRMsPjhvIeBCvl/CH+vl+R/V+Yc2tgd769kU70AOkNR9uh9cKf1yoUuRQYtjoEjmiHQ4uspjgQG9dz6kJ7etbzeIg5Q/4GQJSzf7HEGOOfFA12MEpACmqZoLC7A6XM507a6yYraIbdsMGBTvvllHwzjoFIfiVEnMe0UxiiWUUg1EOxYi9Z+RL6/DXR+//SXmGgA9W701wpq6RqnRHOXBK1RZ2100MQuG4LYrgoVi/JHHvlI1e7z8cdNf6YotBeLJdTCNgxgDpf+9dVWCU6WeT228dJG+vQDRei9IbykumY21klXmQUgQVtwWZmdA7zmi2xWxN7mbPn2luu2IQiqoTt8iGBkwVcF2ljJ5MkZayi2dedy0/ea1v+mMfqVWtvLOwkFMEPubLwoyG4dFgN2oRHzKPQe36oZvrd69VmWC2vnGf/SWw+m4sAbAvNoqOlcwuVojvq8dx03gNGR+P/UwCiD+ZJGq2rGH5AYsHWEvLSWqJ7p7y/F/+UhOnmpoOYXhYxRywjxpQ4spWkQfyJyOBU4UVV/5xeq/PU0OyQO+/TqFV8jdfO8Xj+xdv+cQkJ4rdd9sCUERlQeA8JaYUTjPgtRI/IUXHUWjiKVkloPvgYFF7W7BHSQULLLDhIXaXOpxOO/+b+dHga1QtNrGJmTC4GkdJnlCKPBpTBhhI3u6I=212FD3x19z9sWBHDJACbC00B75E'


def accessSetup():
    query = {'grant_type': 'refresh_token',
             'refresh_token': refresh_token,
             'access_type': '',
             'code': '',
             'client_id': 'FYXOCOZZTN8WGW9SP3XGIAZRK0DUBRDJ',
             'redirect_uri': ''
             }
    response = requests.post("https://api.tdameritrade.com/v1/oauth2/token", data=query)
    # save 30-minute access_token
    access_token = response.json()['access_token']
    # print(f"{response.json()}")

    return access_token


def simpleRequests(access_token):
    query = {}
    headers = {
        'Authorization': f'Bearer {access_token}'}

    # dt = datetime.now()
    # ts = datetime.timestamp(dt)
    # use timestamp to avoid making requests everytime
    response = requests.get(f"https://api.tdameritrade.com/v1/accounts/{account_id}", headers=headers)

    print(f"my account ({account_id}):")
    print(response.json())


def quoteRequest(access_token, symbol: str):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    print(
        json.dumps(requests.get(f"https://api.tdameritrade.com/v1/marketdata/{symbol}/quotes", headers=headers).json(),
                   indent=4)
    )


def main():
    with open("time.json", "r") as f:
        data = json.load(f)

    dt = datetime.now()
    ts = datetime.timestamp(dt)

    if ts > float(data["access_token"]["creationTime"]) + 1800:
        print("access_token invalid, refreshing...")
        access_token = accessSetup()
        f = open("time.json", "r")
        f_contents = json.load(f)
        f.close()
        f_contents['access_token'] = {"value": f"{access_token}", "creationTime": f"{ts}"}
        f = open("time.json", "w")
        f.write(json.dumps(f_contents, indent=4))
        f.close()
    else:
        print(f"Access_token still valid for "
              f"{'{:.2f}'.format((1800.0 - (ts - float(data['access_token']['creationTime']))) / 60.0)} minutes. "
              f"Skipping setup.")
        access_token = data["access_token"]["value"]

    # simpleRequests(access_token)
    # quoteRequest(access_token, "PYPL")  # example quote
    # print(calc_intrinsic_value(access_token, 'FISV'))
    # print(get_spy())
    build_fundamentals_df(access_token)


if __name__ == '__main__':
    main()
