import pandas as pd
import yfinance as yf
import time
import pandas_ta as ta
import glob

START = "2019-05-01"
END = "2022-05-01"
INTERVAL = '1d'
STOCKSCSV = "Stocks in the SP 500 Index.csv"
SP500TICKER = "^GSPC"
PERIOD = "3y"
SNPPATH = "S&P500.csv"
path = "c:/users/roeym/desktop/backtrade/dates/*.csv"


def clear_unnamed():
    for date in dates:
        df = pd.read_csv(f"./dates/{date}.csv")
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df.to_csv(f"./dates/{date}.csv")


def get_advance_decline_ratio():
    adr, add = [], []
    for date in dates:
        date_df = pd.read_csv(f"./dates/{date}.csv")
        advance = (date_df['PriceUp'] == 1).sum()
        decline = (date_df['PriceDown'] == 1).sum()
        if decline == 0:
            decline = 0.0000000000001
        ad_ratio = advance / decline
        ad_difference = advance - decline
        date_df['AD_difference'] = ad_difference
        date_df['AD_RATIO'] = ad_ratio
        date_df.to_csv(f"./dates/{date}.csv")
        add.append(ad_difference)
        adr.append(ad_ratio)
    df_sp['AD_difference'] = add
    df_sp['AD_ratio'] = adr
    df_sp.to_csv(SNPPATH)


def calc_mcclellan():
    df = pd.read_csv(SNPPATH, index_col=[0])
    add = df['AD_difference']
    ema19 = ta.ema((add * 0.1), 19)
    ema39 = ta.ema((add * 0.05), 39)
    mcclellanosc = ema19 - ema39
    df['mcclellanOSC'] = mcclellanosc
    mcclellansum = mcclellanosc.cumsum()
    df['mcclellanSUM'] = mcclellansum
    df.to_csv(SNPPATH)
    for index, date in enumerate(dates):
        if index >= 38:
            curr_df = pd.read_csv(f"./dates/{date}.csv")
            curr_df['mcclellanSUM'] = mcclellansum[index]
            curr_df['mcclellanOSC'] = mcclellanosc[index]
            curr_df.to_csv(f"./dates/{date}.csv")


def get_high_corr(ticker):
    req_df = pd.read_csv(f"./stocks/{ticker}.csv")
    req_close = req_df['Close']
    corr = []
    tickers.remove(ticker)
    for stock in tickers:
        test_df = pd.read_csv(f"./stocks/{stock}.csv")
        test_close = test_df['Close']
        corr.append(test_close.corr(req_close))
    top3 = sorted(zip(corr, tickers), reverse=True)[:3]
    return [x[1] for x in top3]


def get_dates(tickers):
    ex_tick = tickers[0]
    ex_ticker_df = pd.read_csv(f"./stocks/{ex_tick}.csv")
    dates_list = ex_ticker_df['Date']
    return dates_list


def create_Sp500():
    stock = yf.Ticker(SP500TICKER)
    df_sp = stock.history(start=START, end=END, interval=INTERVAL)
    df_sp = df_sp.drop(columns=['Dividends', 'Stock Splits'])
    df_sp.to_csv(f"S&P500.csv")
    return df_sp


def get_tickers():
    sandp500 = pd.read_csv(STOCKSCSV)
    ticks = sandp500['Symbol']
    return ticks


def get_columns():
    ex_tick = tickers[0]
    ex_ticker_df = pd.read_csv(f"./stocks/{ex_tick}.csv")
    columns_list = ex_ticker_df.columns.values.tolist()
    return columns_list


def creating_dates():
    columns.remove('Date')
    for date in dates:
        df = pd.DataFrame(columns=columns)
        df.to_csv(f"./dates/{date}.csv")


def stocks_to_dates():
    bad_stocks = []
    for index, ticker in enumerate(tickers):
        try:
            print(f"currently at {index + 1} out of {len(tickers)}")
            ticker_df = pd.read_csv(f"./stocks/{ticker}.csv")
            for date in dates:
                curr_date_df = pd.read_csv(f"./dates/{date}.csv", index_col=[0])
                row = ticker_df.loc[ticker_df['Date'] == date].values[0].tolist()[1:]
                curr_date_df.loc[len(curr_date_df.index)] = row
                curr_date_df.to_csv(f"./dates/{date}.csv")
        except:
            bad_stocks.append(ticker)
    print(bad_stocks)


if __name__ == '__main__':
    t1 = time.perf_counter()
    # df_sp = create_Sp500()
    df_sp = pd.read_csv(SNPPATH)
    tickers = get_tickers()
    dates = get_dates(tickers)
    columns = get_columns()
    creating_dates()
    stocks_to_dates()
    get_advance_decline_ratio()
    calc_mcclellan()
    t2 = time.perf_counter()
    print(f'Finished in {t2 - t1} seconds')
