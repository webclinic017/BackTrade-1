import pandas as pd


# def get_advance_decline_ratio(stocklist):
#     def get_advance_decline_ratio(stocks_dict, df_indexes):
#         ad_ratios = pd.DataFrame(index=df_indexes, columns=['A/D Ratio', 'Advance', 'Decline'])
#     advance, decline = 0, 0
#     for stock in stocklist:
#         stock_df = pd.read_csv(f"./stocks/{stock}.csv")
#         stock_df['Change'] = round(stock_df['Close'].pct_change(), 3)
#         decline = (df['Change'] < 0).sum()
#         advance = (df['Change'] > 0).sum()
#     if decline == 0:
#         decline = 0.0000000000001
#
#     return ad_ratios


def get_high_corr(ticker, tickers):
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


def get_tickers():
    ticks = []
    f = open("S&P 500.txt", "r")
    list_of_tickers = f.read().split(",")
    for ticker in list_of_tickers:
        ticks.append(ticker.split(":")[1])
    return ticks


def creating_dates():
    tickers = get_tickers()
    exmpticker = tickers[0]
    exmp_df = pd.read_csv(f"./stocks/{exmpticker}.csv")
    dates = exmp_df['Date']
    columns = exmp_df.columns.values.tolist()
    columns.remove('Date')
    for date in dates:
        df = pd.DataFrame(columns=columns)
        df.to_csv(f"./dates/{date}.csv")


def stocks_to_dates():
    for index, ticker in enumerate(tickers):
        try:
            print(f"currently at {index + 1} out of 499")
            ticker_df = pd.read_csv(f"./stocks/{ticker}.csv")
            for date in dates:
                    curr_date_df = pd.read_csv(f"./dates/{date}.csv", index_col=[0])
                    row = ticker_df.loc[ticker_df['Date'] == date].values[0].tolist()[1:]
                    curr_date_df.loc[len(curr_date_df.index)] = row
                    curr_date_df.to_csv(f"./dates/{date}.csv")
        except:
            print(f"problem with ticker: {ticker} ")

            

if __name__ == '__main__':
    tickers = get_tickers()
    ex_tick = tickers[0]
    ex_ticker_df = pd.read_csv(f"./stocks/{ex_tick}.csv")
    dates = ex_ticker_df['Date']
    creating_dates()
    stocks_to_dates()
