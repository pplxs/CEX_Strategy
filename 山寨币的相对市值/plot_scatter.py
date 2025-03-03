import plotly.express as px
import pandas as pd


def plotRelMv(df, est_tag):
    # 绘制动态散点图
    fig = px.scatter(
        df,
        x="industry",  # X轴：行业字符串
        y="market_cap_percentage",    # Y轴：市值百分比
        animation_frame="weekly",  # 动画帧：按月变化
        size="market_cap_percentage",  # 点的大小：市值百分比
        color="symbol",  # 点的颜色：符号
        hover_name="symbol",  # 悬停显示符号
        size_max=55,    # 点的最大大小
        title=f"{est_tag}estimate Symbol by Market Cap"
    )

    # 自定义布局
    fig.update_layout(
        width=1000,  # 图表宽度
        height=800,  # 图表高度
        xaxis_showgrid=False,  # 不显示X轴网格
        yaxis_showgrid=False,  # 不显示Y轴网格
        paper_bgcolor='rgba(0,0,0,0)',  # 背景透明
        plot_bgcolor='rgba(0,0,0,0)'    # 图表背景透明
    )

    fig.write_html(f'{est_tag}estimated_symbols.html')
    # 显示图表
    # fig.show()

if __name__ == "__main__":
    df = pd.read_csv('weekly_data_filter.csv')
    df['industry'] = pd.Categorical(df['industry'], categories=df['industry'].unique(), ordered=True)

    under_df = df[df['underestimated']==1].reset_index(drop=True)
    over_df = df[df['overestimated']==1].reset_index(drop=True)
    plotRelMv(under_df,est_tag='under')
    # plotRelMv(over_df,est_tag='over')