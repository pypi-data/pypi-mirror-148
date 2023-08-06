# -*-coding:utf-8-*-
# 测试


import sys
import os
import numpy as np
import datetime
import matplotlib.pyplot as plt
from QuadQuanta.core.strategy import BaseStrategy
from QuadQuanta.utils.logs import logger
from QuadQuanta.data.mongodb_api import insert_mongodb
from QuadQuanta.data.get_data import get_trade_days, get_bars, get_securities_info
import talib

FILENAME = os.path.basename(sys.argv[0]).split(".py")[0]


class TestStrategy(BaseStrategy):
    def __init__(self,
                 code=None,
                 start_date=None,
                 end_date=None,
                 frequency='day', init_cash=100000):
        super(TestStrategy, self).__init__(code, start_date, end_date,
                                           frequency, init_cash=init_cash)
        self.pre_volume_dict = {}
        self.pre_data_dict = {}
        self.double_limit_list = ['']
        self.fall_symbol_list = []
        self.break_symbol_list = []
        self.history_N_data = []
        self.symbol_limit_date = {}
        self.total_assert = []

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

        if code in self.acc.positions.keys():
            volume_long = self.acc.get_position(
                code).volume_long
            if volume_long > 0:
                if self.acc.get_position(code).hold_days >= 1:
                    # price = round(max(self.max_close_dict[code][1:]) * 0.95, 2)
                    price = close
                    order = self.acc.send_order(code,
                                                volume_long,
                                                price,
                                                'sell',
                                                order_time=str(bar['date']))
                    logger.info(
                        f"sell date:{bar['date']} code:{code} price:{price} profit:{int(self.acc.get_position(code).float_profit)} ratio:{self.acc.get_position(code).profit_ratio}"
                    )
                    self.acc.make_deal(order)
        else:
            price = high
            order_volume = 100 * (self.acc.total_assets /
                                  (10 * price) // 100)

            order = self.acc.send_order(code,
                                        order_volume,
                                        price,
                                        'buy',
                                        order_time=str(bar['datetime']))
            self.acc.make_deal(order)
            logger.info(f"buy:{code}, date:{bar['date']}, price:{order['price']}, amount:{order['amount']}")

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

                self.acc.settle()
                logger.info(
                    f"date:{date} asserts: {self.acc.total_assets}, profit_ratio: {int(self.acc.profit_ratio)}"
                )

            except Exception as e:
                print(e)


if __name__ == '__main__':
    import datetime

    today = datetime.date.today()
    end_time = str(today)
    trade_days_until_today = get_trade_days(start_time='2014-01-01',
                                            end_time=end_time)
    start_time = trade_days_until_today[-10]

    test = TestStrategy(code=['002529'],start_date='2021-11-01',
                        end_date='2021-11-10',
                        frequency='daily', init_cash=10000000)

    test.syn_backtest()
