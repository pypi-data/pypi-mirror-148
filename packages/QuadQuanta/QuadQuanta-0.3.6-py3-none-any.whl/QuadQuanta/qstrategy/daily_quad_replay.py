# -*-coding:utf-8-*-
# 四板股
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


class QuadLimit(BaseStrategy):
    def __init__(self,
                 code=None,
                 start_date=None,
                 end_date=None,
                 frequency='day', init_cash=100000):
        super(QuadLimit, self).__init__(code, start_date, end_date,
                                        frequency, init_cash=init_cash)
        self.pre_volume_dict = {}
        self.pre_data_dict = {}
        self.double_limit_list = []
        self.fall_symbol_list = []
        self.break_symbol_list = []
        self.history_N_data = []
        self.symbol_limit_date = {}
        self.total_assert = []
        self.hold_day = 5


    def init(self):
        self.bought_symbols = []
        self.success_count = 0
        self.failed_count = 0
        self.sccess_list = []
        self.failed_list = []
        self.trading_date = get_trade_days(self.start_date, self.end_date)
        self.all_securities_info = get_securities_info(format='pandas')


    def on_bar(self, bars):
        bar = bars[-1]
        code = bar['code']
        current_day = bar['date']
        current_date = datetime.date.fromisoformat(current_day)
        close = round(bar['close'], 2)
        high = round(bar['high'], 2)

        low = round(bar['low'], 2)
        pre_close = bar['pre_close']
        low_rate = 100 * (low - pre_close) / pre_close
        close_rate = 100 * (close - pre_close) / pre_close
        limit = round(bar['high_limit'], 2)
        pre_bar = bars[-2]
        pre_limit = round(pre_bar['high_limit'], 2)
        pre_close = round(pre_bar['close'], 2)
        pre_2_bar = bars[-3]
        pre_2_limit = round(pre_2_bar['high_limit'], 2)
        pre_2_close = round(pre_2_bar['close'], 2)
        pre_3_bar = bars[-4]
        pre_3_limit = round(pre_3_bar['high_limit'], 2)
        pre_3_close = round(pre_3_bar['close'], 2)
        pre_2_close_rate = 100 * (pre_2_close - pre_3_close) / pre_3_close
        pre_close_rate = 100 * (pre_close - pre_2_close) / pre_3_close

        # if pre_3_close == pre_3_limit:
        if pre_2_close < pre_2_limit:
            if pre_close == pre_limit:
                start_date = datetime.date.fromisoformat(self.all_securities_info.loc[code]['start_date'])
                if current_date - start_date > datetime.timedelta(days=100) and pre_close_rate > 9:
                    if close == limit:
                        if low < close:
                            self.sccess_list.append(code)
                            self.success_count += 1

                    elif high == limit:
                        self.failed_list.append(code)
                        self.failed_count += 1
                    else:
                        pass



    def syn_backtest(self):

        for i in range(0, len(self.trading_date)):
            try:
                date = self.trading_date[i]
                logger.info(f"{date}")

                self.history_N_data = get_bars(self.subscribe_code, end_time=date, count=self.hold_day)
                for symbol in self.subscribe_code:
                    try:
                        if str(symbol).startswith('688'):
                            continue
                        bars = self.history_N_data[self.history_N_data['code'] == symbol]
                        self.on_bar(bars)
                    except Exception as e:
                        pass
                        # print(e, symbol)
                logger.info(f"四板成功:{self.sccess_list}")
                logger.info(f"四板失败:{self.failed_list}")
                self.sccess_list = []
                self.failed_list = []
            except Exception as e:
                print(e)
        logger.info(f"成功个数:{self.success_count}")
        logger.info(f"失败次数:{self.failed_count}")

if __name__ == '__main__':
    import datetime

    today = datetime.date.today()
    end_time = str(today)
    trade_days_until_today = get_trade_days(start_time='2014-01-01',
                                            end_time=end_time)
    start_time = trade_days_until_today[-4]

    test = QuadLimit(start_date='2021-06-01',
                     end_date='2021-10-30',
                     frequency='daily', init_cash=10000000)

    test.syn_backtest()
