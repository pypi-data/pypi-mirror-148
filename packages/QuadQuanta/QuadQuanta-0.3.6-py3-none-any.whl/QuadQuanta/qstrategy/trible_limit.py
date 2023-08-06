#-*-coding:utf-8-*- 
#-*-coding:utf-8-*-
# 分析换手三板以上的介入点
# -*-coding:utf-8-*-

import numpy as np
import time
from QuadQuanta.core.strategy import BaseStrategy
from QuadQuanta.data.clickhouse_api import query_clickhouse
from QuadQuanta.portfolio import Account
from QuadQuanta.utils.logs import logger
from QuadQuanta.data.mongodb_api import insert_mongodb, save_mongodb
from QuadQuanta.data.get_data import get_trade_days, get_securities_info,get_bars
from pymongo.errors import DuplicateKeyError


class DailyTribleReplay(BaseStrategy):
    def __init__(self,
                 code=None,
                 start_date=None,
                 end_date=None,
                 frequency='day'):
        super(DailyTribleReplay, self).__init__(code, start_date, end_date,
                                                frequency)
        self.pre_volume_dict = {}
        self.limit_symbol_list = []
        self.fall_symbol_list = []
        self.break_symbol_list = []
        self.quad_symbol_list = []
        self.pre_data_dict = {}

    def init(self):
        self.all_securities_info = get_securities_info(format='pandas')


    def all_limit(self,datas):
        if len(datas) < 3:
            return False
        for data in datas:
            close = round(data['close'],2)
            high_limit = round(data['high_limit'],2)
            if close < high_limit:
                return False
        return True


    def on_day_bar(self, bar):
        code = bar['code']
        date = bar['date']

        close = round(bar['close'], 2)
        high = round(bar['high'], 2)
        limit = round(bar['high_limit'], 2)
        low = round(bar['low'], 2)
        amount = bar['amount']
        volume = bar['volume']
        symbol_data = {}
        current_day = bar['date']
        current_date = datetime.date.fromisoformat(current_day)
        pre_close = bar['pre_close']
        high_rate = 100 * (high - pre_close) / pre_close
        try:

            if close == limit and high_rate > 9:
                # if (amount > 1 * pow(10, 8)):
                history_3_data = get_bars(code, end_time=date, count=3)
                if self.all_limit(history_3_data):
                    # 非新股
                    # 上市日期
                    start_date = datetime.date.fromisoformat(self.all_securities_info.loc[code]['start_date'])
                    # start_date = get_securities_info(code=code)[-1]['start_date']

                    if current_date - start_date > datetime.timedelta(days=30):
                        # if close < high * 0.99:
                        self.quad_symbol_list.append(code)

        except DuplicateKeyError:
            pass
        except Exception as e:
            print("on_bar exception:", type(e))

    def syn_backtest(self):
        for i in range(0, len(self.trading_date)):
            try:
                date = self.trading_date[i]
                self.today_data = self.day_data[self.day_data['date'] == date]
                self.code_list = np.unique(self.today_data['code'])
                for bar in self.today_data:
                    if str(bar['code']).startswith('688'):
                        continue
                    self.on_day_bar(bar)
                logger.info(f"{date}")
                logger.info(f"三连板：{self.quad_symbol_list}")
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
    start_time = trade_days_until_today[-300]
    test = DailyTribleReplay(start_date=start_time,
                             end_date=end_time,
                             frequency='daily')
    # test = DailyDoubleReplay(start_date='2019-05-01',
    #                          end_date='2019-05-28',
    #                          frequency='daily')

    test.syn_backtest()
