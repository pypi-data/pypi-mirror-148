# -*-coding:utf-8-*-
# 活跃涨停股，再次涨停买点


import sys
import os
import numpy as np
import datetime
import matplotlib.pyplot as plt
from QuadQuanta.core.strategy import BaseStrategy
from QuadQuanta.utils.logs import logger
from QuadQuanta.data.mongodb_api import query_mongodb
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
        # 10天内二板
        self.hold_day = 10
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
        self.all_securities_info = get_securities_info(format='pandas')

    def on_day_bar(self, bars):
        bar = bars[-1]
        pre_bar = bars[-2]

        code = bar['code']
        max_high = np.max(bars[:-1]['high'])
        close = round(bar['close'], 2)
        high = round(bar['high'], 2)
        open_ = round(bar['open'], 2)
        avg = round(bar['avg'], 2)
        low = round(bar['low'], 2)

        limit = round(bar['high_limit'], 2)
        pre_limit = round(pre_bar['high_limit'], 2)
        pre_close = round(bar['pre_close'], 2)
        high_limit_rate = 100 * (limit - pre_close) / pre_close
        low_rate = 100 * (low - pre_close) / pre_close
        current_day = bar['date']
        current_date = datetime.date.fromisoformat(current_day)
        MA5 = talib.SMA(bars['close'], 5)[-1]
        MA10 = talib.SMA(bars['close'], 10)[-1]
        # 上市日期
        start_date = datetime.date.fromisoformat(self.all_securities_info.loc[code]['start_date'])
        low_MA5_rate = round(100 * (low - MA5) / MA5, 2)


        if code in self.acc.positions.keys():
            volume_long = self.acc.get_position(
                code).volume_long
            if volume_long > 0:
                if self.acc.get_position(code).hold_days >= 1:

                    # price = round(max(self.max_close_dict[code][1:]) * 0.95, 2)
                    price = close
                    # if open_ < MA5:
                    #     price = open_
                    order = self.acc.send_order(code,
                                                volume_long,
                                                price,
                                                'sell',
                                                order_time=str(bar['date']))
                    if self.acc.get_position(code).profit_ratio > 0:
                        self.success_count += 1
                    else:
                        self.failed_count += 1

                    self.acc.make_deal(order)
                    logger.info(
                        f"sell date:{bar['date']} code:{code} price:{price} volume:{volume_long} profit:{int(self.acc.get_position(code).float_profit)} ratio:{self.acc.get_position(code).profit_ratio}"
                    )


        if high == limit:
                self.nice_symbol.append(code)
                price = high
                order_volume = 100 * (self.acc.total_assets /
                                      (10 * price) // 400)

                order = self.acc.send_order(code,
                                            order_volume,
                                            price,
                                            'buy',
                                            order_time=str(bar['datetime']))
                self.acc.make_deal(order)
                logger.info(
                    f"buy:{code}, date:{bar['date']}, price:{order['price']},volume:{order_volume} amount:{order['amount']}")


    def syn_backtest(self):

            for i in range(0, len(self.trading_date)):
                try:
                    # 每日标的列表

                    date = self.trading_date[i]
                    self.last_active_limit_dict = query_mongodb('QuadQuanta', 'daily_active_limit', sql={
                        '_id': {'$lt': date}
                    })[-1]
                    logger.info(f"{date}")
                    self.last_active_limit = self.last_active_limit_dict['symbol_list']
                    self.symbol_list = self.last_active_limit + self.positon_list
                    self.symbol_list = list(set(self.symbol_list))

                    self.history_N_data = get_bars(self.symbol_list, end_time=date, count=self.hold_day)
                    for symbol in self.symbol_list:
                        bars = self.history_N_data[self.history_N_data['code'] == symbol]
                        if str(bars[0]['code']).startswith('688'):
                            continue
                        self.on_day_bar(bars)
                    # self.symbol_list += self.nice_symbol
                    self.positon_list = self.nice_symbol
                    # logger.info(self.nice_symbol)
                    self.nice_symbol = []
                    self.total_assert.append(self.acc.total_assets)
                    self.acc.settle()
                    logger.info(
                        f"date:{date} asserts: {self.acc.total_assets}, profit_ratio: {int(self.acc.profit_ratio)}"
                    )
                except Exception as e:
                    print(e)
            logger.info(f"success count:{self.success_count}, failed_cout:{self.failed_count}")
            #
            plt.title(f"{FILENAME}:{self.start_date}-{self.end_date}")
            plt.plot(self.total_assert)

            plt.show()


if __name__ == '__main__':
    import datetime

    today = datetime.date.today()
    end_time = str(today)
    trade_days_until_today = get_trade_days(start_time='2014-01-01',
                                            end_time=end_time)
    start_time = trade_days_until_today[-10]

    test = ActiveLimit(start_date='2021-01-01',
                       end_date='2021-05-31',
                       frequency='daily', init_cash=10000000)

    test.syn_backtest()
