# -*-coding:utf-8-*-
# 常规涨停后走势
# 涨停次日收盘未涨停，次日的走势


import sys
import os
import numpy as np
import datetime
import matplotlib.pyplot as plt
from QuadQuanta.core.strategy import BaseStrategy
from QuadQuanta.utils.logs import logger
from QuadQuanta.data.mongodb_api import query_mongodb, save_mongodb
from QuadQuanta.data.get_data import get_trade_days, get_bars, get_securities_info
import talib

FILENAME = os.path.basename(sys.argv[0]).split(".py")[0]


class LimitTrend(BaseStrategy):
    def __init__(self,
                 code=None,
                 start_date=None,
                 end_date=None,
                 frequency='day', init_cash=100000):
        super(LimitTrend, self).__init__(code, start_date, end_date,
                                         frequency, init_cash=init_cash)
        self.history_N_data = []
        self.symbol_limit_date = {}
        self.total_assert = []
        self.hold_day = 1
        self.delta_day = 5
        self.success_rate = 74
        logger.info("success_rate", self.success_rate)

    def sys_init(self):
        pass

    def init(self):
        self.symbol_list = []
        self.positon_list = []
        self.success_count = 0
        self.failed_count = 0
        self.break_success_count = 0
        self.break_failed_count = 0
        self.nice_symbol = []
        self.limit_dict = {}
        self.trading_date = get_trade_days(self.start_date, self.end_date)

    def on_day_bar(self, next_bars, next_two_bars):
        next_bar = next_bars[-1]
        next_two_bar = next_two_bars[-1]
        self.res_dict = {}

        close = round(next_bar['pre_close'], 2)
        code = next_bar['code']
        next_open_rate = round(100 * (next_bar['open'] - close) / close, 2)
        next_close_rate = round(100 * (next_bar['close'] - close) / close, 2)
        next_high_rate = round(100 * (next_bar['high'] - close) / close, 2)
        next_low_rate = round(100 * (next_bar['low'] - close) / close, 2)
        next_date = next_bar['date']
        next_close = round(next_bar['close'],2)
        next_high = round(next_bar['high'],2)
        next_high_limit = round(next_bar['high_limit'],2)

        self.res_dict['_id'] = next_date + '-' + code
        self.res_dict['code'] = code
        self.res_dict['next_date'] = next_date
        if next_high < next_high_limit:
            self.res_dict['limit'] = 0
        elif next_close < next_high_limit:
            self.res_dict['limit'] = 1
        else:
            self.res_dict['limit'] = 2

        self.res_dict['next_open'] = next_open_rate
        self.res_dict['next_close'] = next_close_rate
        self.res_dict['next_high'] = next_high_rate
        self.res_dict['next_low'] = next_low_rate


        next_two_open_rate = round(100 * (next_two_bar['open'] - next_close) / next_close, 2)
        next_two_close_rate = round(100 * (next_two_bar['close'] - next_close) / next_close, 2)
        next_two_high_rate = round(100 * (next_two_bar['high'] - next_close) / next_close, 2)
        next_two_low_rate = round(100 * (next_two_bar['low'] - next_close) / next_close, 2)

        self.res_dict['next_two_open'] = next_two_open_rate
        self.res_dict['next_two_close'] = next_two_close_rate
        self.res_dict['next_two_high'] = next_two_high_rate
        self.res_dict['next_two_low'] = next_two_low_rate

        import time
        time.sleep(0.01)

        save_mongodb('QuadQuanta', 'limit_trend', self.res_dict)

    def syn_backtest(self):

        for i in range(1, len(self.trading_date) - 1):
            try:
                # 每日标的列表

                date = self.trading_date[i]
                next_date = self.trading_date[i + 1]
                pre_date = self.trading_date[i - 1]
                self.during_limit_dict = query_mongodb('QuadQuanta', 'daily_limit', sql={
                    'date': pre_date})
                logger.info(f"{date}")
                self.during_double_limit = [symboldata['code'] for symboldata in self.during_limit_dict]
                self.symbol_list = list(set(self.during_double_limit))

                self.next_bar_data = get_bars(self.symbol_list, end_time=date, count=self.hold_day)
                self.next_two_bar_data = get_bars(self.symbol_list, end_time=next_date, count=self.hold_day)

                for symbol in self.symbol_list:
                    next_bars = self.next_bar_data[self.next_bar_data['code'] == symbol]
                    next_two_bars = self.next_two_bar_data[self.next_two_bar_data['code'] == symbol]
                    if str(next_bars[0]['code']).startswith('688') or str(next_bars[0]['code']).startswith('30'):
                        continue
                    self.on_day_bar(next_bars, next_two_bars)

            except Exception as e:
                print(e)


if __name__ == '__main__':
    import datetime

    today = datetime.date.today()
    end_time = str(today)
    trade_days_until_today = get_trade_days(start_time='2014-01-01',
                                            end_time=end_time)
    start_time = trade_days_until_today[-10]

    test = LimitTrend(start_date='2021-01-01',
                      end_date='2021-10-31',
                      frequency='daily', init_cash=10000000)

    test.syn_backtest()
