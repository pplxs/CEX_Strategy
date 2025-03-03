import numpy as np
import pandas as pd
import pymysql
import configparser
from decimal import Decimal
import datetime

def getAllCoinMarketCap():
    # 从raw_data_cmc中查
    sql = f'''select SUM(IFNULL(fully_diluted_market_cap, 0))  from pv_allcoin_raw_data_daily_cmc_{year} where date_time_ymd="{current_date_time}" 
            and market_cap>0 and cmc_rank<=100 and id not in (6801,28167,28040,28043,25967,27929);'''
    cs = conn.cursor()
    cs.execute(sql)
    res = cs.fetchone()
    if res is None or res[0] is None:
        print('No Data: '+current_date_time)
        return None
    return res[0]

def getStablecoinMarketCap():
    # 获取当天所有的稳定币
    cs = conn.cursor()
    sql = f'''select SUM(IFNULL(fully_diluted_market_cap, 0)) from pv_allcoin_raw_data_daily_cmc_{year} where date_time_ymd="{current_date_time}" and JSON_CONTAINS(tags, '"stablecoin"')
            and market_cap>0 and cmc_rank<=100 and id not in (6801,28167,28040,28043,25967,27929);'''
    cs.execute(sql)
    res = cs.fetchone()
    if res is None or res[0] is None or res[0] == '':
        return None
    return res[0]

def getBtcPriceByCmcId(coin):
    sql = f'''select price from pv_allcoin_raw_data_daily_cmc_{year} where id={coin} and date_time_ymd="{current_date_time}";'''
    cs = conn.cursor()
    cs.execute(sql)
    res = cs.fetchone()
    if res is None or res[0] is None:
        print('No Data: ' + current_date_time)
        return None
    return res[0]


def getCoinMarketCapByCmcId(coin):
    # 从raw_data_cmc中查
    sql = f'''select fully_diluted_market_cap from pv_allcoin_raw_data_daily_cmc_{year} where id={coin} and date_time_ymd="{current_date_time}";'''
    cs = conn.cursor()
    cs.execute(sql)
    res = cs.fetchone()
    if res is None or res[0] is None:
        print('No Data: ' + current_date_time)
        return None
    return res[0]

def fill_data():
    global prev_data
    # 获取当天所有币的总市值
    allCoinMarketCap = toDecimal(getAllCoinMarketCap())
    # 获取当天稳定币的市值
    stablecoinMarketCap = toDecimal(getStablecoinMarketCap())
    # 获取当天BTC的市值
    btcCoinMarketCap = toDecimal(getCoinMarketCapByCmcId(1))
    # 获取当天ETH的市值
    ethCoinMarketCap = toDecimal(getCoinMarketCapByCmcId(1027))
    # 获取btc的价格
    btcPrice = toDecimal(getBtcPriceByCmcId(1))
    if btcPrice is None:
        print(current_date_time+"比特币价格数据有缺失")
    else:
        btcPrice = str(btcPrice)
    # 获取其它币种的市值
    if allCoinMarketCap is None or stablecoinMarketCap is None or btcCoinMarketCap is None or ethCoinMarketCap is None:
        # # 记录异常数据对应的时间和异常数据的第一个参数
        # missingData.append([current_date_time, prev_data, None])
        # prev_data = None
        # return
        altcoinMarketCap = None
        data = (current_date_time,
                btcCoinMarketCap, None,
                ethCoinMarketCap, None,
                stablecoinMarketCap, None,
                altcoinMarketCap, None,
                allCoinMarketCap, btcPrice)
    else:
        altcoinMarketCap = allCoinMarketCap - stablecoinMarketCap - btcCoinMarketCap - ethCoinMarketCap
        data = (current_date_time,
                str(btcCoinMarketCap), getPerc(btcCoinMarketCap, allCoinMarketCap),
                str(ethCoinMarketCap), getPerc(ethCoinMarketCap, allCoinMarketCap),
                str(stablecoinMarketCap), getPerc(stablecoinMarketCap, allCoinMarketCap),
                str(altcoinMarketCap), getPerc(altcoinMarketCap, allCoinMarketCap),
                str(allCoinMarketCap),btcPrice)
    # # 记录当天数据 / 记录数据作为异常数据的第二个参数
    # indexEnd = len(missingData) - 1
    # if indexEnd >= 0 and missingData[indexEnd][2] is None:
    #     missingData[indexEnd][2] = data
    # prev_data = data
    return pd.DataFrame(data)


def toDecimal(value):
    if value is None:
        return None
    else:
        return Decimal(value)


# 计算比例
def getPerc(item, allcoins):
    if item is None or allcoins is None:
        return None
    else:
        return str(item / allcoins * 100)


def getConn():
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf8')
    db_url = config['base_config']['host']
    db_port = config['base_config']['port']
    db_username = config['base_config']['username']
    db_password = config['base_config']['password']
    db_name = config['base_config']['basename']
    return pymysql.connect(host=db_url,
                           port=int(db_port),
                           user=db_username,
                           password=db_password,
                           db=db_name,
                           charset='utf8mb4')


if __name__ == '__main__':
    start_date = datetime.date(2020, 1, 1)
    end_date = datetime.date(2025, 1, 1)
    date_range = []
    delta = datetime.timedelta(days=1)  # 定义时间间隔为1天
    while start_date <= end_date:
        date_range.append(start_date)
        start_date += delta
    conn = getConn()
    prev_data = None
    # [[date,data1,data2],[date,data1,data2]]

    all_data = pd.DataFrame()
    missingData = []
    for date in date_range:
        current_date_time = date.strftime('%Y-%m-%d')
        year = current_date_time.split('-')[0]
        print('start:' + current_date_time)
        data = fill_data()
        if data is not None:
            all_data = pd.concat([all_data,data.T],axis=0)

    all_data.columns = ['date_time', 'btc_FDV', 'btc_FDV_percentage', 'eth_FDV',
                    'eth_FDV_percentage', 'stablecoin_FDV', 'stablecoin_FDV_percentage',
                    'altcoin_FDV', 'altcoin_FDV_percentage', 'total_FDV', 'btc_price']

    all_data.sort_values(by="date_time",inplace=True)
    all_data.to_csv("FDV_data_cmc.csv",index=False)


