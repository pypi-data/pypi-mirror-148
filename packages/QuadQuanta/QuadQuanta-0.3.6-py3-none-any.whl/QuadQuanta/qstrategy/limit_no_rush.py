#-*-coding:utf-8-*- 
# 涨停后未冲高个股
import numpy as np
import time
from QuadQuanta.core.strategy import BaseStrategy
from QuadQuanta.data.clickhouse_api import query_clickhouse
from QuadQuanta.portfolio import Account
from QuadQuanta.utils.logs import logger
from QuadQuanta.data.mongodb_api import insert_mongodb
from QuadQuanta.data.get_data import get_trade_days


class LimitNoRush(BaseStrategy):
    def __init__(self,
                 code=None,
                 start_date=None,
                 end_date=None,
                 frequency='day'):
        super(LimitNoRush, self).__init__(code, start_date, end_date,
                                          frequency)
        self.pre_data_dict = {}
        self.limit_symbol_list = []
        self.fall_symbol_list = []
        self.daily_limit_list = []

    def init(self):
        pass

    def on_day_bar(self, bar):
        code = bar['code']
        close = round(bar['close'], 2)
        high = round(bar['high'], 2)
        limit = round(bar['high_limit'], 2)
        low = round(bar['low'], 2)
        amount = bar['amount']
        volume = bar['volume']
        symbol_data = {}
        pre_close = round(bar['pre_close'],2)
        high_rate = 100 * (high - pre_close) / pre_close
        close_rate = 100 * (close - pre_close) / pre_close
        try:
            pre_data = self.pre_data_dict[code]
            pre_high_limit = round(pre_data['high_limit'], 2)
            pre_high = round(pre_data['high'], 2)
            pre_close_rate = 100 * (pre_data['close'] - pre_data['pre_close']) / pre_data['pre_close']

            if pre_close == pre_high_limit and pre_close_rate > 9:
                if high_rate < 3.1 and close_rate > -5:
                    if (amount > 1 * pow(10, 8)):
                            # 涨停未冲高
                            # if close < high * 0.99:
                            self.daily_limit_list.append(code)
                            symbol_data['_id'] = bar['date'] + '-' + code
                            symbol_data['date'] = bar['date']
                            symbol_data['code'] = code
                            symbol_data['type'] = 'enlarge_limit'
            self.pre_data_dict[code] = bar
        except:
            self.pre_data_dict[code] = bar

    def syn_backtest(self):
        for i in range(0, len(self.trading_date)):
            try:
                # 每日标的列表
                self.symbol_list = []
                date = self.trading_date[i]
                self.today_data = self.day_data[self.day_data['date'] == date]
                self.code_list = np.unique(self.today_data['code'])
                for bar in self.today_data:
                    if str(bar['code']).startswith('688'):
                        continue
                    self.on_day_bar(bar)
                logger.info(f"{date}")
                logger.info(f"每日首板:{self.daily_limit_list}")
                self.daily_limit_list = []
            except Exception as e:
                print(e)
                continue


if __name__ == '__main__':
    import datetime
    today = datetime.date.today()
    end_time = str(today)
    trade_days_until_today = get_trade_days(start_time='2014-01-01',
                                            end_time=end_time)
    start_time = trade_days_until_today[-8]
    test = LimitNoRush(start_date='2020-10-10',
                       end_date='2020-11-01',
                       frequency='daily')

    test.syn_backtest()
