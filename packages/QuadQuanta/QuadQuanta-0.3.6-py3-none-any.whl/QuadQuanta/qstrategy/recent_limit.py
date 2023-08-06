# -*-coding:utf-8-*-
# 近期涨停异动
# 最近四个交易日触及涨停，但是未连板
# 最近四个交易日冲高回落,但是未涨停
import datetime
import csv
from QuadQuanta.data.get_data import get_trade_days
from QuadQuanta.data.mongodb_api import insert_mongodb, save_mongodb, query_mongodb


def recent_limit(date):
    limit_dict = query_mongodb('QuadQuanta', 'daily_limit', sql={
        'date': date})
    limit_symbols = [symbol_data['code'] for symbol_data in limit_dict]

    break_limit_dict = query_mongodb('QuadQuanta', 'daily_break', sql={
        'date': date})
    break_limit_symbols = [symbol_data['code'] for symbol_data in break_limit_dict]

    double_limit_dict = query_mongodb('QuadQuanta', 'daily_double_limit', sql={
        '_id': date})[0]
    double_limit_symbols = double_limit_dict['symbol_list']

    fall_limit_dict = query_mongodb('QuadQuanta', 'daily_fall', sql={
        'date': date})
    fall_limit_symbols = [symbol_data['code'] for symbol_data in fall_limit_dict]

    ever_limit_symbols = limit_symbols + break_limit_symbols
    return ever_limit_symbols, double_limit_symbols, fall_limit_symbols


if __name__ == '__main__':
    today = datetime.date.today()
    end_time = str(today)
    trade_days_until_today = get_trade_days(start_time='2014-01-01',
                                            end_time=end_time)

    trade_days = trade_days_until_today[-4:]
    last_day = trade_days[-1]
    ever_limit_symbols = []
    double_limit_symbols = []
    fall_limit_symbols = []
    limit_res = []
    fall_res = []
    symbol_data = {}
    print(trade_days)
    # N字涨停模式标
    daily_N_limit = query_mongodb('QuadQuanta', 'daily_N_limit', sql={
        '_id': last_day})[-1]['symbol_list']
    daily_TwoN_limit = query_mongodb('QuadQuanta', 'daily_TwoN_limit', sql={
        '_id': last_day})[-1]['symbol_list']
    daily_breakfall_limit = query_mongodb('QuadQuanta', 'daily_breakfall_limit', sql={
        '_id': last_day})[-1]['symbol_list']

    for day in trade_days:
        daily_limit_symbols, daily_double_limit_symbols, daily_fall_symbols = recent_limit(day)
        ever_limit_symbols += daily_limit_symbols
        double_limit_symbols += daily_double_limit_symbols
        fall_limit_symbols += daily_fall_symbols

    current_limit_symbols, _, _ = recent_limit(trade_days[-1])

    for symbol in set(ever_limit_symbols):
        if symbol not in set(
                double_limit_symbols + current_limit_symbols + daily_N_limit + daily_TwoN_limit + daily_breakfall_limit):
            limit_res.append(symbol)
    symbol_data['_id'] = trade_days[-1]
    symbol_data['symbols'] = limit_res
    symbol_data['type'] = 'recent_ever_limit'
    # insert_mongodb('QuadQuanta', 'daily_recent_ever_limit', symbol_data)
    print(f"近期涨停或炸板{limit_res}")
    csv_symbol = [[symbol] for symbol in limit_res]
    # 写入CSV文件
    # with open('./CSV/recentlimit.csv', 'w', newline='') as csvfile:
    #     spamwriter = csv.writer(csvfile, delimiter=' ',
    #                             quoting=csv.QUOTE_MINIMAL)
    #     #
    #     spamwriter.writerow(["证券代码"])
    #     for item in csv_symbol:
    #         spamwriter.writerow(item)

    for symbol in set(fall_limit_symbols):
        if symbol not in set(double_limit_symbols + current_limit_symbols + ever_limit_symbols):
            fall_res.append(symbol)
    symbol_data['_id'] = trade_days[-1]
    symbol_data['symbols'] = fall_res
    symbol_data['type'] = 'recent_fall'
    # insert_mongodb('QuadQuanta', 'daily_recent_fall_limit', symbol_data)
    print(f"冲高回落{fall_res}")
