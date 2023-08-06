# -*-coding:utf-8-*-
# 首次炸板日买入，看次日能否解套

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

FILENAME = os.path.basename(sys.argv[0]).split(".py")[0]


class BreakLimit(BaseStrategy):
    def __init__(self,
                 code=None,
                 start_date=None,
                 end_date=None,
                 frequency='day'):
        super(BreakLimit, self).__init__(code, start_date, end_date, frequency)
        self.pre_volume_dict = {}
        self.symbol_list = []
        self.pre_data_dict = {}
        self.break_symbol_list=[]

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
        symbol_data = {}
        pre_close = round(bar['pre_close'], 2)
        high_rate = 100 * (high - pre_close) / pre_close
        try:
            pre_data = self.pre_data_dict[code]
            pre_high_limit = round(pre_data['high_limit'], 2)
            pre_high = round(pre_data['high'], 2)
            pre_close_rate = 100 * (pre_data['close'] - pre_data['pre_close']) / pre_data['pre_close']
            if high == limit and high_rate > 9:
                if (amount > 1 * pow(10, 8)):
                    if pre_high < pre_high_limit * 0.99:
                        # 首次炸板
                        if close < high * 0.99:
                            self.break_symbol_list.append(code)
                            symbol_data['_id'] = bar['date'] + '-' + code
                            symbol_data['date'] = bar['date']
                            symbol_data['code'] = code
                            symbol_data['type'] = 'enlarge_limit'
                            price = high * 0.98
                            order_volume = 100 * (self.acc.total_assets /
                                                  (10 * price) // 100)

                            order = self.acc.send_order(code,
                                                        order_volume,
                                                        price,
                                                        'buy',
                                                        order_time=str(bar['datetime']))
                            logger.info(f"buy:{code}, price:{order['price']}, amount:{order['amount']}")
                            self.acc.make_deal(order)
                            self.acc.get_position(code).on_price_change(
                                round(bar['close'], 2))

            self.pre_data_dict[code] = bar
        except:
            self.pre_data_dict[code] = bar


        if code in self.acc.positions.keys():
            volume_long_history = self.acc.get_position(
                code).volume_long_history
            if volume_long_history > 0:
                order = self.acc.send_order(code,
                                            volume_long_history,
                                            close,
                                            'sell',
                                            order_time=str(bar['date']))

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

        plt.title(f"{FILENAME}:{self.start_date}-{self.end_date}")
        plt.plot(self.total_assert)

        plt.show()


if __name__ == '__main__':
    logger.info(f"filename:{FILENAME}.py")
    test = BreakLimit(start_date='2020-01-01',
                      end_date='2021-01-01',
                      frequency='daily')

    test.syn_backtest()
