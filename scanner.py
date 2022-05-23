import time
import concurrent.futures
import yfinance as yf
import numpy as np
import talib
import pandas as pd
import otherfunctions as of
import pandas_ta as ta
from warnings import simplefilter

simplefilter(action="ignore", category=pd.errors.PerformanceWarning)
vix = yf.Ticker('^VIX')
vix = vix.history(period="5y")
vvix = yf.Ticker('^VVIX')
vvix = vvix.history(period="5y")
vxn = yf.Ticker('^VXN')
vxn = vxn.history(period="5y")
candle_names = talib.get_function_groups()['Pattern Recognition']



def create_threads(splits):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(create_csv, splits)


def add_candles(df):
    for candle in candle_names:
        df[candle] = getattr(talib, candle)(df['Open'], df['High'], df['Low'], df['Close'])


def add_indicators(df):
    df['ma50'] = df['Open'].rolling(50).mean()
    df['ma200'] = df['Open'].rolling(200).mean()
    df['ADX'] = talib.ADX(df['High'], df['Low'], df['Close'], timeperiod=14)
    df['ADXR'] = talib.ADXR(df['High'], df['Low'], df['Close'], timeperiod=14)
    df['AROONOSC'] = talib.AROONOSC(df['High'], df['Low'], timeperiod=14)
    df['DX'] = talib.DX(df['High'], df['Low'], df['Close'], timeperiod=14)
    df['PPO'] = talib.PPO(df['Close'], fastperiod=12, slowperiod=26)
    df['stochK'], df['stochD'] = talib.STOCH(df['High'], df['Low'], df['Close'], fastk_period=5, slowk_period=3,
                                             slowk_matype=0, slowd_period=3, slowd_matype=0)
    df['TRIX'] = talib.TRIX(df['Close'], timeperiod=14)
    df['ULTOSC'] = talib.ULTOSC(df['High'], df['Low'], df['Close'], timeperiod1=7, timeperiod2=14, timeperiod3=28)
    df['MACD'], df['MACDSIG'], df[' MACDHIST'] = talib.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
    df['TRANGE'] = talib.TRANGE(df['High'], df['Low'], df['Close'])
    indicators = [df.ta.ao(), df.ta.apo(), df.ta.bias(), df.ta.bop(), df.ta.cci(), df.ta.cfo(), df.ta.cg(), df.ta.cmo(),
                  df.ta.coppock(), df.ta.cti(), df.ta.inertia(), df.ta.mom(), df.ta.pgo(), df.ta.psl(), df.ta.roc(),
                  df.ta.rsi(), df.ta.rsx(), df.ta.slope(), df.ta.uo(), df.ta.willr(), df.ta.alma(), df.ta.dema(),
                  df.ta.wma(), df.ta.fwma(), df.ta.hma(), df.ta.hwma(), df.ta.jma(), df.ta.kama(),
                  df.ta.linreg(), df.ta.mcgd(), df.ta.pwma(), df.ta.rma(), df.ta.sinwma(), df.ta.swma(), df.ta.t3(),
                  df.ta.tema(), df.ta.trima(), df.ta.vidya(), df.ta.vwma(), df.ta.zlma(), df.ta.chop(),
                  df.ta.increasing(), df.ta.qstick(), df.ta.ttm_trend(), df.ta.vhf(), df.ta.atr(),
                  df.ta.massi(), df.ta.pdist(), df.ta.rvi(),
                  df.ta.true_range(), df.ta.ui(), df.ta.ad(), df.ta.adosc(),
                  df.ta.cmf(), df.ta.efi(), df.ta.mfi(), df.ta.obv(), df.ta.pvol(), df.ta.pvr(), df.ta.pvt(),
                  df.ta.ebsw()]
    names = ['ao', 'apo', 'bias', 'bop', 'cci', 'cfo', 'cg', 'cmo', 'coppock', 'cti', 'inertia', 'mom', 'pgo', 'psl',
             'roc', 'rsi', 'rsx', 'slope', 'uo', 'willr', 'alma', 'dema', 'wma', 'fwma', 'hma', 'hwma', 'jma', 'kama',
             'linreg', 'mcgd', 'pwma', 'rma', 'sinwma', 'swma', 't3', 'tema', 'trima', 'vidya', 'vwma', 'zlma', 'chop',
             'increasing', 'qstick', 'ttm_trend', 'vhf', 'atr', 'massi', 'pdist', 'rvi', 'true_range', 'ui',
             'ad', 'adosc', 'cmf', 'efi', 'mfi', 'obv', 'pvol', 'pvr', 'pvt', 'ebsw']
    for name, indicator in zip(names, indicators):
        df[name] = indicator


def add_other(df):
    df['VIX'] = vix['Close']
    df['VVIX'] = vvix['Close']
    df['VXN'] = vxn['Close']
    df['Market Cap'] = df['Open'] * df['Volume']
    df['DPC'] = df['Open'] / df['Open'].shift(1) - 1
    df['Cumulative Return'] = (1 + df['DPC']).cumprod()


def create_csv(ticker):
    stock = yf.Ticker(ticker)
    df = stock.history(period="5y")
    df = df.drop(columns=['Stock Splits'])
    add_candles(df)
    add_indicators(df)
    add_other(df)
    df.to_csv(f"./stocks/{ticker}.csv")


def main():
    t1 = time.perf_counter()
    ticker = 'TSLA'

    tickers = of.get_tickers()
    print(of.get_high_corr(ticker, tickers))
    exit()
    tickers = ['SPY', 'TSLA']
    splits = np.array_split(tickers, 25)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(create_threads, splits)
    t2 = time.perf_counter()
    print(f'Finished in {t2 - t1} seconds')


if __name__ == '__main__':
    main()
