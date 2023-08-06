# -*-coding:utf-8-*-
# 二板涨停后 检测股性是否激活，后期涨停的成功率


import numpy as np
import datetime
from QuadQuanta.core.strategy import BaseStrategy
from QuadQuanta.utils.logs import logger
from QuadQuanta.data.mongodb_api import insert_mongodb
from QuadQuanta.data.get_data import get_trade_days, get_bars, get_securities_info
import talib


class DoubleLimitNext(BaseStrategy):
    def __init__(self,
                 code=None,
                 start_date=None,
                 end_date=None,
                 frequency='day', init_cash=100000):
        super(DoubleLimitNext, self).__init__(code, start_date, end_date,
                                              frequency, init_cash=init_cash)
        self.pre_volume_dict = {}
        self.pre_data_dict = {}
        self.double_limit_list = ['']
        self.fall_symbol_list = []
        self.break_symbol_list = []
        self.history_N_data = []
        self.symbol_limit_date = {}

    def init(self):
        self.success_count = 0
        self.failed_count = 0

    def on_day_bar(self, bar):
        code = bar['code']
        close = round(bar['close'], 2)
        high = round(bar['high'], 2)
        limit = round(bar['high_limit'], 2)
        low = round(bar['low'], 2)
        amount = bar['amount']
        volume = bar['volume']
        current_day = bar['date']
        current_date = datetime.date.fromisoformat(current_day)
        symbol_data = {}
        pre_close = round(bar['pre_close'], 2)
        high_rate = 100 * (high - pre_close) / pre_close

        if code in self.double_limit_list:
            pre_data = self.pre_data_dict[code]
            # 昨日收盘在60日线上
            current_history_N_data = self.history_N_data[self.history_N_data['code'] == code]
            MA60 = talib.SMA(current_history_N_data['pre_close'], 60)[-1]
            if pre_close < MA60 or len(code) < 6:
                self.double_limit_list.remove(code)
            pre_high = round(pre_data['high'], 2)
            pre_high_limit = round(pre_data['high_limit'], 2)
            datedelta = current_date - self.symbol_limit_date[code]
            # 二板后间隔10日
            if datedelta > datetime.timedelta(days=10):
                # 昨日未涨停
                if high == limit and pre_high < 0.99 * pre_high_limit:
                    if close == limit:
                        logger.info(f"success: date:{current_day}, code:{code}")
                        self.success_count += 1
                    else:
                        logger.info(f"failed: date:{current_day}, code:{code}")
                        self.failed_count += 1

        try:
            pre_data = self.pre_data_dict[code]
            pre_high_limit = round(pre_data['high_limit'], 2)
            pre_close = round(pre_data['close'], 2)
            pre_close_rate = 100 * (pre_data['close'] - pre_data['pre_close']) / pre_data['pre_close']

            if close == limit and high_rate > 9:
                if (amount > 1 * pow(10, 8)):
                    if pre_close == pre_high_limit:
                        # 非新股
                        # 上市日期
                        start_date = datetime.date.fromisoformat(get_securities_info(code)[-1]['start_date'])
                        # start_date = get_securities_info(code=code)[-1]['start_date']

                        self.symbol_limit_date[code] = current_date
                        if current_date - start_date > datetime.timedelta(days=60):
                            # if close < high * 0.99:
                            self.double_limit_list.append(code)
                            self.symbol_limit_date[code] = current_date

            self.pre_data_dict[code] = bar
        except Exception as e:
            self.pre_data_dict[code] = bar

    def syn_backtest(self):
        for i in range(0, len(self.trading_date)):
            try:
                # 每日标的列表

                self.symbol_list = []
                date = self.trading_date[i]
                logger.info(f"{date}")
                self.today_data = self.day_data[self.day_data['date'] == date]
                self.history_N_data = get_bars(self.double_limit_list, end_time=date, count=60)
                self.code_list = np.unique(self.today_data['code'])
                for bar in self.today_data:
                    if str(bar['code']).startswith('688'):
                        continue
                    self.on_day_bar(bar)

                # logger.info(f"连板:{self.double_limit_list}")
                logger.info(
                    f"date:{date} asserts: {self.acc.total_assets}, profit_ratio: {int(self.acc.profit_ratio)}"
                )

                # try:
                #     insert_mongodb('QuadQuanta', 'daily_first_limit',
                #                    {'_id': date, 'symbol_list': self.double_limit_list})
                # except:
                #     pass
            except Exception as e:
                print(e)
        logger.info(f"success count:{self.success_count}, failed_cout:{self.failed_count}")
        #


if __name__ == '__main__':
    import datetime

    today = datetime.date.today()
    end_time = str(today)
    trade_days_until_today = get_trade_days(start_time='2014-01-01',
                                            end_time=end_time)
    start_time = trade_days_until_today[-10]

    test = DoubleLimitNext(start_date='2019-05-01',
                           end_date='2019-10-01',
                           frequency='daily', init_cash=10000000)

    test.syn_backtest()
