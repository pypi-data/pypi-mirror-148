# -*-coding:utf-8-*-

import numpy as np
import time
import matplotlib.pyplot as plt
from QuadQuanta.core import BaseStrategy
from QuadQuanta.data.clickhouse_api import query_clickhouse
from QuadQuanta.portfolio import Account


class BreakReverse(BaseStrategy):
    def __init__(self,
                 code=None,
                 start_date=None,
                 end_date=None,
                 frequency='day'):
        super(BreakReverse, self).__init__(code, start_date, end_date,
                                           frequency)
        self.symbol_list = []
        self.pre_volume_dict = {}

    def init(self):
        self.account = Account()

    def on_day_bar(self, bar):
        code = bar['code']
        price = round(bar['close'], 2)
        close = round(bar['close'], 2)
        high = round(bar['high'], 2)
        limit = round(bar['high_limit'], 2)
        low = round(bar['low'], 2)
        amount = bar['amount']
        if code in self.acc.positions.keys():
            volume_long_history = self.acc.get_position(
                code).volume_long_history
            if volume_long_history > 0:
                order = self.acc.send_order(code,
                                            volume_long_history,
                                            price,
                                            'sell',
                                            order_time=str(bar['date']))
                # print(
                #     f"date:{bar['date']} code:{code} profit:{self.acc.get_position(code).float_profit} ratio:{self.acc.get_position(code).profit_ratio}"
                # )
                self.acc.make_deal(order)
        try:
            pre_volume = self.pre_volume_dict[code]
            if ((close == limit) and (bar['volume'] > 2.1 * pre_volume)) or (
                (high == limit) and (100 * (limit - close) / close > 2)):
                if amount > 2 * pow(10, 8):
                    self.symbol_list.append(bar['code'])
            self.pre_volume_dict[code] = bar['volume']
        except:
            self.pre_volume_dict[code] = bar['volume']

    def on_min_bar(self, bars):
        if bars[0]['open'] <= bars[0]['pre_close'] and bars[2]['close'] > bars[
                0]['pre_close']:
            code = bars[0]['code']
            price = round(bars[2]['close'], 2)
            order_volume = 100 * (self.acc.total_assets / (3 * price) // 100)
            order = self.acc.send_order(code,
                                        order_volume,
                                        price,
                                        'buy',
                                        order_time=str(bars[1]['datetime']))
            self.acc.make_deal(order)
            self.acc.get_position(code).on_price_change(
                round(bars[-1]['close'], 2))
            # print(f"{bars[0]['date']}-{self.acc.positions.keys()}")
            # print(self.acc.positions)

    def syn_backtest(self):
        self.total_assert = []
        for i in range(0, len(self.trading_date) - 1):
            try:
                # 每日标的列表
                if len(self.symbol_list) > 0:
                    self.min_data = query_clickhouse(self.symbol_list,
                                                     str(self.trading_date[i]),
                                                     str(self.trading_date[i]),
                                                     self.frequency)
                    self.symbol_list = np.unique(self.min_data['code'])
                    for j in range(len(self.symbol_list)):
                        self.symbol_min_data = self.min_data[
                            self.min_data['code'] == self.symbol_list[j]]
                        self.on_min_bar(self.symbol_min_data)
                self.symbol_list = []
                date = self.trading_date[i]
                self.today_data = self.day_data[self.day_data['date'] == date]
                self.code_list = np.unique(self.today_data['code'])
                for bar in self.today_data:
                    self.on_day_bar(bar)
                # print(f"{date}-{self.symbol_list}")

            except Exception as e:
                print(e)
                continue
            self.acc.settle()
            self.total_assert.append(self.acc.total_assets)
        #     print(f"asserts: {self.acc.total_assets}, profig_ratio: {self.acc.profit_ratio}")
        # print(f"asserts: {self.acc.total_assets}, profig_ratio: {self.acc.profit_ratio}")
        plt.plot(self.total_assert)
        plt.show()


if __name__ == '__main__':
    test = BreakReverse(start_date='2014-01-01',
                        end_date='2015-01-10',
                        frequency='min')

    test.syn_backtest()
