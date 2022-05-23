import time
import concurrent.futures
import yfinance as yf
import numpy as np
import talib
import pandas as pd
from otherfunctions import get_high_corr
import otherfunctions as of


tickers = of.get_tickers()


def create_threads(splits):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(fix_csv, splits)


def add_highest_corr_stocks(ticker):
    top_corr = of.get_high_corr(ticker, tickers)
    df = pd.read_csv(f"./stocks/{ticker}.csv")
    for stock in top_corr:
        high_corr_stock = pd.read_csv(f"./stocks/{stock}.csv")
        df[stock] = high_corr_stock['Close']


def fix_csv(ticker):
    add_highest_corr_stocks(ticker)


def main():
    t1 = time.perf_counter()
    splits = np.array_split(tickers, 25)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(create_threads, splits)
    t2 = time.perf_counter()
    print(f'Finished in {t2 - t1} seconds')


if __name__ == '__main__':
    main()
