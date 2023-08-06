# -*-coding:utf-8-*-
# 打回封板策略

import sys
import os
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
from tqdm import tqdm

from QuadQuanta.core.strategy import BaseStrategy
from QuadQuanta.data.clickhouse_api import query_clickhouse, query_limit_count, query_N_clickhouse
from QuadQuanta.portfolio import Account
from QuadQuanta.utils.logs import logger

FILENAME = os.path.basename(sys.argv[0]).split(".py")[0]


class EnlargeLimit(BaseStrategy):
    def __init__(self,
                 code=None,
                 start_date=None,
                 end_date=None,
                 frequency='day',
                 **kwargs):
        super().__init__(code, start_date, end_date, frequency,**kwargs)
        self.pre_volume_dict = {}
        self.symbol_list = []

    def init(self):
        pass

    def on_day_bar(self, bar):
        code = bar['code']
        date = bar['date']
        close = round(bar['close'], 2)
        high = round(bar['high'], 2)
        limit = round(bar['high_limit'], 2)
        low = round(bar['low'], 2)
        amount = bar['amount']
        volume = bar['volume']
        pre_close = round(bar['pre_close'], 2)
        avg_price = round(amount / volume, 2)
        high_rate = 100 * (high - pre_close) / pre_close
        if code in self.acc.positions.keys():
            volume_long_history = self.acc.get_position(
                code).volume_long_history
            if volume_long_history > 0:
                order = self.acc.send_order(code,
                                            volume_long_history,
                                            close,
                                            'sell',
                                            order_time=str(bar['date']))
                logger.info(
                    f"sell date:{bar['date']} code:{code} profit:{self.acc.get_position(code).float_profit} ratio:{self.acc.get_position(code).profit_ratio}"
                )
                self.acc.make_deal(order)

        # 触及涨停，成交量大于5亿
        if high == limit and amount > 5 * pow(10, 8):
            limit_count = query_limit_count(code, date, date)['limit'][0]

            # 回封买入
            if limit_count > 4:
                # 上一日涨幅小于8
                history_N_data = query_N_clickhouse(2, code, date)
                # 近期首板,低位炸板反包板
                pre_bar = history_N_data[-2]
                pre_high = round(pre_bar['high'], 2)
                pre_high_limit = round(pre_bar['high_limit'], 2)
                # pre_close = round(pre_bar['close'],2)
                # pre_high_rate = 100 * (pre_bar['high'] - pre_bar['pre_close']) / pre_bar['pre_close']
                if pre_high == pre_high_limit and pre_close < pre_high_limit:
                    order_volume = 100 * (self.acc.total_assets /
                                          (5 * high) // 100)

                    order = self.acc.send_order(code,
                                                order_volume,
                                                high,
                                                'buy',
                                                order_time=str(bar['datetime']))
                    logger.info(f"buy:{code}, price:{order['price']}, amount:{order['amount']}")
                    self.acc.make_deal(order)
                    self.acc.get_position(code).on_price_change(
                        round(bar['close'], 2))

    def syn_backtest(self):
        self.total_assert = []
        for i in (range(0, len(self.trading_date))):
            start_ = time.perf_counter()

            try:
                date = self.trading_date[i]
                logger.info(f"date:{date}")
                self.today_data = self.day_data[self.day_data['date'] == date]
                # if len(self.symbol_list) > 0:
                #     self.symbol_data = query_clickhouse(
                #         self.symbol_list, str(self.trading_date[i]),
                #         str(self.trading_date[i]), self.frequency)

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
        # print(f"asserts: {self.acc.total_assets}, profit_ratio: {self.acc.profit_ratio}")
        plt.plot(self.total_assert)
        plt.show()


if __name__ == '__main__':
    logger.info(f"filename:{FILENAME}.py, 炸板反包")
    test = EnlargeLimit(start_date='2019-01-01',
                        end_date='2020-01-01',
                        frequency='daily',solid=True)

    test.syn_backtest()
