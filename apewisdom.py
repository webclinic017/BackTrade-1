import requests
import numpy as np
import pandas_datareader as pdr
import datetime as dt
import pandas as pd


def get_stock_table(url):
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    r = requests.get(url, headers=header)
    ticker_series = pd.read_html(r.text)
    return ticker_series


def api_manage(flt, pageNbr):
    url = f"https://apewisdom.io/api/v1.0/filter/{flt}/page/{pageNbr}"
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    r = requests.get(url, headers=header)
    return r


if __name__ == '__main__':
    # url = r"https://apewisdom.io/"
    flt = "all-stocks"
    pageNbr = "1"
    table = api_manage(flt,pageNbr)
    x = table.json()
    df = pd.DataFrame(x['results'])
    df = df.drop(columns=['name','rank_24h_ago','mentions_24h_ago'])
    print(df)
    # df = pd.DataFrame(table.text)
    # print(df.head())
