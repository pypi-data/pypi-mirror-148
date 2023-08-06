# -*-coding:utf-8-*-
# 保存涨停开板次数

import sys
import os
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
from tqdm import tqdm
from clickhouse_driver import Client
from QuadQuanta.config import config
from QuadQuanta.core.strategy import BaseStrategy
from QuadQuanta.data.clickhouse_api import query_clickhouse, query_exist_date
from QuadQuanta.utils.logs import logger
import time

import numpy as np
from QuadQuanta.data.data_trans import tuplelist_to_np
from QuadQuanta.utils.common import removeDuplicates, is_sorted
from QuadQuanta.utils.datetime_func import is_valid_date
FILENAME = os.path.basename(sys.argv[0]).split(".py")[0]


class LimitCount(BaseStrategy):
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

    def syn_backtest(self):
        # 表不存在则创建相应表
        client = Client(host=config.clickhouse_IP, database='jqdata_test')
        create_table_sql = 'CREATE TABLE IF NOT EXISTS stock_day_limit (datetime DateTime,code String, date String ,limit UInt8) \
         ENGINE = MergeTree() ORDER BY (datetime, code)'
        client.execute(create_table_sql)
        for i in tqdm(range(0, len(self.trading_date))):
            date = self.trading_date[i]
            exist_date_range = query_exist_date(start_time=self.start_date, end_time=self.end_date, frequency='limit',client=client)
            if date not in exist_date_range:
                try:
                    self.today_data = self.day_data[self.day_data['date'] == date]
                    limit_count_list = []
                    for bar in self.today_data:
                        code = bar['code']
                        high = round(bar['high'], 2)
                        high_limit = round(bar['high_limit'], 2)
                        if high < high_limit:
                            limit_count = 0
                            limit_count_list.append(limit_count)
                        else:
                            min_bars = query_clickhouse(code,
                                                        date,
                                                        date,
                                                        frequency='minute',
                                                        database='jqdata_test')
                            close_bars = min_bars['close']
                            for i in range(len(close_bars) - 1):
                                # 一字开
                                if i == 0 and round(close_bars[i], 2) == high_limit:
                                    limit_count += 1

                                if round(close_bars[i], 2) < high_limit and round(
                                        close_bars[i + 1], 2) == high_limit:
                                    limit_count += 1
                                if round(close_bars[i], 2) == high_limit and round(
                                        close_bars[i + 1], 2) < high_limit:
                                    limit_count += 1
                            limit_count_list.append(limit_count)

                except Exception as e:
                    logger.warning(e)
                    continue
                raw_datetime = self.today_data['datetime'].tolist()
                raw_code = self.today_data['code'].tolist()
                raw_date = self.today_data['date'].tolist()
                if len(limit_count_list) == len(raw_datetime):
                    ready_data = list(
                        zip(raw_datetime, raw_code, raw_date, limit_count_list))
                else:
                    raise ValueError
                save_day_limit_to_clickdb(ready_data, client)


def save_day_limit_to_clickdb(data, client):
    sql = 'INSERT INTO  stock_day_limit (datetime, code, date, limit) VALUES'
    # sql = 'INSERT INTO int_test (x) VALUES'
    client.execute(sql, data, types_check=True)







def query_limit_count(code: list = None,
                     start_time: str = '1970-01-01',
                     end_time: str = '2200-01-01',
                     table_name='stock_day_limit',
                     database='jqdata_test') -> np.ndarray:
    if is_valid_date(start_time) and is_valid_date(end_time):
        try:
            time.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            start_time = start_time + ' 09:00:00'
            end_time = end_time + ' 17:00:00'
    #  判断日期合法
    if start_time > end_time:
        raise ValueError('开始时间大于结束时间')

    client = Client(host=config.clickhouse_IP, database=database)

    if code:
        if isinstance(code, str):
            # TODO 是否是有效的股票代码
            code = list(map(str.strip, code.split(',')))
        # 注意WHERE前的空格
        sql = "SELECT x.* FROM %s x" % table_name + " WHERE `datetime` >= %(start_time)s \
                        AND `datetime` <= %(end_time)s AND `code` IN %(code)s ORDER BY (`datetime`, `code`)"

        # 查询,返回数据类型为元组数组
        res_tuple_list = client.execute(sql, {
            'start_time': start_time,
            'end_time': end_time,
            'code': code
        })
    else:
        sql = "SELECT x.* FROM %s x" % table_name + " WHERE `datetime` >= %(start_time)s \
                                AND `datetime` <= %(end_time)s ORDER BY (`datetime`, `code`)"

        res_tuple_list = client.execute(sql, {
            'start_time': start_time,
            'end_time': end_time
        })
    #  TODO clickhouse分片

    # 默认有序条件下删除res_tuple_list重复数据
    if is_sorted(res_tuple_list):
        res_tuple_list = removeDuplicates(res_tuple_list)
    else:
        raise Exception('clickhouse返回列表非有序')
    # 元组数组通过numpy结构化,注意数据长度code:8字符 date:10字符.可能存在问题

    return np.array(res_tuple_list,
                        dtype=[('datetime', 'object'), ('code', 'U8'), ('date', 'U10'),
                               ('limit', 'u8')])


if __name__ == '__main__':
    # logger.info(f"filename:{FILENAME}.py")
    test = LimitCount(start_date='2020-01-01',
                      end_date='2020-05-15',
                      frequency='daily')

    test.syn_backtest()
    # query_limit_count(start_time='2021-04-01', end_time='2021-04-21')
