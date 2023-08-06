# -*-coding:utf-8-*-
# 涨停20%个股封板率

# -*-coding:utf-8-*-


import sys
import os
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
from tqdm import tqdm

from QuadQuanta.core.strategy import BaseStrategy
from QuadQuanta.data.clickhouse_api import query_clickhouse
from QuadQuanta.portfolio import Account
from QuadQuanta.utils.logs import logger
from QuadQuanta.data.mongodb_api import insert_mongodb
from QuadQuanta.data.get_data import get_bars, get_trade_days

FILENAME = os.path.basename(sys.argv[0]).split(".py")[0]


class Limit20(BaseStrategy):
    def __init__(self,
                 code=None,
                 start_date=None,
                 end_date=None,
                 frequency='day',
                 init_cash=100000):
        super(Limit20, self).__init__(code, start_date, end_date, frequency, init_cash=init_cash)
        self.pre_volume_dict = {}
        self.max_close_dict = {}
        self.symbol_list = []
        self.pre_data_dict = {}

    def init(self):
        self.success_count = 0
        self.failed_count = 0

    def on_day_bar(self, bar):
        today = bar['date']
        code = bar['code']
        close = round(bar['close'], 2)
        high = round(bar['high'], 2)
        limit = round(bar['high_limit'], 2)
        low = round(bar['low'], 2)
        amount = bar['amount']
        avg_price = amount / bar['volume']
        pre_close = bar['pre_close']
        open_ = round(bar['open'], 2)
        high_rate = 100 * (high - pre_close) / pre_close
        close_rate = 100 * (close - pre_close) / pre_close

        # 涨停，放量大于2.5倍，成交额大于2亿，加入候选列表

        # # 触及涨停
        # if (high == limit) and high_rate > 9 and amount > pow(10, 8) and amount < 10 * pow(10, 8):
        #     history_N_data = get_bars(bar['code'], end_time=str(today), count=11)[:-1]
        #     last_day_data = history_N_data[-1]
        #     # 昨日未涨停
        #     if round(last_day_data['close'], 2) < round(last_day_data['high_limit']):
        #         max_N_high = np.max(history_N_data['high'])
        #         if high < max_N_high:
        try:
            pre_data = self.pre_data_dict[code]
            pre_high_limit = round(pre_data['high_limit'], 2)
            pre_high = round(pre_data['high'], 2)
            self.pre_data_dict[code] = bar
            if high == limit and high_rate > 15:
                if (amount > 1 * pow(10, 8)):
                    if pre_high < pre_high_limit * 0.99:
                        # symbol_data = {}
                        # symbol_data['_id'] = bar['date'] + '-' + code
                        # symbol_data['date'] = bar['date']
                        # symbol_data['code'] = code
                        # symbol_data['type'] = 'first_limit'
                        #
                        # insert_mongodb('QuadQuanta', 'first_limit', symbol_data)

                        # price = round(bar['high'] * 0.98, 2)
                        price = high
                        order_volume = 100 * (self.acc.total_assets /
                                              (1000 * price) // 100)

                        order = self.acc.send_order(code,
                                                    order_volume,
                                                    price,
                                                    'buy',
                                                    order_time=str(bar['datetime']))
                        logger.info(f"buy:{code}, price:{order['price']}, amount:{order['amount']}")
                        self.acc.make_deal(order)
                        self.acc.get_position(code).on_price_change(
                            round(bar['close'], 2))
        except:
            self.pre_data_dict[code] = bar
        if code in self.acc.positions.keys():
            volume_long = self.acc.get_position(
                code).volume_long
            if volume_long > 0:
                # 保存最大值
                try:
                    self.max_close_dict[code].append(close)
                except:
                    self.max_close_dict[code] = []
                if self.acc.get_position(code).hold_days == 1:

                    # price = round(max(self.max_close_dict[code][1:]) * 0.95, 2)
                    price = close
                    order = self.acc.send_order(code,
                                                volume_long,
                                                price,
                                                'sell',
                                                order_time=str(bar['date']))
                    if self.acc.get_position(code).profit_ratio > 0:
                        self.success_count += 1
                    else:
                        self.failed_count += 1
                    logger.info(
                        f"sell date:{bar['date']} code:{code} price:{price} profit:{int(self.acc.get_position(code).float_profit)} ratio:{self.acc.get_position(code).profit_ratio}"
                    )
                    self.acc.make_deal(order)

    def syn_backtest(self):
        self.total_assert = []
        for i in (range(0, len(self.trading_date))):
            start_ = time.perf_counter()

            try:
                date = self.trading_date[i]
                logger.info(f"date:{date}")
                self.today_data = self.day_data[self.day_data['date'] == date]
                for bar in self.today_data:
                    if str(bar['code']).startswith('00') or str(bar['code']).startswith('60') or str(
                            bar['code']).startswith('688'):
                        continue
                    self.on_day_bar(bar)

            except Exception as e:
                logger.warning(e)
                continue
            self.acc.settle()
            self.total_assert.append(self.acc.total_assets)
            # print(time.perf_counter() - start_)
            logger.info(
                f"date:{date} asserts: {self.acc.total_assets}, profit_ratio: {int(self.acc.profit_ratio)}"
            )
        logger.info(f"success count:{self.success_count}, failed_cout:{self.failed_count}")
        # print(f"asserts: {self.acc.total_assets}, profit_ratio: {self.acc.profit_ratio}")

        plt.title(f"{FILENAME}:{self.start_date}-{self.end_date}")
        plt.plot(self.total_assert)

        plt.show()


if __name__ == '__main__':
    logger.info(f"filename:{FILENAME}.py")
    test = Limit20(start_date='2020-10-01',
                   end_date='2021-02-10',
                   frequency='daily', init_cash=100000000)

    test.syn_backtest()
