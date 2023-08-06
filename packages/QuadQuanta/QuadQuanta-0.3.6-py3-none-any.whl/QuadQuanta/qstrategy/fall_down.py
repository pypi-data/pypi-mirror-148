# -*-coding:utf-8-*-
# 炸板后反包

# 次日拉红
import sys
import os
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
from tqdm import tqdm

from QuadQuanta.core.strategy import BaseStrategy
from QuadQuanta.data.clickhouse_api import query_clickhouse, query_N_clickhouse
from QuadQuanta.portfolio import Account
from QuadQuanta.utils.logs import logger

FILENAME = os.path.basename(sys.argv[0]).split(".py")[0]
class BreakLimit(BaseStrategy):
    def __init__(self,
                 code=None,
                 start_date=None,
                 end_date=None,
                 frequency='day'):
        super().__init__(code, start_date, end_date, frequency)
        self.pre_volume_dict = {}
        self.symbol_list = []

    def init(self):
        pass

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
        if open_ < 0.1 and open_ > -3 and high_ > 1:
            # 昨日冲高高点是三日内最高点
            # 平盘价 买入
            code = bar['code']
            # or str(code).startswith('3')
            if str(code).startswith('688'):
                pass
            else:
                history_N_data = query_N_clickhouse(count=4, code=code, end_time=self.pre_date)
                history_N_high = history_N_data['high']
                if history_N_high[-1] >= np.max(history_N_high[:-1]):
                    price = round(bar['pre_close'], 2)
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
        pre_close = bar['pre_close']
        high_rate = 100 * (high - pre_close) / pre_close

        # 涨停，放量大于2.5倍，成交额大于2亿，加入候选列表

        try:
            pre_volume = self.pre_volume_dict[code]
            # if high == limit and 100 * (
            #         limit - close) / close >= 3 and amount > 1 * pow(10, 8):
            # 冲高回落股
            if (high < limit) and amount > 2 * pow(10, 8):
                # if 100 * ((high - close) / close) >= 3:
                if high_rate > 9:
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
                                            close,
                                            'sell',
                                            order_time=str(bar['date']))
                logger.info(
                    f"sell date:{bar['date']} code:{code} profit:{self.acc.get_position(code).float_profit} ratio:{self.acc.get_position(code).profit_ratio}"
                )
                self.acc.make_deal(order)

    def syn_backtest(self):
        self.total_assert = []
        for i in (range(0, len(self.trading_date))):
            start_ = time.perf_counter()

            try:
                self.today = self.trading_date[i]
                self.next_date = self.trading_date[i + 1]
                self.pre_date = self.trading_date[i - 1]
                logger.info(f"date:{self.today}")
                self.today_data = self.day_data[self.day_data['date'] == self.today]
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
                f"date:{self.today} asserts: {self.acc.total_assets}, profit_ratio: {self.acc.profit_ratio}"
            )
        # print(f"asserts: {self.acc.total_assets}, profit_ratio: {self.acc.profit_ratio}")
        plt.title(f"{FILENAME}:{self.start_date}-{self.end_date}")
        plt.plot(self.total_assert)
        plt.show()

if __name__ == '__main__':
    logger.info(f"filename:{FILENAME}.py")
    test = BreakLimit(start_date='2021-01-01',
                      end_date='2022-01-01',
                      frequency='daily')

    test.syn_backtest()
