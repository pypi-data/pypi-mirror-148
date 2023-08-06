# -*-coding:utf-8-*-
# 近期活跃涨停（封板成功率高）


import sys
import os
import numpy as np
import datetime
import matplotlib.pyplot as plt
from QuadQuanta.core.strategy import BaseStrategy
from QuadQuanta.utils.logs import logger
from QuadQuanta.data.mongodb_api import save_mongodb, query_mongodb
from QuadQuanta.data.get_data import get_trade_days, get_bars, get_securities_info
import talib

FILENAME = os.path.basename(sys.argv[0]).split(".py")[0]


class ActiveLimit(BaseStrategy):
    def __init__(self,
                 code=None,
                 start_date=None,
                 end_date=None,
                 frequency='day', init_cash=100000):
        super(ActiveLimit, self).__init__(code, start_date, end_date,
                                          frequency, init_cash=init_cash)
        self.history_N_data = []
        self.symbol_limit_date = {}
        self.total_assert = []
        # 活跃持续时间
        self.hold_day = 30
        self.delta_day = 5
        self.success_rate = 74

    def init(self):
        self.symbol_list = []
        self.success_count = 0
        self.failed_count = 0
        self.break_success_count = 0
        self.break_failed_count = 0
        self.nice_symbol = []
        self.limit_dict = {}
        self.trading_date = get_trade_days(self.start_date, self.end_date)
        # 所有股票概况
        self.all_securities_info = get_securities_info(format='pandas')

    def get_success_rate(self, N_data: np.ndarray):
        limit_count = 0
        success_limit_count = 0
        code = N_data['code'][0]
        for bar in N_data:

            close = round(bar['close'], 2)
            high = round(bar['high'], 2)
            limit = round(bar['high_limit'], 2)
            if high == limit:
                limit_count += 1
                if close == limit:
                    success_limit_count += 1
        if limit_count == 0:
            success_limit_rate = 0
        else:
            success_limit_rate = int(100 * (success_limit_count / limit_count))
        self.limit_dict[code] = [limit_count, success_limit_rate]

    def on_day_bar(self, bars):
        bar = bars[-1]
        pre_bar = bars[-2]
        code = bar['code']
        max_high = np.max(bars[:-1]['high'])
        close = round(bar['close'], 2)
        high = round(bar['high'], 2)
        limit = round(bar['high_limit'], 2)
        pre_limit = round(pre_bar['high_limit'], 2)
        pre_close = round(bar['pre_close'], 2)
        high_limit_rate = 100 * (limit - pre_close) / pre_close

        self.get_success_rate(bars)
        if high_limit_rate > 8 and pre_close < pre_limit:
            if (self.limit_dict[code][0] > 1 and self.limit_dict[code][1] > self.success_rate) or (
                    self.limit_dict[code][0] > 3):
                self.nice_symbol.append(code)

    def syn_backtest(self):

        for i in range(0, len(self.trading_date)):

            # 每日标的列表

            date = self.trading_date[i]
            logger.info(f"{date}")

            current_date = datetime.date.fromisoformat(date)

            self.history_N_data = get_bars(self.subscribe_code, end_time=date, count=self.hold_day)

            # 排除连板票
            self.double_limit_dict = query_mongodb('QuadQuanta', 'daily_double_limit', sql={
                '_id': {'$lt': date}
            })[-self.hold_day:]
            self.double_limit_list = [symbol for symbol_data in self.double_limit_dict for symbol in
                                      symbol_data['symbol_list']]
            for symbol in self.subscribe_code:
                try:
                    # 上市日期
                    start_date = datetime.date.fromisoformat(self.all_securities_info.loc[symbol]['start_date'])
                    if (current_date - start_date) < datetime.timedelta(days=100) or symbol in self.double_limit_list:
                        continue
                    bars = self.history_N_data[self.history_N_data['code'] == symbol]
                    if str(bars[0]['code']).startswith('688'):
                        continue
                    self.on_day_bar(bars)
                except Exception as e:
                    print(e)
            # self.symbol_list += self.nice_symbol
            logger.info(self.nice_symbol)
            save_mongodb('QuadQuanta', 'daily_active_limit', {'_id': date, 'symbol_list': self.nice_symbol})
            self.nice_symbol = []

        logger.info(f"success count:{self.success_count}, failed_cout:{self.failed_count}")


if __name__ == '__main__':
    import datetime
    from QuadQuanta.data.update_data import update_day_bar
    from QuadQuanta.data.save_data import save_securities_info

    try:
        logger.info("更新bar数据...")
        update_day_bar()
    except Exception as e:
        print(e)

    today = datetime.date.today()
    end_time = str(today)
    trade_days_until_today = get_trade_days(start_time='2014-01-01',
                                            end_time=end_time)
    start_time = trade_days_until_today[-2]
    try:
        logger.info("更新股票概况...")
        save_securities_info()
    except Exception as e:
        print(e)
    test = ActiveLimit(start_date=start_time,
                       end_date=end_time,
                       frequency='daily', init_cash=10000000)
    # test = ActiveLimit(start_date='2021-01-01',
    #                    end_date='2021-10-28',
    #                    frequency='daily', init_cash=10000000)
    test.syn_backtest()
