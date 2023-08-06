# -*-coding:utf-8-*-
# 昨日冲高回落次日高开涨停


import numpy as np
import time
from QuadQuanta.core.strategy import BaseStrategy
from QuadQuanta.data.clickhouse_api import query_clickhouse
from QuadQuanta.portfolio import Account
from QuadQuanta.utils.logs import logger
from QuadQuanta.data.mongodb_api import insert_mongodb, query_mongodb
from QuadQuanta.data.get_data import get_trade_days


class FallBreak(BaseStrategy):
    def __init__(self,
                 code=None,
                 start_date=None,
                 end_date=None,
                 frequency='day'):
        super(FallBreak, self).__init__(code, start_date, end_date,
                                        frequency)
        self.pre_volume_dict = {}
        self.limit_symbol_list = []
        self.fall_break_list = []
        self.pre_fall_symbol = []

    def init(self):
        self.break_count = 0
        self.break_success = 0
        self.break_high = 0

    def on_day_bar(self, bar):
        code = bar['code']
        close = round(bar['close'], 2)
        _open = round(bar['open'], 2)
        high = round(bar['high'], 2)
        limit = round(bar['high_limit'], 2)
        low = round(bar['low'], 2)
        amount = bar['amount']
        volume = bar['volume']
        symbol_data = {}
        pre_close = bar['pre_close']
        high_rate = 100 * (high - pre_close) / pre_close
        open_rate = 100 * (_open - pre_close) / pre_close
        if open_rate < 5 :

            self.break_count += 1
            if high == limit:
                self.fall_break_list.append(code)
                self.break_high += 1
            if close == limit:
                self.break_success += 1





    def syn_backtest(self):
        for i in range(1, len(self.trading_date)):
            try:
                # 每日标的列表
                self.symbol_list = []
                date = self.trading_date[i]
                pre_date = self.trading_date[i-1]
                self.pre_fall_data = query_mongodb('QuadQuanta', 'daily_fall', sql={
                'date': pre_date
            })
                self.pre_fall_symbol = [data['code'] for data in self.pre_fall_data ]
                self.today_data = self.day_data[self.day_data['date'] == date]
                self.code_list = np.unique(self.today_data['code'])
                for bar in self.today_data:
                    if str(bar['code']).startswith('688') or bar['code'] not in self.pre_fall_symbol or str(bar['code']).startswith('30'):
                        continue

                    self.on_day_bar(bar)
                logger.info(f"{date}")
                logger.info(f"冲高回落:{self.fall_break_list}")
                self.fall_break_list = []

            except Exception as e:
                print(e)
                continue
        # logger.info(f"高开次数:{self.break_count}")
        logger.info(f"高开封板成功率:{self.break_success/self.break_high}")
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
    start_time = trade_days_until_today[-300]
    test = FallBreak(start_date=start_time,
                     end_date=end_time,
                     frequency='daily')

    test.syn_backtest()
