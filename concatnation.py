import pandas as pd
import yfinance as yf
import time
import otherfunctions as of
import numpy as np


def concatnate_date():
    for index, date in enumerate(dates):
        print(f"currently at {index + 1} out of {len(dates)}")
        df = pd.read_csv(f"./dates/{date}.csv")

        df.to_csv(f"./dates/{date}.csv")



if __name__ == '__main__':
    t1 = time.perf_counter()
    tickers = of.get_tickers()
    dates = of.get_dates(tickers)

    t2 = time.perf_counter()
    print(f'Finished in {t2 - t1} seconds')
