# -*-coding:utf-8-*-
# 波动率计算

import sys
import os
import numpy as np
import datetime
import matplotlib.pyplot as plt
from QuadQuanta.core.strategy import BaseStrategy
from QuadQuanta.utils.logs import logger
from QuadQuanta.data.mongodb_api import insert_mongodb, query_mongodb
from QuadQuanta.data.get_data import get_trade_days, get_bars, get_securities_info
import talib

FILENAME = os.path.basename(sys.argv[0]).split(".py")[0]


class Vola(BaseStrategy):
    def __init__(self,
                 code=None,
                 start_date=None,
                 end_date=None,
                 frequency='day', init_cash=100000):
        super(Vola, self).__init__(code, start_date, end_date,
                                   frequency, init_cash=init_cash)

    def init(self):
        self.hold_day = 5

        self.trading_date = get_trade_days(self.start_date, self.end_date)

    def sys_init(self):
        pass

    def on_bar(self, bars):
        bar = bars[-1]
        code = bar['code']
        current_day = bar['date']
        close = bars['close']
        high = bars['high']
        low = bars['low']
        volume = bars['volume']
        amount = bars['amount']


        atr = talib.TRANGE(high, low, close)
        volatility = 100 * atr[1:] / close[:-1]
        # 每万手波动率
        norm_volatility = pow(10, 6) * volatility / volume[1:]
        # 每亿元波动率
        amount_volatility = pow(10, 8) * volatility / amount[1:]


        # print((atr))
        # if (norm_volatility[-2] > 1.1 * norm_volatility[-3]) and (norm_volatility[-4] > 1.1 * norm_volatility[-3]):
        print(f"{current_day} : {code}")
        # print(f"波动率{volatility}")
        print(f"每万手波动率: {norm_volatility}")
        print(f"每亿元波动率: {amount_volatility}")

    def syn_backtest(self):

        for i in range(0, len(self.trading_date)):
            try:
                date = self.trading_date[i]
                logger.info(f"{date}")
                self.during_double_limit_dict = query_mongodb('QuadQuanta', 'daily_double_limit', sql={
                    '_id': {'$lte': date}
                })[-10:-2]
                self.during_double_limit = [symbol for symbol_data in self.during_double_limit_dict for symbol in
                                            symbol_data['symbol_list']]
                self.history_N_data = get_bars(self.during_double_limit, end_time=date, count=self.hold_day)
                for symbol in self.during_double_limit:
                    if str(symbol).startswith('688'):
                        continue
                    bars = self.history_N_data[self.history_N_data['code'] == symbol]
                    self.on_bar(bars)
            except Exception as e:
                print(e)


if __name__ == '__main__':
    import datetime

    today = datetime.date.today()
    end_time = str(today)
    trade_days_until_today = get_trade_days(start_time='2014-01-01',
                                            end_time=end_time)
    start_time = trade_days_until_today[-2]

    test = Vola(start_date=start_time,
                end_date=end_time,
                frequency='daily', init_cash=10000000)

    test.syn_backtest()
