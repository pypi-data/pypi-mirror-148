# -*-coding:utf-8-*-
# 横盘待突破个股
# 10日内涨停，当前股价在10日线上方 小于1.1*五日均价
# -*-coding:utf-8-*-

import numpy as np
import time
from QuadQuanta.core.strategy import BaseStrategy
from QuadQuanta.utils.logs import logger
from QuadQuanta.data.mongodb_api import insert_mongodb
from QuadQuanta.data.get_data import get_trade_days, get_bars
import talib


class HoldBreak(BaseStrategy):
    def __init__(self,
                 code=None,
                 start_date=None,
                 end_date=None,
                 frequency='day'):
        super(HoldBreak, self).__init__(code, start_date, end_date,
                                        frequency)
        self.period = 25
        self.pre_volume_dict = {}
        self.limit_symbol_list = []
        self.fall_symbol_list = []
        self.break_symbol_list = []

    def init(self):
        pass

    def on_bars(self, bars):
        # 涨停标志
        limit_flag = False
        # 涨停次数标志
        count_flag = True
        MA10 = talib.SMA(bars['close'], 10)
        MA5 = talib.SMA(bars['close'], 5)
        symbol_data = {}
        for i, bar in enumerate(bars[10:]):
            if count_flag and round(bar['close'], 2) == round(bar['high_limit'], 2) and i < 13:
                limit_flag = True
                count_flag = False
            if limit_flag:
                close = bar['close']
                # 任意一天低于10日线退出
                if close < round(MA10[i + 10], 2):
                    break
                if i == (len(bars) - 11):
                    if close < round(MA5[i+10], 2) * 1.1:
                        if bars['amount'][-1] > pow(10, 8):
                            symbol = bars['code'][-1]
                            date = bars['date'][-1]
                            symbol_data['_id'] = date + '-' + symbol
                            symbol_data['code'] = symbol
                            symbol_data['date'] = date

                            insert_mongodb('QuadQuanta', 'hold_to_break', symbol_data)
                            self.symbol_list.append(bars['code'][-1])
                    else:
                        break

    def syn_backtest(self):
        for i in range(0, len(self.trading_date)):
            try:
                self.symbol_list = []
                date = self.trading_date[i]
                self.history_N_data = get_bars(code=self.subscribe_code, end_time=date, count=self.period)
                self.code_list = np.unique(self.day_data['code'])
                for code in self.code_list:
                    bars = self.history_N_data[self.history_N_data['code'] == code]
                    self.on_bars(bars)
                logger.info(f"{date}")
                logger.info(f"{self.symbol_list}")
            except Exception as e:
                print(e)
                continue


if __name__ == '__main__':
    import datetime

    today = datetime.date.today()
    end_time = str(today)
    trade_days_until_today = get_trade_days(start_time='2014-01-01',
                                            end_time=end_time)
    start_time = trade_days_until_today[-2]
    test = HoldBreak(start_date=start_time,
                     end_date=end_time,
                     frequency='daily')

    test.syn_backtest()
