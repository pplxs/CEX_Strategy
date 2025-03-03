
from get_marketcap import getConn, toDecimal
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import matplotlib.ticker as ticker

def getMarketCap(conn)->pd.DataFrame():
    sql = "select * from pv_market_cap_data_cmc;"
    cs = conn.cursor()
    cs.execute(sql)
    res = pd.DataFrame(cs.fetchall())
    res.columns = ['date_time', 'btc_marketCap', 'btc_marketCap_percentage', 'eth_marketCap', 'eth_marketCap_percentage','stablecoin_marketCap','stablecoin_marketCap_percentage','altcoin_marketCap','altcoin_marketCap_percentage','total_marketCap','btc_price']
    res.drop_duplicates(inplace=True,subset="date_time")
    res.dropna(inplace=True)
    res.sort_values(by="date_time",inplace=True)
    res.reset_index(inplace=True,drop=True)
    return res

def plotMarketCap(data):
    fig, ax1 = plt.subplots(figsize=(14, 7))
    market_caps = [
        data["altcoin_marketCap"],
        data["stablecoin_marketCap"],
        data["eth_marketCap"],
        data["btc_marketCap"],
    ]
    labels = ['Altcoin Market Cap', 'Stable Market Cap', 'Eth Market Cap', 'Btc Market Cap',]
    colors = ['#1f77b4', '#aec7e8', '#ffbb78', '#ff7f0e']
    stacks = ax1.stackplot(data["date_time"], *market_caps, labels=labels, colors=colors)
    cum_mc = 0
    for mc in market_caps:
        cum_mc+=mc
        ax1.plot(data["date_time"], cum_mc, color="white", linewidth=0.2)
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Market Cap')
    ax1.legend(loc='upper left')
    # 设置x轴的时间间隔
    locator = ticker.MaxNLocator(5)  # 显示10个刻度
    ax1.xaxis.set_major_locator(locator)

    ax2 = ax1.twinx()
    ax2.plot(data["date_time"], round(np.log(data["btc_price"]),2), color='gray', label='Log(Btc Price)')
    ax2.set_ylabel('Log(Btc Price) (USD)')
    ax2.legend(loc='upper right')

    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=0)
    plt.savefig("MarketCap.png")
    plt.show()

def plotMarketCapPercentage(data):
    fig, ax1 = plt.subplots(figsize=(14, 7))
    market_caps = [
        data["altcoin_marketCap_percentage"],
        data["stablecoin_marketCap_percentage"],
        data["eth_marketCap_percentage"],
        data["btc_marketCap_percentage"],
    ]
    labels = ['Altcoin Market Cap Perc', 'Stable Market Cap Perc', 'Eth Market Cap Perc', 'Btc Market Cap Perc',]
    colors = ['#1f77b4', '#aec7e8', '#ffbb78', '#ff7f0e']
    stacks = ax1.stackplot(data["date_time"], *market_caps, labels=labels, colors=colors)

    cum_mc = 0
    for mc in market_caps:
        cum_mc+=mc
        ax1.plot(data["date_time"], cum_mc, color="white", linewidth=0.2)


    ax1.set_xlabel('Date')
    ax1.set_ylabel('Market Cap Percentage')
    ax1.legend(loc='upper left')
    # 设置x轴的时间间隔
    locator = ticker.MaxNLocator(5)  # 显示5个刻度
    ax1.xaxis.set_major_locator(locator)

    # 创建第二个y轴来绘制比特币价格
    ax2 = ax1.twinx()
    ax2.plot(data["date_time"], round(np.log(data["btc_price"]),2), color='gray', label='Log(Btc Price)')
    ax2.set_ylabel('Log(Btc Price) (USD)')
    ax2.legend(loc='upper right')

    plt.savefig("MarketCapPercentage.png")
    plt.show()



if __name__ == "__main__":
    # conn = getConn()
    # res = getMarketCap()

    marketcap = pd.read_csv("market_cap_data_cmc.csv")
    # 业务表1： 市值占比
    # data1 = res[["date_time","btc_marketCap_percentage","eth_marketCap_percentage","stablecoin_marketCap_percentage","altcoin_marketCap_percentage","btc_price"]]
    plotMarketCap(marketcap)
    plotMarketCapPercentage(marketcap)