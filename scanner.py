import time
import concurrent.futures
import yfinance as yf
import numpy as np
import talib
import pandas as pd


def get_tickers():
    ticks = []
    f = open("S&P 500.txt", "r")
    list_of_tickers = f.read().split(",")
    for ticker in list_of_tickers:
        ticks.append(ticker.split(":")[1])
    return ticks


def create_threads(splits):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(create_csv, splits)


def create_csv(ticker):
    stock = yf.Ticker(ticker)
    df = stock.history(period="5y")
    df = df.drop(columns=['Stock Splits'])
    df['Market Cap'] = df['Open'] * df['Volume']
    df['ma50'] = df['Open'].rolling(50).mean()
    df['ma200'] = df['Open'].rolling(200).mean()
    df['DPC'] = df['Open'] / df['Open'].shift(1) - 1
    df['Cumulative Return'] = (1 + df['DPC']).cumprod()
    df['ATR'] = talib.ATR(df['High', 'Low', 'Close'], 14)
    op = df['Open']
    hi = df['High']
    lo = df['Low']
    cl = df['Close']
    candle_names = talib.get_function_groups()['Pattern Recognition']
    for candle in candle_names:
        df[candle] = getattr(talib, candle)(op, hi, lo, cl)
    df.to_csv(f"./stocks/{ticker}.csv")


# advance decline
def main():
    t1 = time.perf_counter()
    # tickers = get_tickers()
    tickers = ['SPY', 'TSLA']
    splits = np.array_split(tickers, 25)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(create_threads, splits)
    t2 = time.perf_counter()
    print(f'Finished in {t2 - t1} seconds')


if __name__ == '__main__':
    main()
