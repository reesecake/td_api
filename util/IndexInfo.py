import requests
import pandas as pd
from bs4 import BeautifulSoup as bs


def get_spy():
    url = 'https://www.slickcharts.com/sp500'

    request = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

    soup = bs(request.text, "lxml")

    stats = soup.find('table', class_='table table-hover table-borderless table-sm')

    df = pd.read_html(str(stats))[0]

    df['% Chg'] = df['% Chg'].str.strip('()-%')

    df['% Chg'] = pd.to_numeric(df['% Chg'])

    df['Chg'] = pd.to_numeric(df['Chg'])

    return df
