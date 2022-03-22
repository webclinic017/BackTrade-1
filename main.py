from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from run_strategy import Run_strategy
from dateutil.relativedelta import relativedelta
from Strategies.bollinger_three import Bollinger_three
from Strategies.ADX_strategy import adx_strat
from Strategies.alligator_strategy import Alligator_strategy
from Strategies.CMF_ATR_MACD_strategy import MACD_CMF_ATR_Strategy
from Strategies.TEMA_MACD_NEW import TEMA_MACD_NEW
from Strategies.temea20_tema60 import Tema20_tema60
import datetime
import re

if __name__ == '__main__':
    f = open("Green list (4).txt", "r")
    list = f.read()
    tickers = []
    list2 = list.split(",")
    for ticker in list2:
        tickers.append(ticker.split(":")[1])
    start_date = datetime.date.today() - relativedelta(years=2)
    # end_date = "2021-09-23"
    # intervals = {"30m": "2021-09-01", "1h": "2021-08-25", "90m": "2021-08-01", "1d": "2021-06-01"}
    interval = "1d"
    strategies = [Bollinger_three,adx_strat,Alligator_strategy,MACD_CMF_ATR_Strategy,TEMA_MACD_NEW,Tema20_tema60]
    parameters = dict(cash=10000,
                      macd1=12,
                      macd2=26,
                      macdsig=9,
                      atrperiod=14,
                      atrdist=2.0,
                      order_pct=1.0, )
    for ticker in tickers:
        for strategy in strategies:
            run_cerebro = Run_strategy(parameters, strategy)
            percentage = run_cerebro.runstrat(ticker, start_date, interval)

