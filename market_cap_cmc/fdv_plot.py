
from get_marketcap import getConn, toDecimal
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import matplotlib.ticker as ticker

def getFDV(conn)->pd.DataFrame():
    sql = "select * from pv_market_cap_data_cmc;"
    cs = conn.cursor()
    cs.execute(sql)
    res = pd.DataFrame(cs.fetchall())
    res.columns = ['date_time', 'btc_FDV', 'btc_FDV_percentage', 'eth_FDV', 'eth_FDV_percentage','stablecoin_FDV','stablecoin_FDV_percentage','altcoin_FDV','altcoin_FDV_percentage','total_FDV','btc_price']
    res.drop_duplicates(inplace=True,subset="date_time")
    res.dropna(inplace=True)
    res.sort_values(by="date_time",inplace=True)
    res.reset_index(inplace=True,drop=True)
    return res

def plotFDV(data):
    fig, ax1 = plt.subplots(figsize=(14, 7))
    FDVs = [
        data["altcoin_FDV"],
        data["stablecoin_FDV"],
        data["eth_FDV"],
        data["btc_FDV"],
    ]
    labels = ['Altcoin FDV', 'Stable FDV', 'Eth FDV', 'Btc FDV',]
    colors = ['#1f77b4', '#aec7e8', '#ffbb78', '#ff7f0e']
    stacks = ax1.stackplot(data["date_time"], *FDVs, labels=labels, colors=colors)
    cum_mc = 0
    for mc in FDVs:
        cum_mc+=mc
        ax1.plot(data["date_time"], cum_mc, color="white", linewidth=0.2)

    ax1.set_xlabel('Date')
    ax1.set_ylabel('FDV')
    ax1.legend(loc='upper left')
    # 设置x轴的时间间隔
    locator = ticker.MaxNLocator(10)  # 显示10个刻度
    ax1.xaxis.set_major_locator(locator)

    ax2 = ax1.twinx()
    ax2.plot(data["date_time"], np.log(data["btc_price"]), color='gray', label='Log(Btc Price)')
    ax2.set_ylabel('Log(Btc Price) (USD)')
    ax2.legend(loc='upper right')

    # plt.setp(ax1.xaxis.get_majorticklabels(), rotation=90)
    plt.savefig("FDV.png")
    plt.show()

def plotFDVPercentage(data):

    fig, ax1 = plt.subplots(figsize=(14, 7))

    FDVs = [
        data["altcoin_FDV_percentage"],
        data["stablecoin_FDV_percentage"],
        data["eth_FDV_percentage"],
        data["btc_FDV_percentage"],
    ]
    labels = ['Altcoin FDV Perc', 'Stable FDV Perc', 'Eth FDV Perc', 'Btc FDV Perc',]
    colors = ['#1f77b4', '#aec7e8', '#ffbb78', '#ff7f0e']
    stacks = ax1.stackplot(data["date_time"], *FDVs, labels=labels, colors=colors)

    cum_mc = 0
    for mc in FDVs:
        cum_mc+=mc
        ax1.plot(data["date_time"], cum_mc, color="white", linewidth=0.2)


    ax1.set_xlabel('Date')
    ax1.set_ylabel('FDV Percentage')
    ax1.legend(loc='upper left')
    # 设置x轴的时间间隔
    locator = ticker.MaxNLocator(5)  # 显示5个刻度
    ax1.xaxis.set_major_locator(locator)

    # 创建第二个y轴来绘制比特币价格
    ax2 = ax1.twinx()
    ax2.plot(data["date_time"], np.log(data["btc_price"]), color='gray', label='Log(Btc Price)')
    ax2.set_ylabel('Log(Btc Price) (USD)')
    ax2.legend(loc='upper right')

    plt.savefig("FDVPercentage.png")
    plt.show()



if __name__ == "__main__":
    # conn = getConn()
    # res = getFDV()

    FDV = pd.read_csv("fdv_data(cmc).csv")
    plotFDV(FDV)
    plotFDVPercentage(FDV)