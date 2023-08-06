# -*-coding:utf-8-*-
# 二板涨停后 十日线的买点
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


class DoubleLimitMA10(BaseStrategy):
    def __init__(self,
                 code=None,
                 start_date=None,
                 end_date=None,
                 frequency='day', init_cash=100000):
        super(DoubleLimitMA10, self).__init__(code, start_date, end_date,
                                              frequency, init_cash=init_cash)
        self.pre_volume_dict = {}
        self.pre_data_dict = {}
        self.double_limit_list = []
        self.fall_symbol_list = []
        self.break_symbol_list = []
        self.history_N_data = []
        self.symbol_limit_date = {}
        self.total_assert = []
        self.hold_day = 60
        # 取多少日内的二连板
        self.during_day = 10

    def init(self):
        self.bought_symbols = []
        self.success_count = 0
        self.failed_count = 0
        self.trading_date = get_trade_days(self.start_date, self.end_date)

    def sys_init(self):
        pass

    def on_bar(self, bars):
        bar = bars[-1]
        code = bar['code']
        current_day = bar['date']
        close = round(bar['close'], 2)
        high = round(bar['high'], 2)
        low = round(bar['low'], 2)
        pre_close = bar['pre_close']
        low_rate = 100 * (low - pre_close) / pre_close
        limit = round(bar['high_limit'], 2)
        pre_bar = bars[-2]
        pre_low = round(pre_bar['low'], 2)
        pre_high = round(pre_bar['high'], 2)
        pre_2close = round(pre_bar['pre_close'], 2)
        MA60 = talib.SMA(bars['close'], 60)[-1]
        MA20 = talib.SMA(bars['close'], 20)[-1]
        MA10 = talib.SMA(bars['close'], 10)[-1]
        MA5 = talib.SMA(bars['close'], 5)[-1]

        if close > MA10:
            if MA5 > MA10 and MA10 > MA20 and MA20 > MA60:
                self.double_limit_list.append(code)

    def syn_backtest(self):

        for i in range(0, len(self.trading_date)):
            try:
                date = self.trading_date[i]
                logger.info(f"{date}")
                self.during_double_limit_dict = query_mongodb('QuadQuanta', 'daily_double_limit', sql={
                    '_id': {'$lte': date}
                })[-self.during_day:]
                self.during_double_limit = [symbol for symbol_data in self.during_double_limit_dict for symbol in
                                            symbol_data['symbol_list']]
                self.history_N_data = get_bars(self.during_double_limit, end_time=date, count=self.hold_day)
                for symbol in self.during_double_limit:
                    if str(symbol).startswith('688'):
                        continue
                    bars = self.history_N_data[self.history_N_data['code'] == symbol]
                    self.on_bar(bars)

                logger.info(f"连板:{set(self.double_limit_list)}")
                self.double_limit_list = []
            except Exception as e:
                print(e)


if __name__ == '__main__':
    import datetime

    today = datetime.date.today()
    end_time = str(today)
    trade_days_until_today = get_trade_days(start_time='2014-01-01',
                                            end_time=end_time)
    start_time = trade_days_until_today[-4]

    test = DoubleLimitMA10(start_date=start_time,
                           end_date=end_time,
                           frequency='daily', init_cash=10000000)

    # test = DoubleLimitMA10(start_date='2021-06-01',
    #                        end_date='2021-06-11',
    #                        frequency='daily', init_cash=10000000)
    test.syn_backtest()
