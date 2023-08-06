# -*-coding:utf-8-*-
# -*-coding:utf-8-*-
# 放量涨停后加速弱转强

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

FILENAME = os.path.basename(sys.argv[0]).split(".py")[0]


class AccLimit(BaseStrategy):
    def __init__(self,
                 code=None,
                 start_date=None,
                 end_date=None,
                 frequency='day'):
        super(AccLimit, self).__init__(code, start_date, end_date, frequency)
        self.pre_volume_dict = {}
        self.symbol_list = []

    def init(self):
        self.success_count = 0
        self.failed_count = 0

    def on_symbol_bar(self, bar):
        """
        标的买入处理
        Parameters
        ----------
        bar

        Returns
        -------

        """
        open_ = round(100 * (bar['open'] - bar['pre_close']) / bar['pre_close'],
                      2)
        high_ = round(100 * (bar['high'] - bar['pre_close']) / bar['pre_close'],
                      2)
        amount = bar['amount']
        code = bar['code']
        close = round(bar['close'], 2)
        high = round(bar['high'], 2)
        limit = round(bar['high_limit'], 2)
        # 涨停
        # if high_ > 1 and open_ < 3:
        if high == limit and high_ > 9:
            symbol_data = {}
            symbol_data['_id'] = bar['date'] + '-' + code
            symbol_data['date'] = bar['date']
            symbol_data['code'] = code
            symbol_data['type'] = 'acc_limit'

            insert_mongodb('QuadQuanta', 'acc_limit2', symbol_data)
            #  or str(code).startswith('30')
            if str(code).startswith('688'):
                pass
            else:
                price = round(bar['open'], 2) * 1.01
                order_volume = 100 * (self.acc.total_assets /
                                      (5 * price) // 100)

                order = self.acc.send_order(code,
                                            order_volume,
                                            price,
                                            'buy',
                                            order_time=str(bar['datetime']))
                logger.info(f"buy:{code}, price:{order['price']}, amount:{order['amount']}")
                self.acc.make_deal(order)
                self.acc.get_position(code).on_price_change(
                    round(bar['close'], 2))

    def on_day_bar(self, bar):
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

        try:
            pre_volume = self.pre_volume_dict[code]
            # 涨停股非st 成交量放大2.5倍,成交额大于3亿
            if (close == limit) and close_rate > 8 and bar['amount'] > 3 * pow(10, 0):
                self.symbol_list.append(code)
            self.pre_volume_dict[code] = bar['volume']
        except:
            self.pre_volume_dict[code] = bar['volume']

        if code in self.acc.positions.keys():

            volume_long_history = self.acc.get_position(
                code).volume_long_history
            if volume_long_history > 0:
                order = self.acc.send_order(code,
                                            volume_long_history,
                                            avg_price,
                                            'sell',
                                            order_time=str(bar['date']))
                # if open_ > 1.04 * pre_close:
                # if self.acc.get_position(code).profit_ratio < -5:
                if self.acc.get_position(code).profit_ratio > 0:
                    self.success_count += 1
                else:
                    self.failed_count += 1
                logger.info(
                    f"sell date:{bar['date']} code:{code} profit:{self.acc.get_position(code).float_profit} ratio:{self.acc.get_position(code).profit_ratio}"
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
                if len(self.symbol_list) > 0:
                    self.symbol_data = query_clickhouse(
                        self.symbol_list, str(self.trading_date[i]),
                        str(self.trading_date[i]), self.frequency)
                    for bar in self.symbol_data:
                        self.on_symbol_bar(bar)
                self.symbol_list = []  # 标的清空

                for bar in self.today_data:
                    if str(bar['code']).startswith('30') or str(bar['code']).startswith('688'):
                        continue
                    self.on_day_bar(bar)

            except Exception as e:
                logger.warning(e)
                continue
            self.acc.settle()
            self.total_assert.append(self.acc.total_assets)
            # print(time.perf_counter() - start_)
            logger.info(
                f"date:{date} asserts: {self.acc.total_assets}, profit_ratio: {self.acc.profit_ratio}"
            )
        print(f"success count:{self.success_count}, failed_cout:{self.failed_count}")
        # print(f"asserts: {self.acc.total_assets}, profit_ratio: {self.acc.profit_ratio}")

        plt.title(f"{FILENAME}:{self.start_date}-{self.end_date}")
        plt.plot(self.total_assert)

        plt.show()


if __name__ == '__main__':
    logger.info(f"filename:{FILENAME}.py")
    test = AccLimit(start_date='2021-06-01',
                    end_date='2021-07-01',
                    frequency='daily')

    test.syn_backtest()

if __name__ == '__main__':
    pass
