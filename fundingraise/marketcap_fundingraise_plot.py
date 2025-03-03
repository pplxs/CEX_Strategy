import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from matplotlib.ticker import FixedLocator

def plotMarketcapFundingraise(data):
    # 创建子图，减小两个子图之间的间距
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(20, 14), gridspec_kw={'hspace': 0.01})

    # 第一个子图
    labels_columns = ['(altcoin+eth)/(altcoin+eth+btc)']
    colors = ['#aec7e8']
    ax1.fill_between(data["date_time"], data[labels_columns[0]], color=colors[0], label=labels_columns[0], alpha=0.5)
    ax1.plot(data["date_time"], data[labels_columns], color="white", linewidth=0.2)

    ax1.set_ylabel('Market Cap Percentage', labelpad=5)
    ax1.tick_params(axis='y', labelsize=10)  # 设置y轴刻度标签大小

    # 创建季度标签
    data['quarter'] = data['date_time'].dt.to_period('Q').astype(str)

    quarter_ticks = data['quarter'].unique()  # 获取所有唯一的季度标签
    quarter_dates = []
    for q in quarter_ticks:
        year = int(q[:4])  # 提取年份
        quarter = int(q[-1])  # 提取季度（跳过 'Q' 字符）
        month = (quarter - 1) * 3 + 1  # 计算季度的第一个月
        quarter_dates.append(pd.Timestamp(year=year, month=month, day=1))

    quarter_dates_num = [mdates.date2num(d) for d in quarter_dates]

    ax1.xaxis.set_major_locator(FixedLocator(quarter_dates_num))  # 使用 FixedLocator 设置固定刻度位置
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-Q%q'))  # 设置日期格式

    labels = [f"{mdates.num2date(d).year}-Q{int((mdates.num2date(d).month-1)/3)+1}" for d in quarter_dates_num]
    ax1.set_xticklabels(labels, rotation=60)  # 设置x轴标签并旋转以便显示

    ax1.grid(True, linestyle='--', color='lightgray', linewidth=0.5, axis='both')  # 显示双向网格
    # ax1.set_xticks([])  # 隐藏第一个子图的x轴刻度
    ax1.legend(loc='upper left', fontsize='small', frameon=False)

    # 第一个子图的第二个y轴
    ax1b = ax1.twinx()
    labels = ['Pre_Seed_Round', 'Seed_Round', 'Angel_Round', 'A_Round', 'B_Round', 'C_Round', 'IPO_Round']
    colors = plt.get_cmap('tab10')(range(7))
    linestyles = ['-', '--', '-.', ':', '--','-','-']
    for i in range(len(labels)):
        ax1b.plot(data["date_time"], np.log(data[labels[i]]), color=colors[i], label=labels[i], linestyle=linestyles[i])

    ax1b.set_ylabel('Log(FoundingRaise Median) Per Year (USD)', labelpad=5)
    ax1b.tick_params(axis='y', labelsize=10)  # 设置y轴刻度标签大小
    ax1b.legend(loc='upper right', fontsize='small', frameon=False)

    # 第二个子图
    labels_columns = ['(altcoin+eth)/(altcoin+eth+btc)']
    colors = ['#aec7e8']
    ax2.fill_between(data["date_time"], data[labels_columns[0]], color=colors[0], label=labels_columns[0], alpha=0.5)
    ax2.plot(data["date_time"], data[labels_columns], color="white", linewidth=0.2)

    ax2.set_xlabel('Date')
    ax2.set_ylabel('Market Cap Percentage', labelpad=5)

    data['quarter'] = data['date_time'].dt.to_period('Q').astype(str)
    quarter_ticks = data['quarter'].unique()  # 获取所有唯一的季度标签
    quarter_dates = []
    for q in quarter_ticks:
        year = int(q[:4])  # 提取年份
        quarter = int(q[-1])  # 提取季度（跳过 'Q' 字符）
        month = (quarter - 1) * 3 + 1  # 计算季度的第一个月
        quarter_dates.append(pd.Timestamp(year=year, month=month, day=1))

    quarter_dates_num = [mdates.date2num(d) for d in quarter_dates]

    ax2.xaxis.set_major_locator(FixedLocator(quarter_dates_num))  # 使用 FixedLocator 设置固定刻度位置
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-Q%q'))  # 设置日期格式

    labels = [f"{mdates.num2date(d).year}-Q{int((mdates.num2date(d).month - 1) / 3) + 1}" for d in quarter_dates_num]
    ax2.set_xticklabels(labels, rotation=60)  # 设置x轴标签并旋转以便显示
    ax2.tick_params(axis='y', labelsize=10)  # 设置y轴刻度标签大小
    ax2.grid(True, linestyle='--', color='lightgray', linewidth=0.5)  # 显示网格
    ax2.legend(loc='upper left', fontsize='small', frameon=False)

    # 创建第三个y轴来显示BTC价格
    ax2b = ax2.twinx()
    ax2b.plot(data["date_time"], np.log(data['btc_price']), color='grey', label='Log(BTC Price)')
    ax2b.set_ylabel('Log(BTC Price) (USD)', labelpad=5, fontsize=10)
    ax2b.tick_params(axis='y', labelsize=10)  # 设置y轴刻度标签大小
    ax2b.legend(loc='lower right', fontsize='small', frameon=False)

    # 调整布局以防止标签重叠
    plt.tight_layout()

    plt.savefig("marketcap_fundingraise.png", bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    marketcap_fundingraise = pd.read_csv("marketcap_fundingraise.csv", parse_dates=['date_time'])
    plotMarketcapFundingraise(marketcap_fundingraise)