#-*-coding:utf-8-*-
# 分析换手四板以上的接入点
# -*-coding:utf-8-*-

import numpy as np
import time
from QuadQuanta.core.strategy import BaseStrategy
from QuadQuanta.data.clickhouse_api import query_clickhouse
from QuadQuanta.portfolio import Account
from QuadQuanta.utils.logs import logger
from QuadQuanta.data.mongodb_api import insert_mongodb, save_mongodb, query_mongodb
from QuadQuanta.data.get_data import get_trade_days, get_securities_info,get_bars
from pymongo.errors import DuplicateKeyError


class DailyQuadReplay(BaseStrategy):
    def __init__(self,
                 code=None,
                 start_date=None,
                 end_date=None,
                 frequency='day'):
        super(DailyQuadReplay, self).__init__(code, start_date, end_date,
                                              frequency)
        self.pre_volume_dict = {}
        self.limit_symbol_list = []
        self.fall_symbol_list = []
        self.break_symbol_list = []
        self.quad_symbol_list = []
        self.pre_data_dict = {}

    def init(self):
        self.all_securities_info = get_securities_info(format='pandas')
        self.daily_limit_symbol = []


    def all_limit(self,bars):
        if len(bars) < 3:
            return False
        for bar in bars:
            close = round(bar['close'],2)
            high_limit = round(bar['high_limit'],2)
            if close < high_limit:
                return False
        return True
    def on_bar(self, bars):
        pass


    def syn_backtest(self):
        for i in range(0, len(self.trading_date)):
            try:
                date = self.trading_date[i]
                self.daily_limit_dict = query_mongodb('QuadQuanta', 'daily_limit', sql={
                    'date': date})
                self.daily_limit_symbol = [symbol_data['code'] for symbol_data in self.daily_limit_dict]
                print(self.daily_limit_symbol)
                self.daily_break_symbol = []
                # self.daily_break_dict = query_mongodb('QuadQuanta', 'daily_break', sql={
                #     'date': date})
                # self.daily_break_symbol = [symbol_data['code'] for symbol_data in self.daily_break_dict]
                self.daiyl_symbol = self.daily_limit_symbol + self.daily_break_symbol
                self.history_N_data = get_bars(self.daiyl_symbol, end_time=date, count=4)
                for symbol in self.daiyl_symbol:
                    if str(symbol).startswith('688'):
                        continue
                    bars = self.history_N_data[self.history_N_data['code'] == symbol]
                    if self.all_limit(bars[:-1]):
                        self.quad_symbol_list.append(symbol)

                logger.info(f"{date}")
                logger.info(f"四连板：{self.quad_symbol_list}")
                # if len(self.quad_symbol_list) > 0:
                #     save_mongodb('QuadQuanta', 'daily_quad_limit', {'_id': date, 'symbol_list': self.quad_symbol_list})
                self.quad_symbol_list = []
            except Exception as e:
                print("exception:", e)
                continue


if __name__ == '__main__':
    import datetime
    from QuadQuanta.data.update_data import update_day_bar

    try:
        update_day_bar()
    except Exception as e:
        print(e)
    today = datetime.date.today()
    end_time = str(today)
    trade_days_until_today = get_trade_days(start_time='2014-01-01',
                                            end_time=end_time)
    start_time = trade_days_until_today[-10]
    test = DailyQuadReplay(start_date=start_time,
                           end_date=end_time,
                           frequency='daily')
    # test = DailyDoubleReplay(start_date='2019-05-01',
    #                          end_date='2019-05-28',
    #                          frequency='daily')

    test.syn_backtest()
